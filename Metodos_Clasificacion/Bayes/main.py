import pandas as pd
import numpy as np
import math


def load_data(file_name):
    """Insert the examples from file into the examples_list"""
    f = open("../data/" + file_name, "r")
    examples_list = []
    for line in f:
        values = line[:-1].split(",")
        examples_list.append(values)
    f.close()

    return examples_list


class Bayes:
    """Class to represet Bayes"""

    def __init__(self, features):
        """init params"""
        self.labels = {}
        self.features = features

    def add_example(self, example_input, example_output):
        """add example to class"""
        if example_output not in self.labels.keys():
            self.labels[example_output] = Label(self.features, example_output)
        self.labels[example_output].new_example(example_input)

    def train(self):
        """get M vector and C Matrix for each label"""
        for label in self.labels:
            self.labels[label].generate_m()
            self.labels[label].generate_c()

    def predict(self, example):
        """get the lowest cost of all label for this example"""
        output = ""
        best = math.inf
        for label in self.labels:
            diff = np.transpose(example) - self.labels[label].get_m()
            dm = np.dot(np.dot(diff, np.linalg.inv(self.labels[label].get_c())), diff)
            if best > dm:
                best = dm
                output = label
        return output

    def get_class(self, label):
        return self.labels[label]


class Label:
    """Class to represent a possible output (iris-setosa, iris-versicolor)"""

    def __init__(self, features, label):
        """init params"""
        self.features = features
        self.label = label
        self.examples = []
        self.m = np.zeros(self.features, dtype=float)
        self.c = np.zeros((self.features, self.features), dtype=float)

    def get_label(self):
        """return the label name of the class"""
        return self.label

    def get_m(self):
        """get the m vector of the current label"""
        return self.m

    def get_c(self):
        """get c vector of the current label"""
        return self.c

    def new_example(self, example):
        """add new example to the label's example_list"""
        self.examples.append(example)

    def generate_m(self):
        """generate M vector"""
        for example in self.examples:
            for i in range(self.features):
                self.m[i] += example[i]
        self.m /= len(self.examples)

    def generate_c(self):
        """generate C matrix"""
        for example in self.examples:

            diff = np.matrix(example - self.m)

            mul = np.dot(diff, diff.T)
            # to avoid singular matrix
            if len(mul) != self.features or len((mul[0] != self.features)):
                mul = np.dot(diff.T, diff)
            self.c += mul

        self.c /= len(self.examples)


if __name__ == "__main__":
    """ Ejemplo de ladiapositiva 13 """
    print(">>>> Ejemplo diapositiva 13")
    bayes = Bayes(3)
    #######  EJEMPLO DIAPOSITIVA 13 ######
    bayes.add_example([50, 250, 200], "RGB")
    bayes.add_example([10, 254, 180], "RGB")
    bayes.add_example([20, 240, 210], "RGB")
    bayes.add_example([40, 248, 190], "RGB")
    bayes.add_example([56, 254, 202], "RGB")
    bayes.train()
    print("Clase RGB")
    print(">> M:\n")
    print(bayes.get_class("RGB").get_m())
    print(">> C:\n")
    print(bayes.get_class("RGB").get_c())
    print("[50,250,200] clasificado como clase ")
    print(bayes.predict([50, 250, 200]))

    ######## IRIS #########
    # Leer datos
    data = load_data("Iris2Clases.txt")
    bayes = Bayes(4)
    for example in data:
        bayes.add_example(
            [
                float(example[0]),
                float(example[1]),
                float(example[2]),
                float(example[3]),
            ],
            example[4],
        )
    bayes.train()
    print("Clase Iris setosa")
    print(">> M:\n")
    print(bayes.get_class("Iris-setosa").get_m())
    print(">> C:\n")
    print(bayes.get_class("Iris-setosa").get_c())
    print("Clase Iris versicolor")
    print(">> M:\n")
    print(bayes.get_class("Iris-versicolor").get_m())
    print(">> C:\n")
    print(bayes.get_class("Iris-versicolor").get_c())
    # TestIris01
    print(bayes.predict([5.1, 3.5, 1.4, 0.2]))
    # TestIris01
    print(bayes.predict([6.9, 3.1, 4.9, 1.5]))
    # TestIris01
    print(bayes.predict([5.0, 3.4, 1.5, 0.2]))
