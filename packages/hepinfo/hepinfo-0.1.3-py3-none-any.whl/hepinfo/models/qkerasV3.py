### qkeras layers which use kerasV3 ###

import logging
import re
import warnings

import keras
import numpy as np
import tensorflow as tf
from keras.api import activations, constraints, initializers, ops, regularizers
from pyparsing import Group, Optional, Regex, Suppress, delimitedList


def _create_variable_name(attr_name, var_name=None):
    """Creates variable name.
    Arguments:
      attr_name: string. attribute name
      var_name: string. variable name

    Returns:
      string. variable name
    """

    if var_name:
        return var_name + '/' + attr_name

    # This naming scheme is to solve a problem of a layer having more than
    # one quantizer can have multiple qnoise_factor variables with the same
    # name of "qnoise_factor".
    return attr_name + '_' + str(ops.get_uid(attr_name))


class BaseQuantizer(tf.Module):
    """Base quantizer

    Defines behavior all quantizers should follow.
    """

    def __init__(self):
        self.built = False

    def build(self, var_name=None, use_variables=False):
        if use_variables:
            if hasattr(self, 'qnoise_factor'):
                self.qnoise_factor = tf.Variable(
                    lambda: tf.constant(self.qnoise_factor, dtype=tf.float32),
                    name=_create_variable_name('qnoise_factor', var_name=var_name),
                    dtype=tf.float32,
                    trainable=False,
                )
            if hasattr(self, 'integer'):
                self.integer = tf.Variable(
                    lambda: tf.constant(self.integer, dtype=tf.int32),
                    name=_create_variable_name('integer', var_name=var_name),
                    dtype=tf.int32,
                    trainable=False,
                )
        self.built = True

    def _set_trainable_parameter(self):
        pass

    def update_qnoise_factor(self, qnoise_factor):
        """Update qnoise_factor."""
        if isinstance(self.qnoise_factor, tf.Variable):
            # self.qnoise_factor is a tf.Variable.
            # This is to update self.qnoise_factor during training.
            self.qnoise_factor.assign(qnoise_factor)
        else:
            if isinstance(qnoise_factor, tf.Variable):
                # self.qnoise_factor is a numpy variable, and qnoise_factor is a
                # tf.Variable.
                self.qnoise_factor = qnoise_factor.eval()
            else:
                # self.qnoise_factor and qnoise_factor are numpy variables.
                # This is to set self.qnoise_factor before building
                # (creating tf.Variable) it.
                self.qnoise_factor = qnoise_factor

    # Override not to expose the quantizer variables.
    @property
    def variables(self):
        return ()

    # Override not to expose the quantizer variables.
    @property
    def trainable_variables(self):
        return ()

    # Override not to expose the quantizer variables.
    @property
    def non_trainable_variables(self):
        return ()


def stochastic_round(x, precision=0.5):
    """Performs stochastic rounding to the first decimal point."""
    scale = 1.0 / precision
    scale_x = x * scale
    fraction = scale_x - tf.floor(scale_x)

    result = tf.where(fraction < tf.random.uniform(tf.shape(x)), tf.math.floor(scale_x), tf.math.ceil(scale_x))
    return result / scale


def _round_through(x, use_stochastic_rounding=False, precision=0.5, training=True):
    """Rounds x but using straight through estimator.

    We use the trick from [Sergey Ioffe](http://stackoverflow.com/a/36480182).

    Straight through estimator is a biased estimator for the rounding
    operation defined by Hinton"s Coursera Lecture 9c where dL/dx is made
    equal to dL/dy for y = f(x) during gradient computation, where f(x) is
    a non-derivable function. In that case, we assume df/dx = 1 in:

    dL   dL df   dL
    -- = -- -- = --
    dx   df dx   dy

    (https://www.youtube.com/watch?v=LN0xtUuJsEI&list=PLoRl3Ht4JOcdU872GhiYWf6jwrk_SNhz9&index=41)

    Arguments:
      x: tensor to perform round operation with straight through gradient.
      use_stochastic_rounding: if true, we perform stochastic rounding.
      precision: by default we will use 0.5 as precision, but that can overriden
        by the user.

    Returns:
      Rounded tensor.
    """
    if use_stochastic_rounding:
        output = tf.cond(
            tf.cast(training, tf.bool),
            lambda: tf.add(x, tf.stop_gradient(-x + stochastic_round(x, precision))),
            lambda: tf.add(x, tf.stop_gradient(-x + tf.round(x))),
        )
    else:
        output = tf.add(x, tf.stop_gradient(-x + tf.round(x)))

    return tf.convert_to_tensor(output)


def _get_scaling_axis(scale_axis, len_axis):
    """Get the axis to perform auto scaling with."""

    if scale_axis is not None:
        axis = list(range(scale_axis))
        axis += list(range(scale_axis + 1, len_axis))
    else:
        if keras.backend.image_data_format() == 'channels_last':
            axis = list(range(len_axis - 1))
        else:
            axis = list(range(1, len_axis))
    return axis


def _get_scale(alpha, x, q, scale_axis=None, per_channel_scale=True):
    """Gets scaling factor for scaling the tensor per channel.
    It uses the least squares method to find the scaling factor.

    (https://en.wikipedia.org/wiki/Linear_least_squares)

    Arguments:
      alpha: A float or string. When it is string, it should be either "auto" or
        "auto_po2", and scale = sum(x * q, axis=all but last) / sum(q * q,
        axis=all but last)
       x: A tensor object. Its elements are in float.
       q: A tensor object. Its elements are in quantized format of x.
       scale_axis: which axis to calculate scale from
       per_channel_scale: A bool. Whether to perform per-channel scaling or not.

    Returns:
      A scaling factor tensor or scalar for scaling tensor per channel.
    """

    if isinstance(alpha, str) and 'auto' in alpha:
        assert alpha in ['auto', 'auto_po2']
        # in different tensorflow version (e.g., 2.4)
        # x.shape is a tuple which doesn't have as_list() method
        try:
            x_shape = x.shape.as_list()
        except AttributeError:
            x_shape = list(x.shape)

        len_axis = len(x_shape)
        if not per_channel_scale:
            qx = ops.mean(x * q, keepdims=True)
            qq = ops.mean(q * q, keepdims=True)
        else:
            if len_axis > 1:
                axis = _get_scaling_axis(scale_axis, len_axis)
                qx = ops.mean(tf.math.multiply(x, q), axis=axis, keepdims=True)
                qq = ops.mean(tf.math.multiply(q, q), axis=axis, keepdims=True)
            else:
                # No summing (averaging) along the channel axis to get per-channel
                # scales.
                qx = x * q
                qq = q * q

        scale = qx / (qq + keras.backend.epsilon())
        if alpha == 'auto_po2':
            scale = ops.power(2.0, tf.math.round(ops.log(scale + keras.backend.epsilon()) / np.log(2.0)))
    elif alpha is None:
        scale = 1.0
    elif isinstance(alpha, np.ndarray):
        scale = alpha
    else:
        scale = float(alpha)
    return scale


_default_sigmoid_type = 'hard'
_sigmoid = None


def hard_sigmoid(x):
    """Computes hard_sigmoid function that saturates between 0 and 1."""

    return ops.clip(0.5 * x + 0.5, 0.0, 1.0)


def smooth_sigmoid(x):
    """Implements a linear approximation of a sigmoid function."""

    # if we use 2.65 as the clipping point, MSE w.r.t. original sigmoid is
    # smaller than hard_simoid but the arithmetic for it is (x >> 3) +
    # (x >> 4) + 0.5, which is also not bad.

    return ops.clip(0.1875 * x + 0.5, 0.0, 1.0)


