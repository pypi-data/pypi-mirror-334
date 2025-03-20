"""
    ############################################################################################################################################################################################################################
    # This algorithm represents a revolutionary new architecture of artificial neural networks created by Sapiens Technology®, which is significantly faster and more accurate than conventional neural network architectures. #
    # The HurNet network, which uses back-division calculations where the computation starts from the output layer and goes back to the previous layers up to the input layer,                                                 #
    # dividing each current neuron by the immediately previous one in a single iteration,                                                                                                                                      #
    # manages to be significantly faster than traditional neural networks that use several iterations of weight adjustment through backpropagation.                                                                            #
    # The neural network architecture in question has been named HurNet (Hur, from Ben-Hur Varriano, who designed the mathematical architecture and the network algorithm; and Net, from neural network).                      #
    # The HurNet neural network does not rely on backpropagation or gradient calculations, achieving optimal weight adjustments in a single iteration.                                                                         #
    # This approach dramatically reduces demands for computational processing and can potentially increase training speed.                                                                                                     #
    # This algorithm is protected by copyright, and any public commentary, disclosure, or distribution of the HurNet algorithm code without prior authorization from Sapiens Technology® is strictly prohibited.               #
    # Reverse engineering and the creation of derivative algorithms through adaptations or inspirations based on the original calculations and code are also not allowed.                                                      #
    # Any violation of these prohibitions will be subject to legal action by our legal department.                                                                                                                             #
    ############################################################################################################################################################################################################################
"""
class MultiLayerHurNet:
    def __init__(self):
        try:
            from numpy import ndarray, array, sum, isscalar, mean, argmin, round, exp, tanh, maximum, where, max, log, clip, linalg
            from random import random
            from pickle import dump, load
            from os import path
            self.__ndarray = ndarray
            self.__isscalar = isscalar
            self.__array = array
            self.__exp = exp
            self.__tanh = tanh
            self.__maximum = maximum
            self.__where = where
            self.__max = max
            self.__sum = sum
            self.__log = log
            self.__clip = clip
            self.__linalg = linalg
            self.__argmin = argmin
            self.__random = random
            self.__mean = mean
            self.__dump = dump
            self.__path = path
            self.__load = load
            self.__round = round
            self.__one_dimensional_output = False
            self.__input_layer = None
            self.__output_sample_shape = None
            self.__weights = None
        except Exception as error:  print('ERROR in class construction: ' + str(error))
    def __integer_validation(self, integer=0): return int(integer) if type(integer) in (bool, int, float) else 0
    def __list_validation(self, x=[], y=None):
        if isinstance(x, self.__ndarray): x = x.tolist()
        elif x == []: x = [0]
        else: x = list(x) if type(x) in (tuple, list) else [x]
        if y is not None:
            if isinstance(y, self.__ndarray): y = y.tolist()
            elif y == []: y = [0]
            else: y = list(y) if type(y) in (tuple, list) else [y]
            try:
                x_length, y_length = len(x), len(y)
                if x_length != y_length:
                    minimum_length = min((x_length, y_length))
                    x = x[:minimum_length]
                    y = y[:minimum_length]
                if self.__isscalar(x[0]): x = [[a] for a in x]
                if self.__isscalar(y[0]): y, self.__one_dimensional_output = [[b] for b in y], True
            except: pass
            return self.__array(x), self.__array(y)
        if self.__isscalar(x[0]): x = [[a] for a in x]
        return self.__array(x)
    def __apply_activation(self, x=[], activation='linear'):
        if activation == 'sigmoid': return 1 / (1 + self.__exp(-x))
        elif activation == 'tanh': return self.__tanh(x)
        elif activation == 'relu': return self.__maximum(0, x)
        elif activation == 'leaky_relu': return self.__where(x > 0, x, x * 0.01)
        elif activation == 'softmax':
            exp_x = self.__exp(x - self.__max(x, axis=1, keepdims=True))
            return exp_x / self.__sum(exp_x, axis=1, keepdims=True)
        elif activation == 'softplus': return self.__log(1 + self.__exp(x))
        elif activation == 'elu': return self.__where(x > 0, x, 1.0 * (self.__exp(x) - 1))
        elif activation in ('silu', 'swish'): return x * (1 / (1 + self.__exp(-x)))
        elif activation == 'gelu': return x * (1 / (1 + self.__exp(-1.702 * x)))
        elif activation == 'selu': return 1.05070098 * self.__where(x > 0, x, 1.67326324 * (self.__exp(x) - 1))
        elif activation == 'mish': return x * self.__tanh(self.__log(1 + self.__exp(x)))
        elif activation == 'hard_sigmoid': return self.__clip((x + 3) / 6, 0, 1)
        else: return x
    def __proximityCalculation(self, sample=[]):
        sample = self.__array(sample)
        training = self.__array(self.__input_layer)
        differences = training - sample
        reshaped = differences.reshape(differences.shape[0], -1)
        distances = self.__linalg.norm(reshaped, axis=1)
        return self.__argmin(distances)
    def addHiddenLayer(self, num_neurons=0):
        try:
            num_neurons = self.__integer_validation(num_neurons)
            if num_neurons < 1: return False
            hidden_layer = [self.__random() for _ in range(num_neurons)]
            if not hasattr(self, '_hidden_layers'): self._hidden_layers = []
            self._hidden_layers.append(hidden_layer)
            return True
        except Exception as error:
            print('ERROR in addHiddenLayer: ' + str(error))
            return False
    def train(self, input_layer=[], output_layer=[], interaction=True, activation_function='linear', bias=0):
        try:
            input_array, output_array = self.__list_validation(x=input_layer, y=output_layer)
            interaction = bool(interaction) if type(interaction) in (bool, int, float) else True
            activation = activation_function.lower().strip() if isinstance(activation_function, str) else 'linear'
            bias = float(bias) if type(bias) in (bool, int, float) else 0
            self.__output_sample_shape = output_array.shape[1:] if output_array.ndim > 1 else ()
            if input_array.ndim > 1:
                axes = tuple(range(1, input_array.ndim))
                summation_function = self.__sum(input_array, axis=axes)
            else: summation_function = self.__sum(input_array)
            if isinstance(summation_function, self.__ndarray): summation_function = self.__where(summation_function == 0, 1, summation_function)
            else:
                if summation_function == 0: summation_function = 1
            n_samples = input_array.shape[0]
            if output_array.ndim > 1:
                reshape_dims = (n_samples,) + (1,) * (output_array.ndim - 1)
                summation_function = summation_function.reshape(reshape_dims)
            weights_per_sample = output_array / summation_function
            if not interaction: self.__weights = self.__mean(weights_per_sample, axis=0)
            else: self.__weights = weights_per_sample
            if hasattr(self, '_hidden_layers') and self._hidden_layers:
                for hidden_layer in self._hidden_layers:
                    avg_hidden = self.__mean(hidden_layer)
                    self.__weights = self.__apply_activation(self.__weights + (self.__weights * 0.1 * avg_hidden), activation)
            else: self.__weights = self.__apply_activation(self.__weights, activation)
            self.__weights = self.__weights + bias
            self.__input_layer = input_array.tolist()
            return True
        except Exception as error:
            print('ERROR in train: ' + str(error))
            self.__weights = output_layer
            return False
    def saveModel(self, model_path=''):
        try:
            model_path = model_path.strip() if isinstance(model_path, str) else str(model_path).strip()
            if len(model_path) < 1: model_path = 'model.hurnet'
            if not model_path.lower().endswith('.hurnet'): model_path += '.hurnet'
            if self.__weights is None: self.__weights = []
            self.__output_sample_shape = self.__output_sample_shape if type(self.__output_sample_shape) in (tuple, list, self.__ndarray) else [-1]
            if type(self.__output_sample_shape) == tuple: self.__output_sample_shape = list(self.__output_sample_shape)
            data = {
                'weights': self.__weights.tolist() if hasattr(self.__weights, 'tolist') else self.__weights,
                'input_layer': self.__input_layer.tolist() if hasattr(self.__input_layer, 'tolist') else self.__input_layer,
                'output_sample_shape': self.__output_sample_shape.tolist() if hasattr(self.__output_sample_shape, 'tolist') else self.__output_sample_shape,
                'one_dimensional_output': int(self.__one_dimensional_output)
            }
            with open(model_path, 'wb') as file: self.__dump(data, file)
            return True
        except Exception as error:
            print('ERROR in saveModel: ' + str(error))
            return False
    def loadModel(self, model_path=''):
        try:
            model_path = model_path.strip() if isinstance(model_path, str) else str(model_path).strip()
            if len(model_path) < 1: model_path = 'model.hurnet'
            if not model_path.lower().endswith('.hurnet'): model_path += '.hurnet'
            if not self.__path.isfile(model_path): return False
            with open(model_path, 'rb') as file: data = self.__load(file)
            def load_model(content=''):
                json_dictionary = {}
                content = str(content)
                try:
                    from json import loads
                    json_dictionary = loads(content)
                except:
                    from ast import literal_eval
                    json_dictionary = literal_eval(content)
                return json_dictionary
            data = load_model(content=data)
            self.__weights = self.__array(data['weights'])
            if len(self.__weights) < 1: self.__weights = None
            self.__input_layer = self.__array(data['input_layer'])
            try: self.__output_sample_shape = tuple(data['output_sample_shape'])
            except: self.__output_sample_shape = None
            if self.__output_sample_shape == (-1,): self.__output_sample_shape = None
            self.__one_dimensional_output = bool(data['one_dimensional_output'])
            return True
        except Exception as error:
            print('ERROR in loadModel: ' + str(error))
            return False
    def predict(self, input_layer=[], decimal_places=8):
        try:
            input_array = self.__list_validation(x=input_layer)
            decimal_places = int(decimal_places) if type(decimal_places) in (bool, int, float) else 8
            if self.__weights is None:
                print('No training has been carried out yet!')
                return input_layer
            n_samples = input_array.shape[0]
            if input_array.ndim > 1:
                axes = tuple(range(1, input_array.ndim))
                summation_function = self.__sum(input_array, axis=axes)
            else: summation_function = self.__sum(input_array)
            output_list = []
            single_weight = (hasattr(self.__weights, 'ndim') and (self.__weights.ndim == len(self.__output_sample_shape) or self.__weights.ndim == 0))
            for index in range(n_samples):
                if single_weight: weight = self.__weights
                else: weight = self.__weights[self.__proximityCalculation(input_array[index])]
                prediction = summation_function[index] * weight
                prediction = self.__round(prediction, decimal_places)
                if decimal_places < 1: prediction = self.__array(prediction).astype(int)
                if self.__output_sample_shape == () or self.__output_sample_shape is None:
                    try: prediction_out = prediction.item()
                    except: prediction_out = prediction
                else: prediction_out = prediction.tolist()
                output_list.append(prediction_out)
            if self.__one_dimensional_output: output_list = [output[0] for output in output_list]
            return output_list
        except Exception as error:
            print('ERROR in predict: ' + str(error))
            try:
                prediction = self.__round(self.__weights, decimal_places)
                if decimal_places < 1: prediction = self.__array(prediction).astype(int)
                return prediction.tolist() if hasattr(prediction, 'tolist') else prediction
            except: return input_layer
