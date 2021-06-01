from random import uniform
from sklearn.metrics import confusion_matrix

import numpy as np
import ast

def vector_product(arr1, arr2):
    if len(arr1) != len(arr2):
        print("LUNGIMILE NU SE POTRIVESC")

    return [x * y for x, y in zip(arr1, arr2)]

def cubic_diff(cube1, cube2):
    new_cube = []
    for i in range(len(cube1)):
        arri = []
        for j in range(len(cube1[i])):
            arrj = []
            for k in range(len(cube1[i][j])):
                arrj.append(cube1[i][j][k] - cube2[i][j][k])
            arri.append(arrj)
        new_cube.append(arri)
    return new_cube


def cubic_multi(real_value, cube1):
    new_cube = []
    for i in range(len(cube1)):
        arri = []
        for j in range(len(cube1[i])):
            arrj = []
            for k in range(len(cube1[i][j])):
                arrj.append(cube1[i][j][k] * real_value)
            arri.append(arrj)
        new_cube.append(arri)
    return new_cube


def matrix_add(matrix1, matrix2):
    new_matrix = []
    for i in range(len(matrix1)):
        arr = []
        for j in range(len(matrix1[0])):
            arr.append(matrix1[i][j] + matrix2[i][j])
        new_matrix.append(arr)
    return new_matrix


def v_minus(arr1, arr2):
    return [(x - y) for x, y in zip(arr1, arr2)]


def v_scalar_minus(real_value, arr):
    new_arr = [real_value for _ in range(len(arr))]
    return v_minus(new_arr, arr)

def single_column(arr):
    return [[el] for el in arr]


def single_line(arr):
    return [el[0] for el in arr]


def transpose(matrix):
    new_matrix = []
    rows = len(matrix)
    cols = len(matrix[0])
    for col in range(cols):
        new_matrix.append([])
        for row in range(rows):
            new_matrix[col].append(matrix[row][col])
    return new_matrix


def to_line_of_line(param):
    new_list = [param]
    return new_list

def matrix_product(matrix_one, matrix_two):
    n = len(matrix_one)
    m = len(matrix_one[0])
    p = len(matrix_two[0])
    res = [[0 for _ in range(p)] for _ in range(n)]
    for i in range(n):
        for j in range(p):
            for k in range(m):
                res[i][j] += matrix_one[i][k] * matrix_two[k][j]
    return res


def sygmoid(x):
    if x == 0:
        return 0
    minu = -x
    ex = np.exp(minu)
    denom = 1.0 + ex
    return 1.0 / denom


def v_sygmoid(sample):
    sol = []
    for value in sample:
        res = sygmoid(value)
        sol.append(res)
    return sol


def copy_arr(arr1, arr2):
    for idx in range(len(arr2)):
        arr1[idx] = arr2[idx]


