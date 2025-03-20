"""
    ############################################################################################################################################################################################################################
    # This algorithm represents a revolutionary new architecture of artificial neural networks created by Sapiens Technology®, which is significantly faster and more accurate than conventional neural network architectures. #
    # The neural network architecture in question has been named HurNet (Hur, from Ben-Hur Varriano, who designed the mathematical architecture and the network algorithm; and Net, from neural network).                      #
    # The HurNet neural network does not rely on backpropagation or gradient calculations, achieving optimal weight adjustments in a single iteration.                                                                         #
    # This approach dramatically reduces demands for computational processing and can potentially increase training speed.                                                                                                     #
    # This algorithm is protected by copyright, and any public commentary, disclosure, or distribution of the HurNet algorithm code without prior authorization from Sapiens Technology® is strictly prohibited.               #
    # Reverse engineering and the creation of derivative algorithms through adaptations or inspirations based on the original calculations and code are also not allowed.                                                      #
    # Any violation of these prohibitions will be subject to legal action by our legal department.                                                                                                                             #
    ############################################################################################################################################################################################################################
"""
class SingleLayerHurNetFX:
    def __init__(self):
        try:
            from numpy import exp, tanh, maximum, max, where, sum, log, clip, ndarray, isscalar, prod, hstack, ones, array, round
            from numpy.linalg import pinv
            from pickle import dump, load
            from os import path
            self.__exp = exp
            self.__tanh = tanh
            self.__maximum = maximum
            self.__where = where
            self.__max = max
            self.__sum = sum
            self.__log = log
            self.__clip = clip
            self.__ndarray = ndarray
            self.__isscalar = isscalar
            self.__array = array
            self.__prod = prod
            self.__hstack = hstack
            self.__ones = ones
            self.__pinv = pinv
            self.__dump = dump
            self.__path = path
            self.__load = load
            self.__round = round
            self.__one_dimensional_output = False
            self.__y_is_1d = False
            self.__activation = 'linear'
            self.__y_shape = None
            self.__weights = []
        except Exception as error:  print('ERROR in SingleLayerHurNetFX class construction: ' + str(error))
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
    def __add_features(self, x=[], activation='linear'):
        if x.ndim > 2: x = x.reshape(x.shape[0], -1)
        elif x.ndim == 1: x = x.reshape(-1, 1)
        interaction = self.__prod(x, axis=1).reshape(-1, 1)
        x = self.__hstack([x, interaction, self.__ones((x.shape[0], 1))])
        if activation not in ('linear', 'softmax'): x = self.__apply_activation(x=x, activation=activation)
        return x
    def train(self, input_layer=[], output_layer=[], interaction=True, activation_function='linear', bias=0):
        try:
            x, y = self.__list_validation(x=input_layer, y=output_layer)
            interaction = bool(interaction) if type(interaction) in (bool, int, float) else True
            activation = activation_function.lower().strip() if type(activation_function) == str else 'linear'
            bias = float(bias) if type(bias) in (bool, int, float) else 0
            x, y = self.__array(x), self.__array(y)
            x_augmented = self.__add_features(x=x, activation=activation)
            self.__y_is_1d, self.__activation = (y.ndim == 1), activation
            if y.ndim > 2:
                self.__y_shape = y.shape[1:]
                y = y.reshape(y.shape[0], -1)
            elif y.ndim == 1:
                self.__y_shape = None
                y = y.reshape(-1, 1)
            else: self.__y_shape = y.shape[1:] if y.shape[1:] != () else None
            x_augmented_transposed = x_augmented.T
            if not interaction: self.__weights = (self.__pinv(x_augmented) @ y) + bias
            else: self.__weights = (self.__pinv(x_augmented_transposed @ x_augmented) @ (x_augmented_transposed @ y)) + bias
            return True
        except Exception as error:
            print('ERROR in SingleLayerHurNetFX.train: ' + str(error))
            self.__weights = output_layer
            return False
    def saveModel(self, model_path=''):
        try:
            model_path = model_path.strip() if type(model_path) == str else str(model_path).strip()
            if len(model_path) < 1: model_path = 'model.hurnet'
            if not model_path.lower().endswith('.hurnet'): model_path += '.hurnet'
            self.__y_shape = self.__y_shape if type(self.__y_shape) in (tuple, list, self.__ndarray) else [-1]
            if type(self.__y_shape) == tuple: self.__y_shape = list(self.__y_shape)
            data = {
                'one_dimensional_output': int(self.__one_dimensional_output),
                'y_is_1d': int(self.__y_is_1d),
                'activation': str(self.__activation).lower().strip(),
                'y_shape': self.__y_shape.tolist() if hasattr(self.__y_shape, 'tolist') else self.__y_shape,
                'weights': self.__weights.tolist() if hasattr(self.__weights, 'tolist') else self.__weights 
            }
            with open(model_path, 'wb') as file: self.__dump(data, file)
            return True
        except Exception as error:
            print('ERROR in SingleLayerHurNetFX.saveModel: ' + str(error))
            return False
    def loadModel(self, model_path=''):
        try:
            model_path, data = model_path.strip() if type(model_path) == str else str(model_path).strip(), ''
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
            self.__activation = str(data['activation']).lower().strip()
            self.__weights = self.__array(data['weights'])
            try: self.__y_shape = tuple(data['y_shape'])
            except: self.__y_shape = None
            if self.__y_shape == (-1,): self.__y_shape = None
            self.__y_is_1d = bool(data['y_is_1d'])
            self.__one_dimensional_output = bool(data['one_dimensional_output'])
            return True
        except Exception as error:
            print('ERROR in SingleLayerHurNetFX.loadModel: ' + str(error))
            return False
    def predict(self, input_layer=[], decimal_places=8):
        try:
            x = self.__list_validation(x=input_layer)
            decimal_places = int(decimal_places) if type(decimal_places) in (bool, int, float) else 8
            x = self.__array(x)
            x_augmented = self.__add_features(x=x, activation=self.__activation)
            predictions = x_augmented @ self.__weights
            if self.__activation == 'softmax': predictions = self.__apply_activation(predictions, 'softmax')
            if decimal_places < 1: predictions = self.__round(predictions).astype(int)
            else: predictions = self.__round(predictions, decimal_places).astype(float)
            if self.__y_shape is not None:
                result = []
                for prediction in predictions: result.append(self.__array(prediction).reshape(self.__y_shape).tolist())
                predictions = result
            elif self.__y_is_1d: predictions = predictions.flatten().tolist()
            else: predictions = predictions.tolist()
            if self.__one_dimensional_output: predictions = [output[0] for output in predictions]
            return predictions
        except Exception as error:
            print('ERROR in SingleLayerHurNetFX.predict: ' + str(error))
            try:
                predictions = self.__weights
                if decimal_places < 1: predictions = self.__round(predictions).astype(int)
                else: predictions = self.__round(predictions, decimal_places).astype(float)
                return predictions.tolist() if hasattr(predictions, 'tolist') else predictions
            except: return input_layer