def set_internal_sigmoid(mode):
    """Sets _sigmoid to either real, hard or smooth."""

    global _sigmoid

    if mode not in ['real', 'hard', 'smooth']:
        raise ValueError("mode has to be 'real', 'hard' or 'smooth'.")

    if mode == 'hard':
        _sigmoid = hard_sigmoid
    elif mode == 'smooth':
        _sigmoid = smooth_sigmoid
    elif mode == 'real':
        _sigmoid = ops.sigmoid


set_internal_sigmoid(_default_sigmoid_type)


class quantized_relu(BaseQuantizer):  # pylint: disable=invalid-name
    """Computes a quantized relu to a number of bits.

    Modified from:

    [https://github.com/BertMoons/QuantizedNeuralNetworks-Keras-Tensorflow]

    Assume h(x) = +1 with p = sigmoid(x), -1 otherwise, the expected value of
    h(x) is:

    E[h(x)] = +1 P(p <= sigmoid(x)) - 1 P(p > sigmoid(x))
            = +1 P(p <= sigmoid(x)) - 1 ( 1 - P(p <= sigmoid(x)) )
            = 2 P(p <= sigmoid(x)) - 1
            = 2 sigmoid(x) - 1, if p is sampled from a uniform distribution U[0,1]

    If use_sigmoid is 0, we just keep the positive numbers up to
    2**integer * (1 - 2**(-bits)) instead of normalizing them, which is easier
    to implement in hardware.

    Attributes:
      bits: number of bits to perform quantization.
      integer: number of bits to the left of the decimal point.
      use_sigmoid: if true, we apply sigmoid to input to normalize it.
      negative_slope: slope when activation < 0, needs to be power of 2.
      use_stochastic_rounding: if true, we perform stochastic rounding.
      relu_upper_bound: A float representing an upper bound of the unquantized
        relu. If None, we apply relu without the upper bound when
        "is_quantized_clip" is set to false (true by default).
        Note: The quantized relu uses the quantization parameters (bits and
        integer) to upper bound. So it is important to set relu_upper_bound
        appropriately to the quantization parameters. "is_quantized_clip"
        has precedence over "relu_upper_bound" for backward compatibility.
      is_quantized_clip: A boolean representing whether the inputs are clipped to
        the maximum value represented by the quantization parameters. This
        parameter is deprecated, and the default is set to True for backwards
        compatibility. Users are encouraged to use "relu_upper_bound" instead.
      qnoise_factor: float. a scalar from 0 to 1 that represents the level of
        quantization noise to add. This controls the amount of the quantization
        noise to add to the outputs by changing the weighted sum of
        (1 - qnoise_factor)*unquantized_x + qnoise_factor*quantized_x.
      var_name: String or None. A variable name shared between the tf.Variables
        created in the build function. If None, it is generated automatically.
      use_ste: Bool. Whether to use "straight-through estimator" (STE) method or
          not.
      use_variables: Bool. Whether to make the quantizer variables to be dynamic
        tf.Variables or not.

    Returns:
      Function that performs relu + quantization to bits >= 0.
    """

    def __init__(
        self,
        bits=8,
        integer=0,
        use_sigmoid=0,
        negative_slope=0.0,
        use_stochastic_rounding=False,
        relu_upper_bound=None,
        is_quantized_clip=True,
        qnoise_factor=1.0,
        var_name=None,
        use_ste=True,
        use_variables=False,
    ):
        super().__init__()
        self.bits = bits
        self.integer = integer
        self.use_sigmoid = use_sigmoid
        self.negative_slope = negative_slope
        self.use_stochastic_rounding = use_stochastic_rounding
        self.relu_upper_bound = relu_upper_bound
        self.is_quantized_clip = is_quantized_clip
        self.qnoise_factor = qnoise_factor
        self.use_ste = use_ste
        assert negative_slope >= 0.0
        if negative_slope != 0.0:
            assert np.mod(np.log2(negative_slope), 1) == 0
        self.var_name = var_name
        self.use_variables = use_variables

    def __str__(self):
        # Converts Tensors to printable strings by converting to a numpy array and
        # then using regex to remove brackets when there is only one integer bit
        integer_bits = re.sub(
            r'\[(\d)\]', r'\g<1>', str(self.integer.numpy() if isinstance(self.integer, tf.Variable) else self.integer)
        )

        flags = [str(self.bits), integer_bits]
        if self.use_sigmoid or self.use_stochastic_rounding:
            flags.append(str(int(self.use_sigmoid)))
        if self.negative_slope:
            flags.append(str(self.negative_slope))
        if self.use_stochastic_rounding:
            flags.append(str(int(self.use_stochastic_rounding)))
        return 'quantized_relu(' + ','.join(flags) + ')'

    def __call__(self, x, training=True):
        if not self.built:
            self.build(var_name=self.var_name, use_variables=self.use_variables)

        non_sign_bits = self.bits - (self.negative_slope != 0.0)
        x = ops.cast(x, dtype='float32')
        m = ops.cast(ops.power(2, non_sign_bits), dtype='float32')
        m_i = ops.cast(ops.power(2, self.integer), dtype='float32')

        # is_quantized_clip has precedence over relu_upper_bound for backward
        # compatibility.
        m_f = ops.cast(
            ops.power(tf.constant(2.0, tf.float32), ops.cast(self.integer, dtype='float32') - non_sign_bits), dtype='float32'
        )
        if self.is_quantized_clip:
            x_u = tf.where(x <= m_i - m_f, ops.relu(x), tf.ones_like(x) * (m_i - m_f))
        elif self.relu_upper_bound is not None:
            x_u = tf.where(x <= self.relu_upper_bound, ops.relu(x), tf.ones_like(x) * self.relu_upper_bound)
        else:
            x_u = ops.relu(x)

        if self.use_sigmoid:
            p = _sigmoid(x / m_i) * m
            xq = m_i * keras.backend.clip(
                2.0 * (_round_through(p, self.use_stochastic_rounding, training=training) / m) - 1.0, 0.0, 1.0 - 1.0 / m
            )
            if self.negative_slope > 0:
                neg_factor = 1 / (self.negative_slope * m)
                xq = xq + m_i * self.negative_slope * keras.backend.clip(
                    2.0 * (_round_through(p * self.negative_slope, self.use_stochastic_rounding, training=training) * neg_factor)
                    - 1.0,
                    -1.0,
                    0.0,
                )
        else:
            p = x * m / m_i
            xq = m_i * ops.clip(_round_through(p, self.use_stochastic_rounding, training=training) / m, 0.0, 1.0 - 1.0 / m)
            if self.negative_slope > 0:
                neg_factor = 1 / (self.negative_slope * m)
                xq = xq + m_i * self.negative_slope * (
                    keras.backend.clip(
                        _round_through(p * self.negative_slope, self.use_stochastic_rounding, training=training) * neg_factor,
                        -1.0,
                        0.0,
                    )
                )

        if self.relu_upper_bound and not self.is_quantized_clip:
            xq = tf.where(xq <= self.relu_upper_bound, xq, tf.ones_like(xq) * self.relu_upper_bound)

        if self.use_ste:
            return x_u + tf.stop_gradient(self.qnoise_factor * (-x_u + xq))
        else:
            return (1 - self.qnoise_factor) * x_u + tf.stop_gradient(self.qnoise_factor * xq)

    def max(self):
        """Get the maximum value that quantized_relu can represent."""
        unsigned_bits = self.bits - (self.negative_slope != 0.0)

        if unsigned_bits > 0:
            return max(1.0, np.array(ops.power(2.0, ops.cast(self.integer, dtype='float32')), dtype='float32'))
        else:
            return 1.0

    def min(self):
        """Get the minimum value that quantized_relu can represent."""
        if self.negative_slope == 0.0:
            return 0.0

        unsigned_bits = self.bits - 1
        if unsigned_bits > 0:
            return min(
                -0.0, -self.negative_slope * np.array(ops.power(2.0, ops.cast(self.integer, dtype='float32')), dtype='float32')
            )
        else:
            return -1.0

    def range(self):
        """Returns a list of all values that quantized_relu can represent

        ordered by their binary representation ascending.
        """
        assert self.use_sigmoid == 0  # current unsupported
        assert self.negative_slope == 0  # # unsupported unsupported
        x = np.asarray(range(2**self.bits))
        return x * np.array(ops.power(2.0, -self.bits + ops.cast(self.integer, dtype='float32')), dtype='float32')

    @classmethod
    def from_config(cls, config):
        return cls(**config)

    def get_config(self):
        config = {
            'bits': self.bits,
            'integer': self.integer.numpy() if isinstance(self.integer, tf.Variable) else self.integer,
            'use_sigmoid': self.use_sigmoid,
            'negative_slope': self.negative_slope,
            'use_stochastic_rounding': self.use_stochastic_rounding,
            'relu_upper_bound': self.relu_upper_bound,
            'qnoise_factor': self.qnoise_factor.numpy() if isinstance(self.qnoise_factor, tf.Variable) else self.qnoise_factor,
        }
        return config


