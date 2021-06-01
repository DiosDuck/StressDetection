import numpy as np
import math
import ast

class Scale:
    def fit(self,array):
        self.__mean=[]
        self.__standard_derivation=[]
        aux=array.tolist()
        for i in range(len(aux[0])):
            #mean
            mean=0
            for x in aux:
                mean+=x[i]
            mean=mean/len(aux)

            #standard_deviation
            standard_deviation=0
            for x in aux:
                standard_deviation+=(x[i]-mean)*(x[i]-mean)
            standard_deviation=math.sqrt(standard_deviation/len(aux))
            self.__mean.append(mean)
            self.__standard_derivation.append(standard_deviation)

    def transform(self,array):
        rez=[]
        aux=array.tolist()
        for x in aux:
            mini=[]
            for i in range(len(x)):
                mini.append((x[i]-self.__mean[i])/self.__standard_derivation[i])
            rez.append(mini)
        return np.array(rez)

    def prebuild(self,file_name):
        f=open(file_name,"r")
        self.__mean=ast.literal_eval(f.readline().strip("\n"))
        self.__standard_derivation=ast.literal_eval(f.readline().strip("\n"))
        f.close()

    def save(self,file_name):
        f=open(file_name,"w")
        f.write(str(self.__mean)+"\n")
        f.write(str(self.__standard_derivation)+"\n")
        f.close()