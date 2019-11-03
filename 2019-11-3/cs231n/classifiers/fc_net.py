from builtins import range
from builtins import object
import numpy as np

from cs231n.layers import *
from cs231n.layer_utils import *


class TwoLayerNet(object):
    """
    A two-layer fully-connected neural network with ReLU nonlinearity and
    softmax loss that uses a modular layer design. We assume an input dimension
    of D, a hidden dimension of H, and perform classification over C classes.

    The architecure should be affine - relu - affine - softmax.

    Note that this class does not implement gradient descent; instead, it
    will interact with a separate Solver object that is responsible for running
    optimization.

    The learnable parameters of the model are stored in the dictionary
    self.params that maps parameter names to numpy arrays.
    """

    def __init__(self, input_dim=3*32*32, hidden_dim=100, num_classes=10,
                 weight_scale=1e-3, reg=0.0):
        """
        Initialize a new network.

        Inputs:
        - input_dim: An integer giving the size of the input
        - hidden_dim: An integer giving the size of the hidden layer
        - num_classes: An integer giving the number of classes to classify
        - dropout: Scalar between 0 and 1 giving dropout strength.
        - weight_scale: Scalar giving the standard deviation for random
          initialization of the weights.
        - reg: Scalar giving L2 regularization strength.
        """
        self.params = {}
        self.reg = reg

        ############################################################################
        # TODO: Initialize the weights and biases of the two-layer net. Weights    #
        # should be initialized from a Gaussian with standard deviation equal to   #
        # weight_scale, and biases should be initialized to zero. All weights and  #
        # biases should be stored in the dictionary self.params, with first layer  #
        # weights and biases using the keys 'W1' and 'b1' and second layer weights #
        # and biases using the keys 'W2' and 'b2'.                                 #
        ############################################################################
        #对于参数的初始化，W应服从正态分布，而b初始化可以默认为0
        self.params['W1'] = weight_scale * np.random.randn(input_dim, hidden_dim)
        self.params['W2'] = weight_scale * np.random.randn(hidden_dim, num_classes)
        self.params['b1'] = np.zeros(hidden_dim)
        self.params['b2'] = np.zeros(num_classes)
        
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################


    def loss(self, X, y=None):
        """
        Compute loss and gradient for a minibatch of data.

        Inputs:
        - X: Array of input data of shape (N, d_1, ..., d_k)
        - y: Array of labels, of shape (N,). y[i] gives the label for X[i].

        Returns:
        If y is None, then run a test-time forward pass of the model and return:
        - scores: Array of shape (N, C) giving classification scores, where
          scores[i, c] is the classification score for X[i] and class c.

        If y is not None, then run a training-time forward and backward pass and
        return a tuple of:
        - loss: Scalar value giving the loss
        - grads: Dictionary with the same keys as self.params, mapping parameter
          names to gradients of the loss with respect to those parameters.
        """
        scores = None
        ############################################################################
        # TODO: Implement the forward pass for the two-layer net, computing the    #
        # class scores for X and storing them in the scores variable.              #
        ############################################################################
        #应用之前写的前向传播函数
        layer1_out, layer1_cache = affine_relu_forward(X, self.params['W1'], self.params['b1'])
        layer2_out, layer2_cache = affine_forward(layer1_out, self.params['W2'], self.params['b2'])
        scores = layer2_out

        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        # If y is None then we are in test mode so just return scores
        if y is None:
            return scores

        loss, grads = 0, {}
        ############################################################################
        # TODO: Implement the backward pass for the two-layer net. Store the loss  #
        # in the loss variable and gradients in the grads dictionary. Compute data #
        # loss using softmax, and make sure that grads[k] holds the gradients for  #
        # self.params[k]. Don't forget to add L2 regularization!                   #
        #                                                                          #
        # NOTE: To ensure that your implementation matches ours and you pass the   #
        # automated tests, make sure that your L2 regularization includes a factor #
        # of 0.5 to simplify the expression for the gradient.                      #
        ############################################################################
        #根据公式可以写出梯度及loss，这里如果反向传播比较复杂，可以画图帮助理解
        loss, dscores = softmax_loss(scores, y)
        loss = loss + 0.5 * self.reg * np.sum(self.params['W1'] * self.params['W1']) + \
           0.5 * self.reg * np.sum(self.params['W2'] * self.params['W2'])
        d1_out, dw2, db2 = affine_backward(dscores, layer2_cache)
        grads['W2'] = dw2 + self.reg * self.params['W2']
        grads['b2'] = db2
        dx1, dw1, db1 = affine_relu_backward(d1_out, layer1_cache)
        grads['W1'] = dw1 + self.reg * self.params['W1']
        grads['b1'] = db1

        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        return loss, grads


