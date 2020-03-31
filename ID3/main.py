import math
import sys
import copy
import codecs


class AttributeList:
    """Class to represent a list of attributes"""

    def __init__(self):
        self.attributes = []

    def append(self, new_attribute):
        self.attributes.append(new_attribute)

    def get_list(self):
        return self.attributes

    def __str__(self):
        text = ""
        for elem in self.attributes:
            text += "[ " + str(elem) + " ]"
        return text


class ExamplesList:
    """Class to represent a list of examples"""

    def __init__(self):
        self.examples = []

    def append(self, newExample):
        self.examples.append(newExample)

    def get_list(self):
        return self.examples

    def __str__(self):
        text = ""
        for example in self.examples:
            for elem in example:
                text += "[ " + str(elem) + " ]"
            text += "\n"
        return text


class Table:
    """CLass to represent a table input for ID3 algorithim, it contains examples and attribute lists"""

    def __init__(self, attribute_list, examples_list):
        self.attribute_list = attribute_list
        self.examples_list = examples_list

    def get_examples(self):
        return self.examples_list

    def get_attributes(self):
        return self.attribute_list

    def num_positive_examples(self):
        count = 0
        for example in self.examples_list:
            if example[len(self.attribute_list) - 1] == "si":
                count += 1
        return count

    def num_negative_examples(self):
        count = 0
        for example in self.examples_list:
            if example[len(self.attribute_list) - 1] == "no":
                count += 1
        return count

    def num_examples(self):
        return len(self.examples_list)


def create_attribute_list_from_file(attribute_list, file_name):
    """Insert the attributes which are in the file, into the attribute_list"""
    f = open(file_name, "r")
    attributes = f.readline()[:-1].split(",")
    for elem in attributes:
        attribute_list.append(elem)
    f.close()


def create_example_list_from_file(examples_list, file_name):
    """Insert the examples from file into the examples_list"""
    f = open(file_name, "r")
    for line in f:
        values = line[:-1].split(",")
        examples_list.append(values)
    f.close()


def get_merit(example_list, N, attribute_index):
    """
    N = number of attributes
    attribute_index = index of the attribute to get the merit
    """
    # array of different attribute values of the table
    keys = []
    # array of positive or negative of the table
    values = []
    # iterate the examples
    for x in range(0, len(example_list)):
        keys.append(example_list[x][attribute_index])
        values.append(example_list[x][N - 1])

    # create dict to save frecuency (attribute_value, times) [soleado:5]
    frecuency = {}
    for key in keys:
        frecuency[key] = keys.count(key)

    frecuency_keys = []  # frecuency_keys contains unique attribute_values
    frecuency_values = []  # array of frecuency values
    # iterate the frecuency dict
    for key, value in frecuency.items():
        frecuency_keys.append(key)
        frecuency_values.append(value)

    ##create array of p,n and r for all attributes values
    p = [0] * len(frecuency_values)
    n = [0] * len(frecuency_values)
    r = [0] * len(frecuency_values)

    for i in range(0, len(example_list)):
        for j in range(0, len(frecuency_keys)):
            if keys[i] == frecuency_keys[j]:
                if values[i] == "si":
                    p[j] += 1
                elif values[i] == "no":
                    n[j] += 1
            r[j] = frecuency_values[j] / len(example_list)
    # get the merit
    merit = 0.00
    for i in range(0, len(frecuency)):
        if p[i] != 0 and n[i] != 0:
            term_1 = (p[i] / frecuency_values[i]) * math.log(
                (p[i] / frecuency_values[i]), 2
            )
            term_2 = (n[i] / frecuency_values[i]) * math.log(
                (n[i] / frecuency_values[i]), 2
            )
            merit = merit + (r[i] * (-term_1 - term_2))
    return merit


def sort_list(example_list, index_of_best_position, value_selected, num_attributes):
    examples_remaining = []
    # iterate over examples
    for i in range(len(example_list)):
        # create new example which won't contains the value selected in this step
        # [soleado,caluroso,alta,falso,no] ==> [caluroso,alta,falso,no]
        new_example = []
        # if soleado == soleado
        if example_list[i][index_of_best_position] == value_selected:
            for j in range(num_attributes):
                if j != index_of_best_position:
                    # append in new_example other values [caluroso,alta,falso,no]
                    new_example.append(example_list[i][j])
            examples_remaining.append(new_example)
    return examples_remaining