class ANN:
    def prebuild(self,file):
        # file
        self.__file = file
        f=open(file,"r")
        #no_features
        f.readline()
        self.__no_features=int(f.readline().strip('\n'))
        # no_targets
        f.readline()
        self.__no_targets = int(f.readline().strip('\n'))
        # no_hidden_layers
        f.readline()
        self.__no_hidden_layers = int(f.readline().strip('\n'))
        # length_of_hidden_layer
        f.readline()
        self.__length_of_hidden_layer = int(f.readline().strip('\n'))
        # no_layers
        f.readline()
        self.__no_layers = int(f.readline().strip('\n'))
        # training_epochs
        f.readline()
        self.__training_epochs = int(f.readline().strip('\n'))
        #weights
        f.readline()
        f.readline()
        s=f.readline().strip('\n')
        self.__weights=[]
        while s!=']':
            self.__weights.append(ast.literal_eval(s))
            s=f.readline().strip('\n')
        #activation
        f.readline()
        f.readline()
        s = f.readline().strip('\n')
        self.__activation = []
        while s != ']':
            self.__activation.append(ast.literal_eval(s))
            s = f.readline().strip('\n')
        #gradient
        f.readline()
        f.readline()
        s = f.readline().strip('\n')
        self.__gradient = []
        while s != ']':
            self.__gradient.append(ast.literal_eval(s))
            s = f.readline().strip('\n')
        #learning_rate
        f.readline()
        self.__learning_rate = float(f.readline().strip('\n'))
        #label
        f.readline()
        self.__label=ast.literal_eval(f.readline().strip('\n'))
        #acc
        f.readline()
        self.__best=float(f.readline().strip('\n'))
        f.close()

    def fit2(self, input_data, desired_outputs,test_input,test_output):
        for i in range(self.__training_epochs):
            print("Epoche: ", i)
            for sample, desired in zip(input_data, desired_outputs):
                self.__forward_propagation(sample)
                self.__backpropagation(desired)
                self.__update_gradients()
            self.__update_weights(len(input_data))
            acc = self.predict(test_input,test_output)
            print("ACC/BEST: " + str(acc) + " / " + str(self.__best))
            if acc >= self.__best:
                self.__best = acc
                self.__write_to_file()

    def predict(self,input,output):
        predict_output = []
        for j in input:
            predict_output.append(self.eval(j))
        confMatrix = confusion_matrix(output, predict_output)
        return sum([confMatrix[i][i] for i in range(len(self.__label))]) / len(output) * 100

    def fit(self, input_data, desired_outputs, label,test_input,test_output):
        self.__label = label
        for i in range(self.__training_epochs):
            print("Epoche: ", i)
            for sample, desired in zip(input_data, desired_outputs):
                self.__forward_propagation(sample)
                self.__backpropagation(desired)
                self.__update_gradients()
            self.__update_weights(len(input_data))
            acc = self.predict(test_input,test_output)
            print("ACC/BEST: " +str(acc)+" / "+str(self.__best))
            if acc>=self.__best:
                self.__best=acc
                self.__write_to_file()

    def __write_to_file(self):
        f=open(self.__file,"w")
        f.write("no_features\n"+str(self.__no_features)+"\n")
        f.write("no_targets\n"+str(self.__no_targets)+"\n")
        f.write("no_hidden_layers\n"+str(self.__no_hidden_layers)+"\n")
        f.write("length_of_hidden_layer\n"+str(self.__length_of_hidden_layer)+"\n")
        f.write("no_layers\n"+str(self.__no_layers)+"\n")
        f.write("training_epochs\n"+str(self.__training_epochs)+"\n")
        f.write("weights\n[")
        for w in self.__weights:
            f.write("\n"+str(w))
        f.write("\n]\n")
        f.write("activation\n[")
        for a in self.__activation:
            f.write("\n" + str(a))
        f.write("\n]\n")
        f.write("gradient\n[")
        for g in self.__gradient:
            f.write("\n" + str(g))
        f.write("\n]\n")
        f.write("learning_rate\n"+str(self.__learning_rate)+"\n")
        f.write("label\n"+str(self.__label)+"\n")
        f.write("acc\n"+str(self.__best)+"\n")
        f.close()

    def __update_weights(self, no_samples):
        #weight[i]=weight[i]-grandiend[i]/(no_samples*leanring_rate)
        final_gradient = cubic_multi(1 / no_samples * self.__learning_rate, self.__gradient)
        self.__weights = cubic_diff(self.__weights, final_gradient)

    def __update_gradients(self):
        self.__deltas.reverse()
        for layer_idx in range(self.__no_layers - 1):
            #grandient[i]=delta[i]T*input[i]+grandiend[i]
            mat_product = matrix_product(single_column(self.__deltas[layer_idx]),
                                         to_line_of_line(self.__activation[layer_idx]))
            self.__gradient[layer_idx] = matrix_add(self.__gradient[layer_idx], mat_product)

    def __backpropagation(self, desired):
        #delta va mentine erroarea pt fiecare layer
        self.__deltas = []
        delta = self.__compute_error_for_backpropagation(desired)
        self.__deltas.append(delta)
        for layer_idx in range(self.__no_layers - 2, 0, -1):
            #delta[i]=weight[i]T*delta[i+1]*input[i]*(1-input[i])
            first_computation = single_line(matrix_product(transpose(self.__weights[layer_idx]),
                                                           single_column(self.__deltas[-1])))
            second_computation = vector_product(first_computation, self.__activation[layer_idx])
            third_computation = vector_product(second_computation,
                                               v_scalar_minus(1, self.__activation[layer_idx]))
            self.__deltas.append(third_computation)

    def __compute_error_for_backpropagation(self, desired_output):
        #take the output
        plus_layer = []
        for value in self.__activation[-1]:
            plus_layer.append(np.exp(value))
        #softmax
        total_sum = sum(plus_layer)
        soft_max_new_error = [curr / total_sum for curr in plus_layer]
        #get error
        error = []
        for idx in range(len(soft_max_new_error)):
            #error = softamx daca nu e output-ul dorit
            #altfel error = softmax-1
            if self.__label[idx] == desired_output:
                curr_error = soft_max_new_error[idx] - 1
            else:
                curr_error = soft_max_new_error[idx] - 0
            error.append(curr_error)
        return error

    def __put_data_in_first_layer(self, sample):
        # pregatire date
        for idx in range(len(sample)):
            self.__activation[0][idx] = sample[idx]

    def __forward_propagation(self, sample):
        self.__put_data_in_first_layer(sample)
        for layer_idx in range(self.__no_layers - 1):
            # inmultesc greutatea (weights[layer_ind] contine
            # toate greutatile de pe acel layer
            solution = matrix_product(self.__weights[layer_idx],
                                      single_column(self.__activation[layer_idx]))
            # daca nu suntem pe penultimul layer=>sigmoid
            # altfel pregatim un softmax
            if (layer_idx + 1) != self.__no_layers - 1:
                copy_arr(self.__activation[layer_idx + 1], v_sygmoid(single_line(solution)))
            else:
                copy_arr(self.__activation[layer_idx + 1], single_line(solution))

    def eval(self, input):
        #eval care face softmax
        self.__forward_propagation(input)
        plus_layer = []
        for value in self.__activation[-1]:
            plus_layer.append(np.exp(value))
        total_sum = sum(plus_layer)
        soft_max_new_error = [curr / total_sum for curr in plus_layer]
        index = soft_max_new_error.index(max(soft_max_new_error))
        return self.__label[index]