class bernoulli(BaseQuantizer):  # pylint: disable=invalid-name
    """Computes a Bernoulli sample with probability sigmoid(x).

    This computation uses ST approximation.

    To do that, we compute sigmoid(x) and a random sample z ~ U[0,1]. As
    p in [0,1] and z in [0,1], p - z in [-1,1]. However, -1 will
    never appear because to get -1 we would need sigmoid(-inf) - z == 1.
    As a result, the range will be in practical terms [0,1].

    The noise introduced by z can be seen as a regularizer to the weights W of
    y = Wx as y = Wx + Wz for some noise z with mean mu(z) and var(z). As a
    result, W**2 var(z) to the variance of y, which has the same effect as a
    regularizer on L2 with lambda = var(z), as presented in Hinton"s Coursera
    Lecture 9c.

    Remember that E[dL/dy] = E[dL/dx] once we add stochastic sampling.

    Attributes:
      alpha: allows one to specify multiplicative factor for number generation
        of "auto" or "auto_po2".
      temperature: amplifier factor for sigmoid function, making stochastic
        less stochastic as it moves away from 0.
      use_real_sigmoid: use real sigmoid for probability.

    Returns:
      Computation of round with stochastic sampling with straight through
      gradient.
    """

    def __init__(self, alpha=None, temperature=6.0, use_real_sigmoid=True, thr=None):
        super().__init__()
        self.alpha = alpha
        self.bits = 1
        self.temperature = temperature
        self.use_real_sigmoid = use_real_sigmoid
        self.default_alpha = 1.0
        self.scale = None
        if thr is not None:
            self.thr = tf.Variable(tf.ones([1]) * thr, trainable=True, dtype=tf.float32)
        else:
            self.thr = None

    def __str__(self):
        flags = []
        if self.alpha is not None:
            alpha = str(self.alpha)
            if isinstance(self.alpha, str):
                alpha = "'" + alpha + "'"
            flags.append('alpha=' + alpha)
        if self.temperature != 6.0:
            flags.append('temperature=' + str(self.temperature))
        if not self.use_real_sigmoid:
            flags.append('use_real_sigmoid=' + str(int(self.use_real_sigmoid)))
        return 'bernoulli(' + ','.join(flags) + ')'

    def __call__(self, x, training=True):
        if isinstance(self.alpha, str):
            assert self.alpha in ['auto', 'auto_po2']

        if isinstance(self.alpha, str):
            len_axis = len(x.shape)

            if len_axis > 1:
                if ops.image_data_format() == 'channels_last':
                    axis = list(range(len_axis - 1))
                else:
                    axis = list(range(1, len_axis))
            else:
                axis = [0]

            std = ops.std(x, axis=axis, keepdims=True) + keras.backend.epsilon()
        else:
            std = 1.0

        if self.use_real_sigmoid:
            p = keras.backend.sigmoid(self.temperature * x / std)
        else:
            p = _sigmoid(self.temperature * x / std)

        if training or self.thr is None:
            r = tf.random.uniform(tf.shape(x))
            q = tf.sign(p - r)
            q += 1.0 - tf.abs(q)
            q = (q + 1.0) / 2.0
        else:
            q = tf.where(p >= self.thr, tf.ones_like(p), tf.zeros_like(p))

        q_non_stochastic = tf.sign(x)
        q_non_stochastic += 1.0 - tf.abs(q_non_stochastic)
        q_non_stochastic = (q_non_stochastic + 1.0) / 2.0

        # if we use non stochastic binary to compute alpha,
        # this function seems to behave better
        scale = _get_scale(self.alpha, x, q_non_stochastic)
        self.scale = scale
        return x + tf.stop_gradient(-x + scale * q)

    def _set_trainable_parameter(self):
        if self.alpha is None:
            self.alpha = 'auto_po2'

    def max(self):
        """Get the maximum value bernoulli class can represent."""
        if self.alpha is None or isinstance(self.alpha, str):
            return 1.0
        else:
            return max(1.0, self.alpha)

    def min(self):
        """Get the minimum value bernoulli class can represent."""
        return 0.0

    @classmethod
    def from_config(cls, config):
        return cls(**config)

    def get_config(self):
        config = {'alpha': self.alpha, 'thr': self.thr.numpy().tolist() if self.thr is not None else None}
        return config



class BernoulliSampling(keras.layers.Layer):
    def __init__(self, num_samples=1, name=None, std=1, thr=0.5, temperature=6.0, use_quantized=False, bits_bernoulli_sigmoid=8, **kwargs):
        super().__init__(name=name, **kwargs)
        self.num_samples = num_samples
        self.std = std
        self.temperature = temperature
        self.use_quantized = use_quantized
        self.bits_bernoulli_sigmoid = bits_bernoulli_sigmoid
        if thr is not None:
            self.thr = tf.Variable(tf.ones([1]) * thr, trainable=False, dtype=tf.float32)
        else:
            self.thr = None

    def call(self, inputs, training=True):
        # convert inputs to sigmoid to get probablity for bernoulli
        if self.use_quantized:
            p = quantized_sigmoid(bits=self.bits_bernoulli_sigmoid, use_stochastic_rounding=True, symmetric=True)(
                self.temperature * inputs / self.std
            )
            p = tf.cast(p, tf.float32)
        else:
            p = ops.sigmoid(self.temperature * inputs / self.std)

        # sample num_samples times from a bernoulli
        out = tf.zeros(tf.shape(inputs))
        if training:
            for _ in range(self.num_samples):
                r = tf.random.uniform(tf.shape(inputs))
                q = tf.sign(p - r)
                q += 1.0 - tf.abs(q)
                q = (q + 1.0) / 2.0
                out += q
            out = out / self.num_samples
        else:
            out = tf.where(p >= self.thr, tf.ones_like(p), tf.zeros_like(p))

        # output is mean of stochastic sampling with straight through gradient
        out = inputs + tf.stop_gradient(-inputs + out)

        return out

    def max(self):
        """Get the maximum value bernoulli class can represent."""
        return 1.0

    def min(self):
        """Get the minimum value bernoulli class can represent."""
        return 0.0

    @classmethod
    def from_config(cls, config):
        return cls(**config)

    def get_config(self):
        config = {'num_samples': self.num_samples, 'thr': self.thr.numpy().tolist() if self.thr is not None else None}
        return config

