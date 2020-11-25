from math import sqrt


class Pattern:

    def __init__(self, letter, pattern):
        self.letter = letter
        self.value = self.pattern_to_value(pattern)
        self.normalize()

    def pattern_to_value(self, pattern):
        signs = list(pattern.replace('#', '1').replace('-', '0'))
        return list(map(int, signs))

    def normalize(self):
        ones = sum(self.value)
        root = sqrt(ones)
        for index, number in enumerate(self.value):
            self.value[index] /= root


class Dataset:

    def __init__(self, filename):
        with open(filename, newline='') as file:
            lines = file.read().strip().split('\r\n')

        self.patterns = []
        self.number_of_patterns = int(lines.pop(0))
        self.horizontal_resolution = int(lines.pop(0))
        self.vertical_resolution = int(lines.pop(0))
        self.shape = self.horizontal_resolution * self.vertical_resolution
        for index in range(self.number_of_patterns):
            letter = lines.pop(0)
            pattern = ''
            for row in range(self.horizontal_resolution):
                pattern += lines.pop(0)
            self.patterns.append(Pattern(letter, pattern))


class Network:

    def __init__(self, train_dataset):
        self.train_dataset = train_dataset
        self.letters = self.get_letters()
        self.input_neurons = self.dataset_to_inputs(self.train_dataset)
        self.layer = self.init_layer()

    def get_letters(self):
        letters = []
        for pattern in self.train_dataset.patterns:
            letters.append(pattern.letter)
        return letters

    def test(self, test_dataset):
        for test in test_dataset.patterns:
            input_neuron = InputNeron(test.value)
            self.input_neurons = [input_neuron]
            print(f'Letter {test.letter}')
            outputs = self.evaluate_layer(self.layer)
            best_confidence = max(outputs)
            best_letter = self.letters[outputs.index(best_confidence)]
            print(f'network has recognized letter {best_letter} with level of confidence = {round(best_confidence, 2)}')

    def evaluate_layer(self, layer):
        outputs = []
        for input in self.input_neurons:
            for index, neuron in enumerate(layer):
                output = neuron.compute_output(input.inputs)
                print(f'Confidence of letter {self.letters[index]}: {output}')
                outputs.append(output)
        return outputs

    def init_layer(self):
        layer = []
        for input in range(len(self.input_neurons)):
            weights = self.input_neurons[input].inputs.value
            layer.append(Neuron(weights))
        return layer

    def dataset_to_inputs(self, dataset):
        input_neurons = []
        patterns = dataset.patterns
        for pattern in patterns:
            input_neurons.append(InputNeron(pattern))
        return input_neurons


class InputNeron:

    def __init__(self, inputs):
        self.inputs = inputs


class Neuron:

    def __init__(self, weights):
        self.number_of_inputs = len(weights)
        self.weights = weights

    def compute_output(self, inputs):
        value = 0
        for i in range(self.number_of_inputs):
            value += self.weights[i] * inputs[i]
        return value


train_dataset = Dataset('train1.txt')
test_dataset = Dataset('test1.txt')
network = Network(train_dataset)
network.test(test_dataset)
