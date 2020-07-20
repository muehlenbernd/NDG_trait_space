import math
import random
import numpy as np

def approximation_step(coor1, coor2, step_sizes):


    new_coordinates = []

    for index in range(len(coor1)):

        distance = coor2[index] * 1.0 - coor1[index]
        new_coordinates.append(coor1[index]*1.0 + distance * step_sizes[index])

    return new_coordinates



def euc_distance(coor1, coor2):

    dimension = len(coor1)

    sum_of_square_distances = 0.0

    for index in range(dimension):
        sum_of_square_distances += (coor1[index]-coor2[index])*(coor1[index]-coor2[index])

    distance = math.sqrt(sum_of_square_distances)


    return distance


def normal_distribution(mean, sdev):

    x = np.random.normal(mean, sdev)

    x = max(x, 0.0)

    x = min(x,1.0)

    return x