def measure_execution_time(function=print, display_message=True, *args, **kwargs):
    try:
        display_message = bool(display_message) if type(display_message) in (bool, int, float) else True
        from time import perf_counter
        start = perf_counter()
        result = function(*args, **kwargs)
        end = perf_counter()
        execution_time = abs(end - start)
        if display_message: print(f'Execution time: {execution_time:.10f} seconds.')
        return execution_time
    except: return 0
def tensor_similarity_percentage(obtained_output=[], expected_output=[]):
    try:
        from numpy import array, maximum, mean, where
        obtained_output = array(obtained_output)
        expected_output = array(expected_output)
        if obtained_output.shape != expected_output.shape: return 0
        difference = abs(obtained_output - expected_output)
        greatest_value = maximum(obtained_output, expected_output)
        greatest_value = where(greatest_value == 0, 1, greatest_value)
        quotient = difference / greatest_value
        average = min((1, max((0, mean(quotient)))))
        return 1 - average
    except: return 0
"""
    ############################################################################################################################################################################################################################
    # This algorithm represents a revolutionary new architecture of artificial neural networks created by Sapiens Technology®, which is significantly faster and more accurate than conventional neural network architectures. #
    # The HurNet network, which uses back-division calculations where the computation starts from the output layer and goes back to the previous layers up to the input layer,                                                 #
    # dividing each current neuron by the immediately previous one in a single iteration,                                                                                                                                      #
    # manages to be significantly faster than traditional neural networks that use several iterations of weight adjustment through backpropagation.                                                                            #
    # The neural network architecture in question has been named HurNet (Hur, from Ben-Hur Varriano, who designed the mathematical architecture and the network algorithm; and Net, from neural network).                      #
    # The HurNet neural network does not rely on backpropagation or gradient calculations, achieving optimal weight adjustments in a single iteration.                                                                         #
    # This approach dramatically reduces demands for computational processing and can potentially increase training speed.                                                                                                     #
    # This algorithm is protected by copyright, and any public commentary, disclosure, or distribution of the HurNet algorithm code without prior authorization from Sapiens Technology® is strictly prohibited.               #
    # Reverse engineering and the creation of derivative algorithms through adaptations or inspirations based on the original calculations and code are also not allowed.                                                      #
    # Any violation of these prohibitions will be subject to legal action by our legal department.                                                                                                                             #
    ############################################################################################################################################################################################################################
"""
