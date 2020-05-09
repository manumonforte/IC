import numpy as np
import sys


class KMeans():
    """Class to represent K-Means algorithim"""
    def __init__(self,features):
        self.v_vectors = []
        self.labels = {}
        self.features = features
        self.U = []

    def add_vector(self,new_vector):
        """Add new vector to vectors attribute"""
        self.v_vectors.append(new_vector)

    def add_label(self,new_label):
        """Add new label to the labels dictionary"""
        self.labels[new_label.get_label_name()] = new_label

    def set_labels(self,labels):
        """Setter"""
        self.labels=labels

    def get_classes(self):
        """Getter"""
        return self.labels
    
    def set_U(self,new_U):
        """Set U matrix attribute"""
        self.U=new_U

    def train(self,epsilon,b):
        higher_distance = True
        counter = 1
        while(higher_distance):

            #Compute delta
            for label in self.labels.keys():
                delta = self.compute_v(self.labels[label],b)
                higher_distance = delta > epsilon
            print("Iteracion: {}".format(counter))

            for label in self.labels.keys():
                print("Vector-{}".format(label))
                print(self.labels[label].get_v_center())

            #Compute U
            self.update_U(b)
            print("Matriz U")
            print(np.transpose(self.U))
            counter+=1

    def compute_v(self,label,b):
        """Get new v center"""
        new_v = np.zeros((1,self.features),dtype="float")
        new_numerator= np.zeros((1,self.features),dtype="float")
        new_denominator = 0
        for i in range(len(self.v_vectors)):
            #compute numerator
            numerator = self.U[i][label.get_index()]
            new_numerator= np.add(new_numerator, np.dot(np.power(numerator,b),self.v_vectors[i]))
            #compute denominator
            denominator = self.U[i][label.get_index()]
            new_denominator = np.add(new_denominator,np.power(denominator,b))

        new_v = np.divide(new_numerator,new_denominator)
        delta = np.linalg.norm(np.subtract(new_v,label.get_v_center())) 
        label.set_v_center(new_v)

        return delta

    def compute_p(self,v1,v2,b):
        """computes de probabilty given 2 v centers"""
        dij = self.calculate_distance(v1,v2)
        numerator = 1/np.power(dij,(1/(b-1)))
        
        denominator= 0

        for label in self.labels.keys():
            drj = self.calculate_distance(v2,self.labels[label].get_v_center())
            denominator += 1/np.power(drj,(1/(b-1)))

        return numerator/denominator

    def calculate_distance(self,v1,v2):
        """Computes the euclidean distance of two vectors"""
        return np.power(np.linalg.norm(np.subtract(v1,v2)),2)

    def update_U(self,b):
        """Get new U Matrix"""
        for i in range(len(self.U)):
            for label in self.labels.keys():
                self.U[i][self.labels[label].get_index()] = self.compute_p(self.labels[label].get_v_center(),self.v_vectors[i],b)

    def get_distances_from_new_example(self,example):
        """Get all labels distances from the example given"""
        label_predicted= None
        min = float('inf')

        print ("Clasificacion de distancia vector {} ".format(example))
        for label in self.labels.keys():
            distance = self.calculate_distance(self.labels[label].get_v_center(),example)
            print ("Distancia a la clase {} : {}".format(self.labels[label].get_label_name(),distance))
            if(distance < min):
                min = distance
                label_predicted = label
        return label_predicted
    
    def get_probabilities_of_new_example(self,example,b):
        """Get all labels probabilities from the example given"""
        print("Clasificacion de probabilidad vector {}".format(example))
        p=[]
        for label in self.labels.keys():
            new_p = self.compute_p(self.labels[label].get_v_center(),example,b)
            p.append(self.labels[label].get_label_name() + " = "+str(new_p))
        return p
		

class Label():

    def __init__(self,index,label_name):
        """Class to represent Label of KMeans Algorithim"""
        self.v_center = []
        self.index = index
        self.label_name = label_name

    def get_v_center(self):
        """Getter"""
        return self.v_center

    def set_v_center(self,new_v):
        """Setter"""
        self.v_center=new_v

    def get_label_name(self):
        """Getter"""
        return self.label_name
    
    def get_index(self):
        return self.index



if __name__=="__main__":
    print("Ejemplo Diap 8")

    clase_1= Label(0,"Clase 1")
    clase_2 = Label(1,"Clase 2")
    clase_1.set_v_center([6.70,3.43])
    clase_2.set_v_center([2.39,2.94])

    kmedias = KMeans(2)

    matrix = [0.022,0.978,0.003,0.997,0.03,0.97,0.002,0.998,0.0,1.0,0.997,0.003,0.997,0.003,0.946,0.054,1.0,0.0,0.990,0.01]
    matrix = np.reshape(matrix,(10,2))
    kmedias.set_U(matrix)

    kmedias.add_label(clase_1)
    kmedias.add_label(clase_2)

    kmedias.add_vector([1,1])
    kmedias.add_vector([1,3])
    kmedias.add_vector([1,5])
    kmedias.add_vector([2,2])
    kmedias.add_vector([2,3])
    kmedias.add_vector([6,3])
    kmedias.add_vector([6,4])
    kmedias.add_vector([7,1])
    kmedias.add_vector([7,3])
    kmedias.add_vector([7,5])

    kmedias.train(epsilon=0.02,b=2)

    print (kmedias.get_distances_from_new_example([2,3]))
    print (kmedias.get_probabilities_of_new_example([2,3],b=2))

    #######################################################################