class FullyConnectedNet(object):
    """
    A fully-connected neural network with an arbitrary number of hidden layers,
    ReLU nonlinearities, and a softmax loss function. This will also implement
    dropout and batch normalization as options. For a network with L layers,
    the architecture will be

    {affine - [batch norm] - relu - [dropout]} x (L - 1) - affine - softmax

    where batch normalization and dropout are optional, and the {...} block is
    repeated L - 1 times.

    Similar to the TwoLayerNet above, learnable parameters are stored in the
    self.params dictionary and will be learned using the Solver class.
    """

    def __init__(self, hidden_dims, input_dim=3*32*32, num_classes=10,
                 dropout=0, use_batchnorm=False, reg=0.0,
                 weight_scale=1e-2, dtype=np.float32, seed=None):
        """
        Initialize a new FullyConnectedNet.

        Inputs:
        - hidden_dims: A list of integers giving the size of each hidden layer.
        - input_dim: An integer giving the size of the input.
        - num_classes: An integer giving the number of classes to classify.
        - dropout: Scalar between 0 and 1 giving dropout strength. If dropout=0 then
          the network should not use dropout at all.
        - use_batchnorm: Whether or not the network should use batch normalization.
        - reg: Scalar giving L2 regularization strength.
        - weight_scale: Scalar giving the standard deviation for random
          initialization of the weights.
        - dtype: A numpy datatype object; all computations will be performed using
          this datatype. float32 is faster but less accurate, so you should use
          float64 for numeric gradient checking.
        - seed: If not None, then pass this random seed to the dropout layers. This
          will make the dropout layers deteriminstic so we can gradient check the
          model.
        """
        self.use_batchnorm = use_batchnorm
        self.use_dropout = dropout > 0
        self.reg = reg
        self.num_layers = 1 + len(hidden_dims)
        self.dtype = dtype
        self.params = {}

        ############################################################################
        # TODO: Initialize the parameters of the network, storing all values in    #
        # the self.params dictionary. Store weights and biases for the first layer #
        # in W1 and b1; for the second layer use W2 and b2, etc. Weights should be #
        # initialized from a normal distribution with standard deviation equal to  #
        # weight_scale and biases should be initialized to zero.                   #
        #                                                                          #
        # When using batch normalization, store scale and shift parameters for the #
        # first layer in gamma1 and beta1; for the second layer use gamma2 and     #
        # beta2, etc. Scale parameters should be initialized to one and shift      #
        # parameters should be initialized to zero.                                #
        ############################################################################
        #与两层结构不同的是，此处从2层延申到了N层，这里就额外设计对不同的层的参数进行初始化。
        #第二个需要注意的点是，batch_normalization的影响，因为会额外有scale与shift参数的初始化
        shape1 = input_dim 
        for i,shape2 in enumerate(hidden_dims):
            self.params['W'+str(i+1)] = weight_scale * np.random.randn(shape1, shape2)
            self.params['b'+str(i+1)] = np.zeros(shape2)
            shape1 = shape2 #对于前面N-1 层，w的维度均为上一次的shape1*该层shape2，对于最后一次有点例外，所以单独计算
            if self.use_batchnorm:
                self.params['gamma'+str(i+1)] = np.ones(shape2)
                self.params['beta'+str(i+1)] = np.zeros(shape2)
        self.params['W' + str(self.num_layers)] = weight_scale * np.random.randn(shape2,num_classes)
        self.params['b' + str(self.num_layers)] = np.zeros(num_classes)

        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        # When using dropout we need to pass a dropout_param dictionary to each
        # dropout layer so that the layer knows the dropout probability and the mode
        # (train / test). You can pass the same dropout_param to each dropout layer.
        self.dropout_param = {}
        if self.use_dropout:
            self.dropout_param = {'mode': 'train', 'p': dropout}
            if seed is not None:
                self.dropout_param['seed'] = seed

        # With batch normalization we need to keep track of running means and
        # variances, so we need to pass a special bn_param object to each batch
        # normalization layer. You should pass self.bn_params[0] to the forward pass
        # of the first batch normalization layer, self.bn_params[1] to the forward
        # pass of the second batch normalization layer, etc.
        self.bn_params = []
        if self.use_batchnorm:
            self.bn_params = [{'mode': 'train'} for i in range(self.num_layers - 1)]

        # Cast all parameters to the correct datatype
        for k, v in self.params.items():
            self.params[k] = v.astype(dtype)


    def loss(self, X, y=None):
        """
        Compute loss and gradient for the fully-connected net.

        Input / output: Same as TwoLayerNet above.
        """
        X = X.astype(self.dtype)
        mode = 'test' if y is None else 'train'

        # Set train/test mode for batchnorm params and dropout param since they
        # behave differently during training and testing.
        if self.use_dropout:
            self.dropout_param['mode'] = mode
        if self.use_batchnorm:
            for bn_param in self.bn_params:
                bn_param['mode'] = mode

        scores = None
        ############################################################################
        # TODO: Implement the forward pass for the fully-connected net, computing  #
        # the class scores for X and storing them in the scores variable.          #
        #                                                                          #
        # When using dropout, you'll need to pass self.dropout_param to each       #
        # dropout forward pass.                                                    #
        #                                                                          #
        # When using batch normalization, you'll need to pass self.bn_params[0] to #
        # the forward pass for the first batch normalization layer, pass           #
        # self.bn_params[1] to the forward pass for the second batch normalization #
        # layer, etc.                                                              #
        ############################################################################
        ar_cache = {}
        dp_cache = {}
        layer_input = X
        for i in range(1, self.num_layers):
            if self.use_batchnorm:
                layer_input, ar_cache[i-1] = affine_bn_relu_forward(
                    layer_input, self.params['W'+str(i)], self.params['b'+str(i)],
                self.params['gamma'+str(i)], self.params['beta'+str(i)], self.bn_params[i-1])
            else:
                layer_input, ar_cache[i-1] = affine_relu_forward(
                    layer_input, self.params['W'+str(i)], self.params['b'+str(i)])
            if self.use_dropout:
                layer_input, dp_cache[i-1] = dropout_forward(layer_input, self.dropout_param)

        layer_out, ar_cache[self.num_layers] = affine_forward(
            layer_input,self.params['W'+str(self.num_layers)], self.params['b'+str(self.num_layers)])
        scores = layer_out

        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        # If test mode return early
        if mode == 'test':
            return scores

        loss, grads = 0.0, {}
        ############################################################################
        # TODO: Implement the backward pass for the fully-connected net. Store the #
        # loss in the loss variable and gradients in the grads dictionary. Compute #
        # data loss using softmax, and make sure that grads[k] holds the gradients #
        # for self.params[k]. Don't forget to add L2 regularization!               #
        #                                                                          #
        # When using batch normalization, you don't need to regularize the scale   #
        # and shift parameters.                                                    #
        #                                                                          #
        # NOTE: To ensure that your implementation matches ours and you pass the   #
        # automated tests, make sure that your L2 regularization includes a factor #
        # of 0.5 to simplify the expression for the gradient.                      #
        ############################################################################
        loss, dscores = softmax_loss(scores, y)
        loss += 0.5 * self.reg * np.sum(self.params['W' + str(self.num_layers)] * self.params['W' + str(self.num_layers)])
        dout, dw, db = affine_backward(dscores, ar_cache[self.num_layers])
        grads['W'+str(self.num_layers)] = dw + self.reg * self.params['W' + str(self.num_layers)]
        grads['b'+str(self.num_layers)] = db
        for i in range(self.num_layers-1):
            layer = self.num_layers - i - 1
            loss += 0.5 * self.reg * np.sum(self.params['W' + str(layer)] * self.params['W' + str(layer)])
            if self.use_dropout:
                dout = dropout_backward(dout, dp_cache[layer-1])
            if self.use_batchnorm:
                dout, dw, db, dgamma, dbeta = affine_bn_relu_backward(dout, ar_cache[layer-1])
                grads['gamma' + str(layer)] = dgamma
                grads['beta' + str(layer)] = dbeta
            else:
                dout, dw, db = affine_relu_backward(dout, ar_cache[layer-1])
            grads['W' + str(layer)] = dw + self.reg * self.params['W' + str(layer)]
            grads['b' + str(layer)] = db

        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        return loss, grads