class QActivation(keras.layers.Layer):
    """Implements quantized activation layers."""

    def __init__(self, activation, **kwargs):
        super().__init__(**kwargs)

        self.activation = activation

        if not isinstance(activation, str):
            self.quantizer = activation
            if hasattr(self.quantizer, '__name__'):
                self.__name__ = self.quantizer.__name__
            elif hasattr(self.quantizer, 'name'):
                self.__name__ = self.quantizer.name
            elif hasattr(self.quantizer, '__class__'):
                self.__name__ = self.quantizer.__class__.__name__
            return

        self.__name__ = activation

        try:
            self.quantizer = get_quantizer(activation)
        except KeyError:
            raise ValueError(f"invalid activation '{activation}'")

    def call(self, inputs):
        return self.quantizer(inputs)

    def get_config(self):
        config = {'activation': self.activation}
        base_config = super().get_config()
        return dict(list(base_config.items()) + list(config.items()))

    def get_quantization_config(self):
        return str(self.activation)

    def compute_output_shape(self, input_shape):
        return input_shape

    def get_prunable_weights(self):
        return []


class quantized_bits(BaseQuantizer):  # pylint: disable=invalid-name
    """Quantizes the number to a number of bits.

    In general, we want to use a quantization function like:

    a = (power(2,bits) - 1 - 0) / (max(x) - min(x))
    b = -min(x) * a

    in the equation:

    xq = a x + b

    This requires multiplication, which is undesirable. So, we
    enforce weights to be between -1 and 1 (max(x) = 1 and min(x) = -1),
    and separating the sign from the rest of the number as we make this function
    symmetric, thus resulting in the following approximation.

    1) max(x) = +1, min(x) = -1
    2) max(x) = -min(x)

    a = power(2,bits-1)
    b = 0

    Finally, just remember that to represent the number with sign, the
    largest representation is -power(2,bits) to power(2, bits-1)

    Symmetric and keep_negative allow us to generate numbers that are symmetric
    (same number of negative and positive representations), and numbers that
    are positive.

    Note:
      the behavior of quantized_bits is different than Catapult HLS ac_fixed
      or Vivado HLS ap_fixed. For ac_fixed<word_length, integer_lenth, signed>,
      when signed = true, it is equavlent to
      quantized_bits(word_length, integer_length-1, keep_negative=True)

    Attributes:
      bits: number of bits to perform quantization.
      integer: number of bits to the left of the decimal point.
      symmetric: if true, we will have the same number of values for positive
        and negative numbers.
      alpha: a tensor or None, the scaling factor per channel.
        If None, the scaling factor is 1 for all channels.
      keep_negative: if true, we do not clip negative numbers.
      use_stochastic_rounding: if true, we perform stochastic rounding.
      scale_axis: which axis to calculate scale from
      qnoise_factor: float. a scalar from 0 to 1 that represents the level of
        quantization noise to add. This controls the amount of the quantization
        noise to add to the outputs by changing the weighted sum of
        (1 - qnoise_factor)*unquantized_x + qnoise_factor*quantized_x.
      var_name: String or None. A variable name shared between the tf.Variables
        created in the build function. If None, it is generated automatically.
      use_ste: Bool. Whether to use "straight-through estimator" (STE) method or
          not.
      use_variables: Bool. Whether to make the quantizer variables to be dynamic
        tf.Variables or not.

    Returns:
      Function that computes fixed-point quantization with bits.
    """

    def __init__(
        self,
        bits=8,
        integer=0,
        symmetric=0,
        keep_negative=True,
        alpha=None,
        use_stochastic_rounding=False,
        scale_axis=None,
        qnoise_factor=1.0,
        var_name=None,
        use_ste=True,
        use_variables=False,
    ):
        super().__init__()
        self.bits = bits
        self.integer = integer
        self.symmetric = symmetric
        self.keep_negative = keep_negative
        self.alpha = alpha
        self.use_stochastic_rounding = use_stochastic_rounding
        # "auto*" |-> symmetric
        if isinstance(self.alpha, str):
            self.symmetric = True
        self.scale = None
        self.scale_axis = scale_axis
        self.qnoise_factor = qnoise_factor
        self.use_ste = use_ste
        self.var_name = var_name
        self.use_variables = use_variables

    def __str__(self):
        # Convert Tensors to printable strings by converting to a numpy array and
        # then using regex to remove brackets when there is only one integer bit
        integer_bits = re.sub(
            r'\[(\d)\]', r'\g<1>', str(self.integer.numpy() if isinstance(self.integer, tf.Variable) else self.integer)
        )

        flags = [str(self.bits), integer_bits, str(int(self.symmetric))]
        if not self.keep_negative:
            flags.append('keep_negative=False')
        if self.alpha:
            alpha = str(self.alpha)
            if isinstance(self.alpha, str):
                alpha = "'" + alpha + "'"
            flags.append('alpha=' + alpha)
        if self.use_stochastic_rounding:
            flags.append('use_stochastic_rounding=' + str(int(self.use_stochastic_rounding)))
        return 'quantized_bits(' + ','.join(flags) + ')'

    def __call__(self, x, training=True):
        """Computes fixedpoint quantization of x."""
        if not self.built:
            self.build(var_name=self.var_name, use_variables=self.use_variables)

        x = ops.cast(tf.convert_to_tensor(x), dtype='float32')

        # quantized_bits with "1" bit becomes a binary implementation.
        unsigned_bits = self.bits - self.keep_negative
        m = ops.cast(ops.power(2, unsigned_bits), dtype='float32')
        m_i = ops.cast(ops.power(2, self.integer), dtype='float32')

        if self.alpha is None:
            scale = 1.0
        elif isinstance(self.alpha, str):
            # We only deal with the symmetric case right now.
            assert self.symmetric, 'Only symmetric quantizers are implemented'
            len_axis = len(x.shape)
            if len_axis > 1:
                axis = _get_scaling_axis(self.scale_axis, len_axis)
            else:
                axis = [0]

            x = x / m_i

            # Using 2's complement, we can represent 2**(bits-1)-1 positive values
            # If we wish to maintain symmetry, we can double 2**(bits-1)-1 to get
            # the total number of possible values we can represent.
            # If symmetry is not enforced, then we can represent (2**bits)-1 values
            # using 2's complement.
            levels = (2 ** (self.bits - 1) - 1) * 2 if self.symmetric else (2**self.bits) - 1

            scale = (ops.max(abs(x), axis=axis, keepdims=True) * 2) / levels

            # If alpha is "auto_po2", then get the "best" po2 scale
            if 'po2' in self.alpha:
                scale = ops.power(2.0, tf.math.round(ops.log(scale + keras.backend.epsilon()) / np.log(2.0)))
                for _ in range(5):
                    v = tf.floor(tf.abs(x) / scale + 0.5)
                    mask = v < levels / 2
                    z = tf.sign(x) * tf.where(mask, v, tf.ones_like(v) * levels / 2)
                    scale = _get_scale(alpha='auto_po2', x=x, q=z, scale_axis=self.scale_axis)

            # If alpha is "auto", then get the "best" floating point scale
            elif self.alpha == 'auto':
                v = tf.floor(tf.abs(x) / scale + 0.5)
                mask = v < levels / 2
                z = tf.sign(x) * tf.where(mask, v, tf.ones_like(v) * levels / 2)
            else:
                raise ValueError(f"Invalid alpha '{self.alpha}'")

            # z is an integer number, so we must make the scale * m and z / m
            scale = scale * m

            # we will not use "z" right now because of stochastic_rounding
            # this is still under test.

            # if "new" in self.alpha:
            #  z = z / m
            #  self.scale = scale
            #  return x + tf.stop_gradient(-x + scale * z)
            x = m_i * x
            xq = m_i * z / m
            self.scale = scale
            xq = scale * xq

            if self.use_ste:
                return x + tf.stop_gradient(self.qnoise_factor * (-x + xq))
            else:
                return (1 - self.qnoise_factor) * x + tf.stop_gradient(self.qnoise_factor * xq)

        else:
            scale = self.alpha

        def handle_unsigned_bits(x, m, m_i, unsigned_bits):
            p = x * m / m_i
            xq = (
                m_i
                * tf.clip_by_value(
                    _round_through(p, self.use_stochastic_rounding, precision=1.0, training=training),
                    self.keep_negative * (-m + self.symmetric),
                    m - 1,
                )
                / m
            )
            return xq

        def handle_binary_quantization(x, keep_negative):
            xq = tf.sign(x)
            xq += 1.0 - tf.abs(xq)
            if not keep_negative:
                xq = (xq + 1.0) / 2.0
            return xq

        # quantized_bits with "1" bit becomes a binary implementation.
        xq = tf.cond(
            tf.cast(unsigned_bits > 0, tf.bool),  # Condition
            lambda: handle_unsigned_bits(x, m, m_i, unsigned_bits),  # True case
            lambda: handle_binary_quantization(x, self.keep_negative),  # False case
        )

        self.scale = scale
        xq = scale * xq

        if self.use_ste:
            return x + tf.stop_gradient(self.qnoise_factor * (-x + xq))
        else:
            return (1 - self.qnoise_factor) * x + tf.stop_gradient(self.qnoise_factor * xq)

    def _set_trainable_parameter(self):
        if self.alpha is None:
            self.alpha = 'auto_po2'
            self.symmetric = True

    def max(self):
        """Get maximum value that quantized_bits class can represent."""
        unsigned_bits = self.bits - self.keep_negative
        if unsigned_bits > 0:
            return max(1.0, np.array(ops.power(2.0, ops.cast(self.integer, dtype='float32')), dtype='float32'))
        else:
            return 1.0

    def min(self):
        """Get minimum value that quantized_bits class can represent."""
        if not self.keep_negative:
            return 0.0
        unsigned_bits = self.bits - self.keep_negative
        if unsigned_bits > 0:
            return -max(1.0, np.array(keras.ops.power(2, keras.ops.cast(self.integer, dtype='float32')), dtype='float32'))
        else:
            return -1.0

    def range(self):
        """Returns a list of all values that quantized_bits can represent
        ordered by their binary representation ascending."""
        assert self.symmetric == 0
        assert self.keep_negative
        assert self.alpha is None or self.alpha == 1.0

        x = np.asarray(range(2**self.bits), dtype=np.float32)
        p_and_n = np.where(x >= 2 ** (self.bits - 1), (x - 2 ** (self.bits - 1)) - 2 ** (self.bits - 1), x)
        return p_and_n * np.array(
            keras.ops.power(2.0, -self.bits + keras.ops.cast(self.integer, dtype='float32') + 1), dtype='float32'
        )

    @classmethod
    def from_config(cls, config):
        return cls(**config)

    def get_config(self):
        config = {
            'bits': self.bits,
            'integer': self.integer.numpy() if isinstance(self.integer, tf.Variable) else self.integer,
            'symmetric': self.symmetric,
            'alpha': self.alpha,
            'keep_negative': self.keep_negative,
            'use_stochastic_rounding': self.use_stochastic_rounding,
            'qnoise_factor': self.qnoise_factor.numpy() if isinstance(self.qnoise_factor, tf.Variable) else self.qnoise_factor,
        }
        return config


