##################################################################################################################################################################
# This is a backpropagation-free Artificial Neural Network algorithm developed by Sapiens Technology®.                                                           #
# The algorithm is a simplified reduction without hidden layers to an example application of a HurNet-type Neural Network.                                       #
# HurNet networks are a technological creation of Sapiens Technology® and their distribution or copying without our permission is strictly prohibited.           #
# We do not permit copying, distribution or back-engineering of this or other versions of the HurNet network or any other code developed by Sapiens Technology®. #
# We will prosecute anyone who fails to comply with the rules set out here or who discloses any details about this code.                                         #
##################################################################################################################################################################
class SingleLayerHurNet:
    def __init__(self):
        try:
            from numpy import exp, tanh, maximum, max, where, sum, log, clip, ndarray, isscalar, array, sum, mean, linalg, argmin, round
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
            self.__mean = mean
            self.__linalg = linalg
            self.__argmin = argmin
            self.__round = round
            self.__dump = dump
            self.__path = path
            self.__load = load
            self.__output_shape = []
            self.__weights = None
            self.__input_layer = None
        except Exception as error: print('ERROR in class construction: ' + str(error))
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
    def __proximityCalculation(self, input_layer=[]):
        input_flat = self.__array(input_layer).flatten()
        input_layer_flat = self.__array([x.flatten() for x in self.__input_layer])
        differences = input_layer_flat - input_flat
        distances = self.__linalg.norm(differences, axis=1)
        return self.__argmin(distances)
    def train(self, input_layer=[], output_layer=[], interaction=True, activation_function='linear', bias=0):
        try:
            input_array, output_array = self.__list_validation(x=input_layer, y=output_layer)
            interaction = bool(interaction) if type(interaction) in (bool, int, float) else True
            activation = activation_function.lower().strip() if type(activation_function) == str else 'linear'
            bias = float(bias) if type(bias) in (bool, int, float) else 0
            self.__output_shape = [self.__array(x).shape for x in output_layer]
            input_flat = self.__array([self.__array(x).flatten() for x in input_layer])
            output_flat = self.__array([self.__array(x).flatten() for x in output_layer])
            summation_function = self.__sum(input_flat, axis=1, keepdims=True)
            summation_function[summation_function == 0] = 1
            weights_per_sample = output_flat / summation_function
            self.__weights = self.__mean(weights_per_sample, axis=0) if not interaction else weights_per_sample
            self.__weights = self.__apply_activation(x=self.__weights, activation=activation) + bias
            self.__input_layer = input_array
            return True
        except Exception as error:
            print(f'ERROR in train: ' + str(error))
            self.__weights = output_layer
            return False
    def saveModel(self, model_path=''):
        try:
            model_path = model_path.strip() if type(model_path) == str else str(model_path).strip()
            if len(model_path) < 1: model_path = 'model.hurnet'
            if not model_path.lower().endswith('.hurnet'): model_path += '.hurnet'
            data = {
                'weights': self.__weights.tolist() if hasattr(self.__weights, 'tolist') else self.__weights,
                'input_layer': self.__input_layer.tolist() if hasattr(self.__input_layer, 'tolist') else self.__input_layer,
                'output_shape': self.__output_shape.tolist() if hasattr(self.__output_shape, 'tolist') else self.__array(self.__output_shape).tolist()
            }
            with open(model_path, 'wb') as file: self.__dump(data, file)
            return True
        except Exception as error:
            print('ERROR in saveModel: ' + str(error))
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
            self.__weights = self.__array(data['weights'])
            self.__input_layer = self.__array(data['input_layer'])
            self.__output_shape = list(data['output_shape'])
            return True
        except Exception as error:
            print('ERROR in loadModel: ' + str(error))
            return False
    def predict(self, input_layer=[], decimal_places=8):
        try:
            outputs = []
            input_array = self.__list_validation(x=input_layer)
            decimal_places = int(decimal_places) if type(decimal_places) in (bool, int, float) else 8
            if self.__weights is None:
                print('No training has been carried out yet!!')
                return []
            if len(self.__weights.shape) == 1 or (len(self.__weights.shape) == 2 and self.__weights.shape[0] == 1):
                for inputs in input_array:
                    inputs_flat = self.__array(inputs).flatten()
                    summation_function = self.__sum(inputs_flat)
                    if summation_function == 0: summation_function = 1
                    output_flat = summation_function * self.__array(self.__weights)
                    output = output_flat.reshape(tuple(self.__output_shape[0]))
                    outputs.append(output)
            else:
                for inputs in input_array:
                    nearest_index = self.__proximityCalculation(inputs)
                    inputs_flat = self.__array(inputs).flatten()
                    summation_function = self.__sum(inputs_flat)
                    if summation_function == 0: summation_function = 1
                    weights = self.__weights[nearest_index]
                    output_flat = summation_function * self.__array(weights)
                    output = output_flat.reshape(tuple(self.__output_shape[nearest_index]))
                    outputs.append(output)
            outputs = self.__round(self.__array(outputs), decimal_places).tolist()
            if decimal_places < 1: outputs = self.__array(outputs).astype(int).tolist()
            return outputs
        except Exception as error:
            print(f'ERROR in predict: ' + str(error))
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
##################################################################################################################################################################
# This is a backpropagation-free Artificial Neural Network algorithm developed by Sapiens Technology®.                                                           #
# The algorithm is a simplified reduction without hidden layers to an example application of a HurNet-type Neural Network.                                       #
# HurNet networks are a technological creation of Sapiens Technology® and their distribution or copying without our permission is strictly prohibited.           #
# We do not permit copying, distribution or back-engineering of this or other versions of the HurNet network or any other code developed by Sapiens Technology®. #
# We will prosecute anyone who fails to comply with the rules set out here or who discloses any details about this code.                                         #
##################################################################################################################################################################