class MultiLayerHurNetFX:
    def __init__(self):
        try:
            from warnings import filterwarnings
            from numpy import exp, tanh, maximum, where, max, sum, log, clip, prod, hstack, ones, ndarray, isscalar, array, round
            from numpy.linalg import pinv
            from pickle import dump, load
            from os import path
            filterwarnings('ignore')
            self.__exp = exp
            self.__tanh = tanh
            self.__maximum = maximum
            self.__where = where
            self.__max = max
            self.__sum = sum
            self.__log = log
            self.__clip = clip
            self.__prod = prod
            self.__hstack = hstack
            self.__ones = ones
            self.__ndarray = ndarray
            self.__isscalar = isscalar
            self.__array = array
            self.__pinv = pinv
            self.__dump = dump
            self.__path = path
            self.__load = load
            self.__round = round
            self.__one_dimensional_output = False
            self.__num_hidden_layers = 0
            self.__y_is_1d = False
            self.__weights = []
            self.__y_shape = None
            self.__interaction = True
            self.__activation = 'linear'
        except Exception as error:  print('ERROR in MultiLayerHurNetFX class construction: ' + str(error))
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
    def __integer_validation(self, integer=0): return int(integer) if type(integer) in (bool, int, float) else 0
    def __add_features(self, x=[], interaction=True, activation='linear'):
        if x.ndim > 2: x = x.reshape(x.shape[0], -1)
        elif x.ndim == 1: x = x.reshape(-1, 1)
        if interaction:
            interaction_x = self.__prod(x, axis=1).reshape(-1, 1)
            x = self.__hstack([x, interaction_x, self.__ones((x.shape[0], 1))])
        else: x = self.__hstack([x, self.__ones((x.shape[0], 1))])
        if activation not in ('linear', 'softmax'): x = self.__apply_activation(x=x, activation=activation)
        return x
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
    def __fit(self, x=[], y=[], interaction=True, activation='linear', bias=0):
        x_augmented = x.copy()
        for _ in range(self.__num_hidden_layers + 1): x_augmented = self.__add_features(x=x_augmented, interaction=interaction, activation=activation)
        self.__y_is_1d = (y.ndim == 1)
        x_augmented_transposed = x_augmented.T
        if interaction: self.__weights = (self.__pinv(x_augmented) @ y) + bias
        else: self.__weights = (self.__pinv(x_augmented_transposed @ x_augmented) @ (x_augmented_transposed @ y)) + bias
    def addHiddenLayer(self, num_neurons=1):
        try:
            number_of_neurons = self.__integer_validation(integer=num_neurons)
            self.__num_hidden_layers += number_of_neurons
            return True
        except Exception as error:
            print('ERROR in MultiLayerHurNetFX.addHiddenLayer: ' + str(error))
            return False
    def train(self, input_layer=[], output_layer=[], interaction=True, activation_function='linear', bias=0):
        try:
            x, y = self.__list_validation(x=input_layer, y=output_layer)
            interaction = bool(interaction) if type(interaction) in (bool, int, float) else True
            activation = activation_function.lower().strip() if type(activation_function) == str else 'linear'
            bias = float(bias) if type(bias) in (bool, int, float) else 0
            x, y = self.__array(x), self.__array(y)
            if y.ndim > 2:
                self.__y_shape = y.shape[1:]
                y = y.reshape(y.shape[0], -1)
            elif y.ndim == 1:
                self.__y_shape = None
                y = y.reshape(-1, 1)
            else: self.__y_shape = y.shape[1:] if y.shape[1:] != () else None
            self.__interaction, self.__activation = interaction, activation
            try: self.__fit(x=x, y=y, interaction=self.__interaction, activation=activation, bias=bias)
            except:
                self.__num_hidden_layers = 0
                self.__interaction = False
                self.__fit(x, y, interaction=self.__interaction, activation=activation, bias=bias)
            return True
        except Exception as error:
            print('ERROR in MultiLayerHurNetFX.train: ' + str(error))
            self.__weights = output_layer
            return False
    def saveModel(self, model_path=''):
        try:
            model_path = model_path.strip() if type(model_path) == str else str(model_path).strip()
            if len(model_path) < 1: model_path = 'model.hurnet'
            if not model_path.lower().endswith('.hurnet'): model_path += '.hurnet'
            self.__y_shape = self.__y_shape if type(self.__y_shape) in (tuple, list, self.__ndarray) else [-1]
            if type(self.__y_shape) == tuple: self.__y_shape = list(self.__y_shape)
            data = {
                'one_dimensional_output': int(self.__one_dimensional_output),
                'y_shape': self.__y_shape.tolist() if hasattr(self.__y_shape, 'tolist') else self.__y_shape,
                'interaction': int(self.__interaction),
                'activation': self.__activation,
                'num_hidden_layers': int(self.__num_hidden_layers),
                'y_is_1d': int(self.__y_is_1d),
                'weights': self.__weights.tolist()
            }
            with open(model_path, 'wb') as file: self.__dump(data, file)
            return True
        except Exception as error:
            print('ERROR in MultiLayerHurNetFX.saveModel: ' + str(error))
            return False
    def loadModel(self, model_path=''):
        try:
            model_path, data = model_path.strip() if type(model_path) == str else str(model_path).strip(), ''
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
            try: self.__num_hidden_layers = int(data['num_hidden_layers'])
            except: self.__num_hidden_layers = 0
            try: self.__interaction = bool(data['interaction'])
            except: self.__interaction = True
            try: self.__weights = self.__array(data['weights'])
            except: self.__weights = []
            try: self.__activation = str(data['activation']).lower().strip()
            except: self.__activation = 'linear'
            try: self.__y_shape = tuple(data['y_shape'])
            except: self.__y_shape = None
            if self.__y_shape == (-1,): self.__y_shape = None
            try: self.__y_is_1d = bool(data['y_is_1d'])
            except: self.__y_is_1d = False
            try: self.__one_dimensional_output = bool(data['one_dimensional_output'])
            except: self.__one_dimensional_output = False
            return True
        except Exception as error:
            print('ERROR in MultiLayerHurNetFX.loadModel: ' + str(error))
            return False
    def predict(self, input_layer=[], decimal_places=8):
        try:
            x = self.__list_validation(x=input_layer)
            decimal_places = int(decimal_places) if type(decimal_places) in (bool, int, float) else 8
            x, number_of_hidden_layers = self.__array(x), self.__num_hidden_layers
            x_augmented = x.copy()
            for _ in range(number_of_hidden_layers + 1): x_augmented = self.__add_features(x_augmented, interaction=self.__interaction)
            predictions = x_augmented @ self.__weights
            if self.__activation == 'softmax': predictions = self.__apply_activation(predictions, 'softmax')
            if decimal_places < 1: predictions = self.__round(predictions).astype(int)
            else: predictions = self.__round(predictions, decimal_places).astype(float)
            if self.__y_shape is not None:
                result = []
                for prediction in predictions: result.append(self.__array(prediction).reshape(self.__y_shape).tolist())
                predictions = result
            elif self.__y_is_1d: predictions = predictions.flatten().tolist()
            else: predictions = predictions.tolist()
            if self.__one_dimensional_output: predictions = [output[0] for output in predictions]
            return predictions
        except Exception as error:
            print('ERROR in MultiLayerHurNetFX.predict: ' + str(error))
            try:
                predictions = self.__weights
                if decimal_places < 1: predictions = self.__round(predictions).astype(int)
                else: predictions = self.__round(predictions, decimal_places).astype(float)
                return predictions.tolist() if hasattr(predictions, 'tolist') else predictions
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
    # The neural network architecture in question has been named HurNet (Hur, from Ben-Hur Varriano, who designed the mathematical architecture and the network algorithm; and Net, from neural network).                      #
    # The HurNet neural network does not rely on backpropagation or gradient calculations, achieving optimal weight adjustments in a single iteration.                                                                         #
    # This approach dramatically reduces demands for computational processing and can potentially increase training speed.                                                                                                     #
    # This algorithm is protected by copyright, and any public commentary, disclosure, or distribution of the HurNet algorithm code without prior authorization from Sapiens Technology® is strictly prohibited.               #
    # Reverse engineering and the creation of derivative algorithms through adaptations or inspirations based on the original calculations and code are also not allowed.                                                      #
    # Any violation of these prohibitions will be subject to legal action by our legal department.                                                                                                                             #
    ############################################################################################################################################################################################################################
"""