class Clip(keras.constraints.Constraint):
    """Clips weight constraint."""

    # This function was modified from Keras minmaxconstraints.
    #
    # Constrains the weights to be between min/max values.
    #   min_value: the minimum norm for the incoming weights.
    #   max_value: the maximum norm for the incoming weights.
    #   constraint: previous constraint to be clipped.
    #   quantizer: quantizer to be applied to constraint.

    def __init__(self, min_value=0.0, max_value=1.0, constraint=None, quantizer=None):
        """Initializes Clip constraint class."""

        self.min_value = min_value
        self.max_value = max_value
        self.constraint = keras.constraints.get(constraint)
        # Don't wrap yourself
        if isinstance(self.constraint, Clip):
            self.constraint = None
        self.quantizer = get_quantizer(quantizer)

    def __call__(self, w):
        """Clips values between min and max values."""
        if self.constraint:
            w = self.constraint(w)
            if self.quantizer:
                w = self.quantizer(w)
        w = ops.clip(w, self.min_value, self.max_value)
        return w

    def get_config(self):
        """Returns configuration of constraint class."""
        return {'min_value': self.min_value, 'max_value': self.max_value}

    @classmethod
    def from_config(cls, config):
        if isinstance(config.get('constraint', None), Clip):
            config['constraint'] = None
        config['constraint'] = keras.constraints.get(config.get('constraint', None))
        config['quantizer'] = get_quantizer(config.get('quantizer', None))
        return cls(**config)


def get_initializer(identifier):
    """Gets the initializer.

    Args:
      identifier: An initializer, which could be dict, string, or callable function.

    Returns:
      A initializer class

    Raises:
      ValueError: An error occurred when quantizer cannot be interpreted.
    """
    if identifier is None:
        return None
    if isinstance(identifier, dict):
        if identifier['class_name'] == 'QInitializer':
            return QInitializer.from_config(identifier['config'])
        else:
            return keras.initializers.get(identifier)
    elif isinstance(identifier, str):
        return keras.initializers.get(identifier)
    elif callable(identifier):
        return identifier
    else:
        raise ValueError('Could not interpret initializer identifier: ' + str(identifier))


class QInitializer(keras.initializers.Initializer):
    """Wraps around Keras initializer to provide a fanin scaling factor."""

    def __init__(self, initializer, use_scale, quantizer):
        self.initializer = initializer
        self.use_scale = use_scale
        self.quantizer = quantizer

        try:
            self.is_po2 = 'po2' in quantizer.__class__.__name__
        except:
            self.is_po2 = False

    def __call__(self, shape, dtype=None):
        x = self.initializer(shape, dtype)

        std_x = np.std(x)
        delta = self.quantizer.max() * 2**-self.quantizer.bits

        # delta is the minimum resolution of the number system.
        # we want to make sure we have enough values.
        if delta > std_x and hasattr(self.initializer, 'scale'):
            q = self.quantizer(x)
            max_q = np.max(abs(q))
            scale = 1.0
            if max_q == 0.0:
                xx = np.mean(x * x)
                scale = self.quantizer.max() / np.sqrt(xx)
            else:
                qx = np.sum(q * x)
                qq = np.sum(q * q)

                scale = qq / qx

            self.initializer.scale *= max(scale, 1)
            x = self.initializer(shape, dtype)

        return np.clip(x, -self.quantizer.max(), self.quantizer.max())

    def get_config(self):
        return {
            'initializer': self.initializer,
            'use_scale': self.use_scale,
            'quantizer': self.quantizer,
        }

    @classmethod
    def from_config(cls, config):
        config = {
            'initializer': get_initializer(config['initializer']),
            'use_scale': config['use_scale'],
            'quantizer': get_quantizer(config['quantizer']),
        }
        return cls(**config)