def id3(table):
    """ID3 Alogrithim"""
    # If the example list is empty, "return"; otherwise, continue.
    if not table.get_examples():
        return print("[RESULTADO]: No hay ejemplos")
    # If all the examples in the example list are +, return "+"; otherwise follow
    if table.num_positive_examples() == table.num_examples():
        return print("[RESULTADO]: +")
    # If all the examples in the example list are -, return "-"; otherwise follow
    if table.num_negative_examples() == table.num_examples():
        return print("[RESULTADO]: -")
    # If attribute list is empty, return "error";
    if not table.get_attributes:
        return print("[ERROR]: Lista de atributos vacía")
    else:
        # (1) call tbest_position an  item that minimizes merit
        merit_list = []
        for x in range(0, len(table.get_attributes()) - 1):
            merit = get_merit(table.get_examples(), len(table.get_attributes()), x)
            merit_list.append(merit)

        print("[MERITOS]")
        for i in range(len(merit_list)):
            print("   {}: {} ".format(table.get_attributes()[i], merit_list[i]))

        best_position = merit_list.index(min(merit_list))
        print(
            "El mejor atributo es",
            table.get_attributes()[best_position],
            "con mérito",
            min(merit_list),
            "\n",
        )
        # start a tree whose root is better:
        # for every value vi better
        examples_remaining = []
        attributes_remaining = []
        best_list = []
        # Get the best examples
        for example in range(0, len(table.get_examples())):
            if table.get_examples()[example][best_position] not in best_list:
                best_list.append(table.get_examples()[example][best_position])

        # include in examples_remaining the list items-examples which have vi value better.
        for i in range(len(best_list)):
            examples_remaining.append(
                sort_list(
                    table.get_examples(),
                    best_position,
                    best_list[i],
                    len(table.get_attributes()),
                )
            )

        # keep new attributes
        for i in range(len(table.get_attributes())):
            if i != best_position:
                attributes_remaining.append(table.get_attributes()[i])

        ##recursive call
        for i in range(len(examples_remaining)):
            print(
                "Para el valor",
                best_list[i],
                "del atributo",
                table.get_attributes()[best_position],
                ":",
            )
            # create new table with exampes and attributes remaining
            print("[SUBTABLA]")
            print("   Atributos: {}".format(attributes_remaining))
            for j in range(0,len(examples_remaining[i])):
                if j==0:
                    print("   Ejemplos:  {}".format(examples_remaining[i][j]))
                else:
                    print("              {}".format(examples_remaining[i][j]))
            id3(Table(attributes_remaining, examples_remaining[i]))


def main():
    x = None
    print("#" * 45)
    print("#        Bienvenido a la practica ID3       #")
    print("#" *45)
    while(True):
        print("#" * 45)
        print("¿Que ejemplo desea probar, seleccione un numero?")
        print(" 1. Ejercicio de Ejemplo de la práctica")
        print(" 2. Ejercicio trasparencia nº 18")
        print(" 3. Ejercicio trasparencia nº 23")
        print(" 4. Salir")
        
        try:
            x = input("Introduza su eleccion:")
            if int(x) < 0 or int(x) > 4: 
                raise Exception("Opcion invalida, debe estar entre [0-4]")
            else:
                attribute_list = AttributeList()
                examples_list = ExamplesList()
                if int(x) == 4:
                    return        
                elif int(x) == 1: 
                    create_attribute_list_from_file(attribute_list, "AtributosJuego.txt")
                    create_example_list_from_file(examples_list, "Juego.txt")
                elif int(x) == 2:
                    create_attribute_list_from_file(attribute_list, "AtributosDiap18.txt")
                    create_example_list_from_file(examples_list, "JuegoDiap18.txt")
                elif int(x) == 3:
                    create_attribute_list_from_file(attribute_list, "AtributosDiap23.txt")
                    create_example_list_from_file(examples_list, "JuegoDiap23.txt")
                table = Table(attribute_list.get_list(), examples_list.get_list())
                id3(table)
        except ValueError as e:
            print("SU selección ha de ser un número entre [0-4]")
        except Exception as e:
            print(e)



if __name__ == "__main__":
    main()
