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
        for index in range(self.number_of_patterns):
            letter = lines.pop(0)
            pattern = ''
            for row in range(self.horizontal_resolution):
                pattern += lines.pop(0)
            self.patterns.append(Pattern(letter, pattern))


train_dataset = Dataset('train.txt')
patterns = train_dataset.patterns
for pattern in patterns:
    print(pattern.value)