def get_constraint(identifier, quantizer):
    """Gets the initializer.

    Args:
      identifier: A constraint, which could be dict, string, or callable function.
      quantizer: A quantizer class or quantization function

    Returns:
      A constraint class
    """
    if identifier:
        if isinstance(identifier, dict) and identifier['class_name'] == 'Clip':
            return Clip.from_config(identifier['config'])
        else:
            return keras.constraints.get(identifier)
    else:
        max_value = max(1, quantizer.max()) if hasattr(quantizer, 'max') else 1.0
        return Clip(-max_value, max_value, identifier, quantizer)

def _need_exponent_sign_bit_check(max_value):
  """Checks whether the sign bit of exponent is needed.

  This is used by quantized_po2 and quantized_relu_po2.

  Args:
    max_value: the maximum value allowed.

  Returns:
    An integer. 1: sign_bit is needed. 0: sign_bit is not needed.
  """

  if max_value is not None:
    if max_value < 0:
      raise ValueError("po2 max_value should be non-negative.")
    if max_value > 1:
      # if max_value is larger than 1,
      #   the exponent could be positive and negative.
      #   e.g., log(max_value) > 0 when max_value > 1
      need_exponent_sign_bit = 1
    else:
      need_exponent_sign_bit = 0
  else:
    # max_value is not specified, so we cannot decide the range.
    # Then we need to put sign_bit for exponent to be safe
    need_exponent_sign_bit = 1
  return need_exponent_sign_bit


def get_auto_range_constraint_initializer(quantizer, constraint, initializer):
    """Get value range automatically for quantizer.

    Arguments:
     quantizer: A quantizer class in quantizers.py.
     constraint: A keras constraint.
     initializer: A keras initializer.

    Returns:
      a tuple (constraint, initializer), where
        constraint is clipped by Clip class in this file, based on the
        value range of quantizer.
        initializer is initializer contraint by value range of quantizer.
    """
    if quantizer is not None:
        constraint = get_constraint(constraint, quantizer)
        initializer = get_initializer(initializer)

        if initializer and initializer.__class__.__name__ not in ['Ones', 'Zeros', 'QInitializer']:
            # we want to get the max value of the quantizer that depends
            # on the distribution and scale
            if not (hasattr(quantizer, 'alpha') and isinstance(quantizer.alpha, str)):
                initializer = QInitializer(initializer, use_scale=True, quantizer=quantizer)
    return constraint, initializer


