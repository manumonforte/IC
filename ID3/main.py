import math
import sys
import copy
import codecs


class AttributeList():
    def __init__(self):
        self.attributes = []
    def append(self,new_attribute):
        self.attributes.append(new_attribute)
    def get_list(self):
        return self.attributes
    def __str__(self):
        text = ""
        for elem in self.attributes:
            text+="[ "+str(elem)+" ]"
        return text

class ExamplesList():
    def __init__(self):
        self.examples= []
    def append(self,newExample):
        self.examples.append(newExample)
    def get_list(self):
        return self.examples
    def __str__(self):
        text = ""
        for example in self.examples:
            for elem in example:
                text+="[ "+str(elem)+" ]"
            text +="\n"
        return text


class Table():
    def __init__(self,attribute_list,examples_list):
        self.attribute_list = attribute_list
        self.examples_list = examples_list
    def get_examples(self):
        return self.examples_list
    def get_attributes(self):
        return self.attribute_list
    def num_positive_examples(self):
        count=0
        for example in self.examples_list:
            if example[len(self.attribute_list)-1] == "si":
                count +=1
        return count
    def num_negative_examples(self):
        count=0
        for example in self.examples_list:
            if example[len(self.attribute_list)-1] == "no":
                count +=1
        return count
    def num_examples(self):
        return len(self.examples_list)

def create_attribute_list_from_file(attribute_list, file_name):
    """Insert the attributes which are in the file, into the attribute_list"""
    f = open(file_name,'r')
    attributes = f.readline()[:-1].split(",")
    for elem in attributes:
        attribute_list.append(elem)
    f.close()

def create_example_list_from_file(examples_list, file_name):
    """Insert the examples from file into the examples_list"""
    f= open(file_name, 'r')
    for line in f:
        values = line[:-1].split(",")
        examples_list.append(values)
    f.close()

def get_merit(example_list,N,attribute_index):
    """
    N = number of attributes
    attribute_index = index of the attribute to get the merit
    """
    #array of different attribute values
    keys =[]
    #array of positive or negative 
    values = []
    #iterate the examples
    for x in range(0, len(example_list)):
        keys.append(example_list[x][attribute_index])
        values.append(example_list[x][N-1])

    #create dict to save frecuency (attribute_value, times)
    frecuency = {}
    for key in keys:
        frecuency[key] = keys.count(key)
    
    keys_2 = [] ##keys_2 contains unique attribute_values
    a = []
    #iterate the frecuency dict
    for key,value in frecuency.items():
        keys_2.append(key)
        a.append(value)
    
    ##create array of p,n and r for all attributes values
    p = [0] * len(a)
    n = [0] * len(a)
    r = [0] * len(a)

    for i in range (0,len(example_list)):#i--> 0-13
        for j in range (0,len(keys_2)): # j--> 0-2
            if keys[i] == keys_2[j]:
                if values[i] == "si":
                    p[j] += 1
                elif values[i] == "no":
                    n[j] += 1
            r[j] = a[j] / len(example_list)

    #get the merit
    merit = 0.00
    for i in range(0,len(frecuency)):
        if p[i] != 0 and n[i] != 0:
            term_1 = (p[i]/a[i])*math.log((p[i]/a[i]),2)
            term_2 = (n[i]/a[i])*math.log((n[i]/a[i]),2)
            merit = merit+(r[i]*(-term_1 - term_2))
    return merit


def sort_list(example_list,best_position,value,N):
    ejemplosRestantes = []
    for p in range(0,len(example_list)):
        ej = []
        print(example_list[p][best_position])
        print(value)
        if example_list[p][best_position] == value:
            for y in range(0,N):
                print(y)
                print(best_position)
                if y == best_position:
                    pass
                else:
                    ej.append(example_list[p][y])
            ejemplosRestantes.append(ej)
        else:
            pass
    return ejemplosRestantes


def sort_list(example_list,index_of_best_position,value_selected,num_attributes):
    examples_remaining = []
    #iterate over examples
    for i in range(len(example_list)):
    #create new example which won't contains the value selected in this step
    #[soleado,caluroso,alta,falso,no] ==> [caluroso,alta,falso,no] 
        new_example = []
        #if soleado == soleado
        if example_list[i][index_of_best_position]== value_selected:
            for j in range(num_attributes):
                if j != index_of_best_position:
                    #append in new_example other values [caluroso,alta,falso,no]
                    new_example.append(example_list[i][j])
            examples_remaining.append(new_example)
    return examples_remaining

def id3(table):
    """ID3 Alogrithim"""
    #Si lista-ejemplos está vacía, "regresar"; en caso contrario, seguir.
    if not table.get_examples():
        return 
    #Si todos los ejemplos en lista-ejemplos son +, devolver "+"; de otro modo seguir
    if table.num_positive_examples() == table.num_examples():
        return print("[RESULTADO]: +")
    #Si todos los ejemplos en lista-ejemplos son +, devolver "+"; de otro modo seguir
    if table.num_negative_examples() == table.num_examples():
        return print("[RESULTADO]: -")
    #Si lista-atributos está vacía, devolver "error";
    if not table.get_attributes:
        return print("[ERROR]: Lista de atributos vacía")
    else:
        #(1) llamar mejor al elemento a de lista-atributos que minimice mérito (a)
        merit_list = []
        for x in range(0,len(table.get_attributes())-1):
            merit = get_merit(table.get_examples(),len(table.get_attributes()),x)
            merit_list.append(merit)
        
        print("[MERITOS]")
        for i in range(len(merit_list)):
            print("   {}: {} ".format(table.get_attributes()[i], merit_list[i]))
    
        best_position = merit_list.index(min(merit_list))
        print("El mejor atributo es",table.get_attributes()[best_position],"con mérito",min(merit_list),'\n')
		#iniciar un árbol cuya raíz sea mejor:
        #para cada valor vi de mejor
        examples_remaining = []
        attributes_remaining = []
        best_list = []
        #Get the best examples
        for example in range(0,len(table.get_examples())):
            if table.get_examples()[example][best_position] not in best_list:
                best_list.append(table.get_examples()[example][best_position])

        #incluir en ejemplos-restantes los elementos de lista-ejemplos
        #que tengan valor v i del atributo mejor.
        for i in range (len(best_list)):
            examples_remaining.append(sort_list(table.get_examples(),best_position,best_list[i],len(table.get_attributes())))


        #nos quedamos con los nuevos atributos
        for i in range(len(table.get_attributes())):
            if i != best_position:
                attributes_remaining.append(table.get_attributes()[i])
            
        ##llamada recursiva
        for i in range(len(examples_remaining)):
            print("Para el valor",best_list[i],"del atributo",table.get_attributes()[best_position],":")
            # creamos tabla con los atributos restantes, y los ejemplos para el valor seleccionado en el paso
            print("[TABLA]")
            print("   Atributos: {}".format(attributes_remaining))
            print("   Ejemplos: {}".format(examples_remaining[i]))
            id3(Table(attributes_remaining,examples_remaining[i]))

def main():
    attribute_list =  AttributeList()
    examples_list = ExamplesList()
    create_attribute_list_from_file(attribute_list,"AtributosTest.txt")
    create_example_list_from_file(examples_list,"JuegoTest.txt")
    table = Table(attribute_list.get_list(),examples_list.get_list())
    id3(table)

if __name__ == "__main__":
	main()