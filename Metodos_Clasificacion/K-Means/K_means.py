import numpy as np
import sys
import random
import logging

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
            logging.info("#" * 50)
            logging.info("[ ITERACION: {} ]".format(counter))
            logging.info("#" * 50)

            for label in self.labels.keys():
                logging.info("[ VECTOR-{} ]".format(label))
                logging.info(self.labels[label].get_v_center())

            #Compute U
            self.update_U(b)
            logging.info("[ MATRIZ U ]")
            logging.info(np.transpose(self.U))
            counter+=1

    def compute_v(self,label,b):
        """Get new v center"""
        new_v = np.zeros((1,self.features),dtype="float")
        new_numerator= np.zeros((1,self.features),dtype="float")
        new_denominator = 0
        for i in range(len(self.v_vectors)):
            #compute numerator
            numerator = self.U[i][label.get_index()]
            new_numerator= np.add(new_numerator, np.dot(np.power(numerator,b), self.v_vectors[i]))
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

        print ("Muestra: {} ".format(example))
        for label in self.labels.keys():
            distance = self.calculate_distance(self.labels[label].get_v_center(),example)
            print ("Distancia a la clase {} : {}".format(self.labels[label].get_label_name(),distance))
            if(distance < min):
                min = distance
                label_predicted = label
        return "Clasificacion: " + label_predicted
    
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

def generate_random_U(num_vectors,num_labels):

    matrix = []
    for i in range(num_vectors):
        elem = random.uniform(0, 1)
        matrix.append(elem)
        matrix.append(1-elem)
    return np.reshape(matrix,(num_vectors,num_labels))

if __name__=="__main__":

    filename="../logs/Kmeans.log"
    logging.basicConfig(filename=filename, filemode='w',format='%(asctime)s - %(message)s', level=logging.INFO)
    log = logging.getLogger()  # root logger
    for hdlr in log.handlers[:]:  # remove all old handlers
        log.removeHandler(hdlr)
    log.addHandler(logging.FileHandler(filename, 'w'))   


    print("-" *50)
    print("CASOS DE PRUEBA")
    print("-" *50)

    clase_1= Label(0,"Iris Setosa")
    clase_2 = Label(1,"Iris Versicolor")
    clase_1.set_v_center([4.6,3.0,4.0,0.0])
    clase_2.set_v_center([6.8,3.4,4.6,0.7])

    kmedias = KMeans(4)

    kmedias.add_label(clase_1)
    kmedias.add_label(clase_2)

    #read file 
    f = open("../data/Iris2Clases.txt","r")
    lines = f.readlines()
    f.close()

    #create U
    matrix = generate_random_U(len(lines),2)
    kmedias.set_U(matrix)

    #add vectors
    for line in lines:
        new_vector = line.strip("\n").split(",")
        new_vector = list(map(float, new_vector[:-1]))
        kmedias.add_vector(new_vector)

    kmedias.train(epsilon=0.01,b=2)

    print(kmedias.get_distances_from_new_example([5.1,3.5,1.4,0.2]))
    print("-" *50)

    print(kmedias.get_distances_from_new_example([6.9,3.1,4.9,1.5]))
    print("-" *50)

    print(kmedias.get_distances_from_new_example([5.1,3.5,1.4,0.2]))