def Num(s):
    """Tries to convert string to either int or float."""
    try:
        try:
            return int(s)
        except ValueError:
            return float(s)
    except ValueError:
        # this should be always true. if it isn't int or float, it should be str
        assert (s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")
        s = s[1:-1]
        return s


def Str(s):
    return s[1:-1]


def IsNum(s):
    try:
        try:
            int(s)
            return True
        except ValueError:
            float(s)
            return True
    except ValueError:
        return False


def IsBool(s):
    if s in ['True', 'False']:
        return True
    else:
        return False


def Bool(s):
    return True if 'True' in s else False


def GetArg(s):
    if IsBool(s):
        return Bool(s)
    elif IsNum(s):
        return Num(s)
    else:
        return Str(s)


def GetParams(s):
    """Extracts args and kwargs from string."""
    # modified from https://stackoverflow.com/questions/38799223/parse-string-to-identify-kwargs-and-args  # pylint: disable=line-too-long

    _lparen = Suppress('(')  # pylint: disable=invalid-name
    _rparen = Suppress(')')  # pylint: disable=invalid-name
    _eq = Suppress('=')  # pylint: disable=invalid-name

    data = _lparen + Optional(delimitedList(Group(Regex(r'[^=,)\s]+') + Optional(_eq + Regex('[^,)]*'))))) + _rparen

    items = data.parseString(s).asList()

    # need to make sure that kwargs only happen after args are processed
    args = [GetArg(i[0]) for i in items if len(i) == 1]
    kwargs = {i[0]: GetArg(i[1]) for i in items if len(i) == 2}

    # check for syntax error
    for i in range(1, len(items)):
        if (len(items[i]) == 1) and (len(items[i - 1]) == 2):
            raise SyntaxError

    return args, kwargs


def safe_eval(eval_str, op_dict, *params, **kwparams):  # pylint: disable=invalid-name
    """Replaces eval by a safe eval mechanism."""

    function_split = eval_str.split('(')
    quantizer = op_dict.get(function_split[0], None)

    if len(function_split) == 2:
        args, kwargs = GetParams('(' + function_split[1])
    else:
        args = []
        kwargs = {}

    args = args + list(params)
    for k in kwparams:
        kwargs[k] = kwparams[k]

    # must be Keras activation object if None
    if quantizer is None:
        logging.info('keras dict %s', function_split[0])
        quantizer = keras.activations.get(function_split[0])

    if len(function_split) == 2 or args or kwargs:
        return quantizer(*args, **kwargs)
    else:
        if isinstance(quantizer, type):
            # Check if quantizer is a class
            return quantizer()
        else:
            # Otherwise it is a function, so just return it
            return quantizer


def _floor_through(x):
  """Computes the floor operation using straight through estimator."""

  return x + tf.stop_gradient(-x + tf.floor(x))


def stochastic_round_po2(x):
  """Performs stochastic rounding for the power of two."""
  # TODO(b/237832905): test stochastic_round_po2 and constraint.
  # because quantizer is applied after constraint.
  y = tf.abs(x)
  eps = tf.keras.backend.epsilon()
  log2 = tf.keras.backend.log(2.0)

  x_log2 = tf.round(tf.keras.backend.log(y + eps) / log2)
  po2 = tf.cast(pow(2.0, tf.cast(x_log2, dtype="float32")), dtype="float32")
  left_val = tf.where(po2 > y, x_log2 - 1, x_log2)
  right_val = tf.where(po2 > y, x_log2, x_log2 + 1)
  # sampling in [2**left_val, 2**right_val].
  minval = 2 ** left_val
  maxval = 2 ** right_val
  val = tf.random.uniform(tf.shape(y), minval=minval, maxval=maxval)
  # use y as a threshold to keep the probabliy [2**left_val, y, 2**right_val]
  # so that the mean value of the sample should be y
  x_po2 = tf.where(y < val, left_val, right_val)
  """
  x_log2 = stochastic_round(tf.keras.backend.log(y + eps) / log2)
  sign = tf.sign(x)
  po2 = (
      tf.sign(x) *
      tf.cast(pow(2.0, tf.cast(x_log2, dtype="float32")), dtype="float32")
  )
  """
  return x_po2


def _clip_power_of_two(x_abs,
                       min_exp,
                       max_exp,
                       max_value,
                       quadratic_approximation=False,
                       use_stochastic_rounding=False,
                       log2_rounding="rnd"):
  """Clips a tensor using power-of-two quantizer.


  Args:
    x_abs: A tensor object. Its elements should be non-negative.
    min_exp: An integer representing the smallest exponent.
    max_exp: An integer representing the largest exponent.
    max_value: A float or None. If it is None, we clip the value to max_value.
    quadratic_approximation: An boolean representing whether the quadratic
      approximation is applied.
    use_stochastic_rounding: An boolean representing whether the stochastic
      rounding method is applied.
    log2_rounding: log2 rounding mode. "rnd" and "floor" currently
      supported, corresponding to tf.round and tf.floor respectively.

  Returns:
    A tensor object, the values are clipped by min_exp and max_exp.
  """

  # if quadratic_approximation is True, round to the exponent for sqrt(x),
  # so that the return value can be divided by two without remainder.
  log2 = np.log(2.0)

  # When the elements of x_abs are small than the keras epsilon,
  # we just overwrite x_abs with eps
  eps = tf.keras.backend.epsilon()
  x_filter = tf.where(x_abs < eps, eps, x_abs)
  if max_value is not None:
    # If the elements of x_filter has value larger than x_value, clip it.
    x_filter = tf.where(x_filter >= max_value,
                        tf.ones_like(x_filter) * max_value, x_filter)

  def power_of_two_clip(x_abs, min_exp, max_exp, quadratic_approximation,
                        use_stochastic_rounding, log2_rounding):
    assert log2_rounding in ["rnd", "floor"]

    if quadratic_approximation:
      q_factor = 2.0
      x_input = tf.sqrt(x_abs)
    else:
      q_factor = 1.0
      x_input = x_abs

    if log2_rounding == "floor":
      x_log2 = _floor_through(tf.keras.backend.log(x_input) / log2)
    elif use_stochastic_rounding:
      x_log2 = tf.keras.tf_utils.smart_cond(
          tf.keras.learning_phase(),
          lambda: stochastic_round_po2(x_input),
          lambda: _round_through(tf.keras.backend.log(x_input) / log2))
    else:
      x_log2 = _round_through(tf.keras.backend.log(x_input) / log2)

    x_clipped = q_factor * tf.keras.backend.clip(x_log2, min_exp, max_exp)
    return x_clipped

  x_clipped = tf.where(
      x_abs < eps,
      tf.ones_like(x_abs) * min_exp,
      power_of_two_clip(x_filter, min_exp, max_exp, quadratic_approximation,
                        use_stochastic_rounding, log2_rounding))

  return x_clipped


def _get_min_max_exponents(non_sign_bits, need_exponent_sign_bit,
                           quadratic_approximation):
  """Given a bitwidth, gets min and max exponents that it can represent.

  Args:
    non_sign_bits: An integer representing the bitwidth of the exponent.
    need_exponent_sign_bit: An integer representing whether it needs sign bit
      in exponent. (1: need sign bit. 0: sign bit is not needed.)
    quadratic_approximation: A boolean representing whether the quadratic
      approximiation method is enforced.

  Returns:
    A tuple of integers: min_exp, max_exp
  """
  effect_bits = non_sign_bits - need_exponent_sign_bit
  min_exp = -2**(effect_bits)
  max_exp = 2**(effect_bits) - 1
  if quadratic_approximation:
    max_exp = 2 * (max_exp // 2)
  return min_exp, max_exp


def get_quantizer(identifier):
    """Gets the quantizer.

    Args:
      identifier: An quantizer, which could be dict, string, or callable function.

    Returns:
      A quantizer class or quantization function from this file. For example,
        Quantizer classes: quantized_bits, quantized_po2, quantized_relu_po2,
        binary, stochastic_binary, ternary, stochastic_ternary, etc.

        Quantization functions: binary_sigmoid, hard_sigmoid, soft_sigmoid, etc.

    Raises:
      ValueError: An error occurred when quantizer cannot be interpreted.
    """

    if identifier is None:
        return None
    if isinstance(identifier, dict):
        return keras.utils.deserialize_keras_object(identifier, module_objects=globals(), printable_module_name='quantizer')
    elif isinstance(identifier, str):
        return safe_eval(identifier, globals())
    elif callable(identifier):
        return identifier
    else:
        raise ValueError('Could not interpret quantizer identifier: ' + str(identifier))


class quantized_po2(BaseQuantizer):  # pylint: disable=invalid-name
  """Quantizes to the closest power of 2.

  Attributes:
    bits: An integer, the bits allocated for the exponent, its sign and the sign
      of x.
    max_value: An float or None. If None, no max_value is specified.
      Otherwise, the maximum value of quantized_po2 <= max_value
    use_stochastic_rounding: A boolean, default is False, if True, it uses
      stochastic rounding and forces the mean of x to be x statstically.
    quadratic_approximation: A boolean, default is False if True, it forces the
      exponent to be even number that closted to x.
    log2_rounding: A string, log2 rounding mode. "rnd" and "floor" currently
      supported, corresponding to tf.round and tf.floor respectively.
    qnoise_factor: float. a scalar from 0 to 1 that represents the level of
      quantization noise to add. This controls the amount of the quantization
      noise to add to the outputs by changing the weighted sum of
      (1 - qnoise_factor)*unquantized_x + qnoise_factor*quantized_x.
    var_name: String or None. A variable name shared between the tf.Variables
      created in the build function. If None, it is generated automatically.
    use_ste: Bool. Whether to use "straight-through estimator" (STE) method or
        not.
    use_variables: Bool. Whether to make the quantizer variables to be dynamic
      tf.Variables or not.
  """

  def __init__(self,
               bits=8,
               max_value=None,
               use_stochastic_rounding=False,
               quadratic_approximation=False,
               log2_rounding="rnd",
               qnoise_factor=1.0,
               var_name=None,
               use_ste=True,
               use_variables=False):
    super().__init__()
    self.bits = bits
    self.max_value = max_value
    self.use_stochastic_rounding = use_stochastic_rounding
    self.log2_rounding = log2_rounding
    # if True, round to the exponent for sqrt(x),
    # so that the return value can be divided by two without remainder.
    self.quadratic_approximation = quadratic_approximation
    need_exponent_sign_bit = _need_exponent_sign_bit_check(self.max_value)
    non_sign_bits = self.bits - 1
    self._min_exp, self._max_exp = _get_min_max_exponents(
        non_sign_bits, need_exponent_sign_bit, self.quadratic_approximation)
    # qnoise_factor related attributes
    self.qnoise_factor = qnoise_factor
    self.use_ste = use_ste
    self.var_name = var_name
    self.use_variables = use_variables

  def __str__(self):
    flags = [str(self.bits)]
    if self.max_value is not None or self.use_stochastic_rounding:
      flags.append(str(int(self.max_value)))
    if self.use_stochastic_rounding:
      flags.append(str(int(self.use_stochastic_rounding)))
    if self.quadratic_approximation:
      flags.append(
          "quadratic_approximation=" + str(int(self.quadratic_approximation)))
    return "quantized_po2(" + ",".join(flags) + ")"

  def __call__(self, x):
    if not self.built:
      self.build(var_name=self.var_name, use_variables=self.use_variables)

    x_sign = tf.sign(x)
    x_sign += (1.0 - tf.abs(x_sign))
    x_abs = tf.abs(x)
    x_clipped = _clip_power_of_two(x_abs, self._min_exp, self._max_exp,
                                   self.max_value,
                                   self.quadratic_approximation,
                                   self.use_stochastic_rounding,
                                   self.log2_rounding)
    xq = x_sign * pow(2.0, x_clipped)

    if self.use_ste:
      return x + tf.stop_gradient(self.qnoise_factor * (-x + xq))
    else:
      return (1 - self.qnoise_factor) * x + tf.stop_gradient(
          self.qnoise_factor * xq)

  def max(self):
    """Get the maximum value that quantized_po2 can represent."""
    if self.max_value:
      return max(1.0, self.max_value)
    else:
      return max(1.0, 2**self._max_exp)

  def min(self):
    """Get the minimum value that quantized_po2 can represent."""
    if self.max_value:
      return -max(1.0, self.max_value)
    else:
      return -max(1.0, 2**self._max_exp)

  @classmethod
  def from_config(cls, config):
    return cls(**config)

  def get_config(self):
    """Gets configugration of the quantizer.

    Returns:
      A dict mapping quantization configuration, including
        bits: bitwidth for exponents.
        max_value: the maximum value of this quantized_po2 can represent.
        use_stochastic_rounding:
          if True, stochastic rounding is used.
        quadratic_approximation:
          if True, the exponent is enforced to be even number, which is
          the closest one to x.
        log2_rounding:
          A string, Log2 rounding mode
    """
    config = {
        "bits":
            self.bits,
        "max_value":
            self.max_value,
        "use_stochastic_rounding":
            self.use_stochastic_rounding,
        "quadratic_approximation":
            self.quadratic_approximation,
        "qnoise_factor":
            self.qnoise_factor.numpy() if isinstance(
                self.qnoise_factor, tf.Variable) else self.qnoise_factor,
        "log2_rounding":
            self.log2_rounding
    }
    return config


class QDense(keras.layers.Dense):
    """Implements a quantized Dense layer."""

    # Most of these parameters follow the implementation of Dense in
    # Keras, with the exception of kernel_range, bias_range,
    # kernel_quantizer, bias_quantizer, and kernel_initializer.
    #
    # kernel_quantizer: quantizer function/class for kernel
    # bias_quantizer: quantizer function/class for bias
    # kernel_range/bias_ranger: for quantizer functions whose values
    #   can go over [-1,+1], these values are used to set the clipping
    #   value of kernels and biases, respectively, instead of using the
    #   constraints specified by the user.
    #
    # we refer the reader to the documentation of Dense in Keras for the
    # other parameters.

    def __init__(
        self,
        units,
        activation=None,
        use_bias=True,
        kernel_initializer='he_normal',
        bias_initializer='zeros',
        kernel_regularizer=None,
        bias_regularizer=None,
        activity_regularizer=None,
        kernel_constraint=None,
        bias_constraint=None,
        kernel_quantizer=None,
        bias_quantizer=None,
        kernel_range=None,
        bias_range=None,
        **kwargs,
    ):
        if kernel_range is not None:
            warnings.warn('kernel_range is deprecated in QDense layer.')

        if bias_range is not None:
            warnings.warn('bias_range is deprecated in QDense layer.')

        self.kernel_range = kernel_range
        self.bias_range = bias_range

        self.kernel_quantizer = kernel_quantizer
        self.bias_quantizer = bias_quantizer

        self.kernel_quantizer_internal = get_quantizer(self.kernel_quantizer)
        self.bias_quantizer_internal = get_quantizer(self.bias_quantizer)

        # optimize parameter set to "auto" scaling mode if possible
        if hasattr(self.kernel_quantizer_internal, '_set_trainable_parameter'):
            self.kernel_quantizer_internal._set_trainable_parameter()

        self.quantizers = [self.kernel_quantizer_internal, self.bias_quantizer_internal]

        kernel_constraint, kernel_initializer = get_auto_range_constraint_initializer(
            self.kernel_quantizer_internal, kernel_constraint, kernel_initializer
        )

        if use_bias:
            bias_constraint, bias_initializer = get_auto_range_constraint_initializer(
                self.bias_quantizer_internal, bias_constraint, bias_initializer
            )
        if activation is not None:
            activation = get_quantizer(activation)

        super().__init__(
            units=units,
            activation=activation,
            use_bias=use_bias,
            kernel_initializer=kernel_initializer,
            bias_initializer=bias_initializer,
            kernel_regularizer=kernel_regularizer,
            bias_regularizer=bias_regularizer,
            activity_regularizer=activity_regularizer,
            kernel_constraint=kernel_constraint,
            bias_constraint=bias_constraint,
            **kwargs,
        )

    def call(self, inputs):
        if self.kernel_quantizer:
            quantized_kernel = self.kernel_quantizer_internal(self.kernel)
        else:
            quantized_kernel = self.kernel
        output = ops.dot(inputs, quantized_kernel)
        if self.use_bias:
            if self.bias_quantizer:
                quantized_bias = self.bias_quantizer_internal(self.bias)
            else:
                quantized_bias = self.bias
            output = tf.nn.bias_add(output, quantized_bias, data_format='N...C')
        if self.activation is not None:
            output = self.activation(output)
        return output

    def compute_output_shape(self, input_shape):
        assert input_shape and len(input_shape) >= 2
        assert input_shape[-1]
        output_shape = list(input_shape)
        output_shape[-1] = self.units
        return tuple(output_shape)

    def get_config(self):
        config = {
            'units': self.units,
            'activation': activations.serialize(self.activation),
            'use_bias': self.use_bias,
            'kernel_quantizer': constraints.serialize(self.kernel_quantizer_internal),
            'bias_quantizer': constraints.serialize(self.bias_quantizer_internal),
            'kernel_initializer': initializers.serialize(self.kernel_initializer),
            'bias_initializer': initializers.serialize(self.bias_initializer),
            'kernel_regularizer': regularizers.serialize(self.kernel_regularizer),
            'bias_regularizer': regularizers.serialize(self.bias_regularizer),
            'activity_regularizer': regularizers.serialize(self.activity_regularizer),
            'kernel_constraint': constraints.serialize(self.kernel_constraint),
            'bias_constraint': constraints.serialize(self.bias_constraint),
            'kernel_range': self.kernel_range,
            'bias_range': self.bias_range,
        }
        base_config = super().get_config()
        return dict(list(base_config.items()) + list(config.items()))

    def get_quantization_config(self):
        return {
            'kernel_quantizer': str(self.kernel_quantizer_internal),
            'bias_quantizer': str(self.bias_quantizer_internal),
            'activation': str(self.activation),
            'units': str(self.units),
        }

    def get_quantizers(self):
        return self.quantizers

    def get_prunable_weights(self):
        return [self.kernel]


class quantized_sigmoid(BaseQuantizer):  # pylint: disable=invalid-name
    """Computes a quantized sigmoid to a number of bits.

    Attributes:
      bits: number of bits to perform quantization.
      symmetric: if true, we will have the same number of values for positive
        and negative numbers.
      use_real_sigmoid: if true, will use the sigmoid from Keras backend
      use_stochastic_rounding: if true, we perform stochastic rounding.

    Returns:
      Function that performs sigmoid + quantization to bits in the range 0.0 to 1.0.
    """

    def __init__(self, bits=8, symmetric=False, use_real_sigmoid=False, use_stochastic_rounding=False):
        super().__init__()
        self.bits = bits
        self.symmetric = symmetric
        self.use_real_sigmoid = use_real_sigmoid
        self.use_stochastic_rounding = use_stochastic_rounding

    def __str__(self):
        flags = [str(self.bits)]
        if self.symmetric:
            flags.append(str(int(self.symmetric)))
        if self.use_real_sigmoid:
            flags.append(str(int(self.use_real_sigmoid)))
        if self.use_stochastic_rounding:
            flags.append(str(int(self.use_stochastic_rounding)))
        return 'quantized_sigmoid(' + ','.join(flags) + ')'

    def __call__(self, x):
        x = ops.cast(x, 'float32')
        m = ops.power(2.0, self.bits)

        p = ops.sigmoid(x) if self.use_real_sigmoid else _sigmoid(x)

        return ops.clip((_round_through(p * m, self.use_stochastic_rounding) / m), (1.0 * self.symmetric) / m, 1.0 - 1.0 / m)

    def max(self):
        """Get the maximum value that quantized_sigmoid can represent."""
        return 1.0 - 1.0 / ops.power(2, self.bits)

    def min(self):
        """Get the minimum value that quantized_sigmoid can represent."""
        return (1.0 * self.symmetric) / ops.power(2, self.bits)

    @classmethod
    def from_config(cls, config):
        return cls(**config)

    def get_config(self):
        config = {
            'bits': self.bits,
            'symmetric': self.symmetric,
            'use_real_sigmoid': self.use_real_sigmoid,
            'use_stochastic_rounding': self.use_stochastic_rounding,
        }
        return config
