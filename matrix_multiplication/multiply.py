#!/usr/bin/python
import random


def zero_matrix(m, n):
    """Creates a zero matrix of m x n dimension"""
    matrix = [[0 for column in range(n)] for row in range(m)]
    return matrix


def random_matrix(m, n):
    """Creates a matrix filled with random numbers, m x n dimension"""
    matrix = [[random.randint(-10, 10) for column in range(n)] for row in range(m)]
    return matrix


def multiply(m1, m2):
    """Multiplies two matrices"""
    if len(m1[0]) != len(m2):
        print "Matrices must be m x n and n x p to multiply them"
        raise ValueError

    result_matrix = zero_matrix(len(m1), len(m2[0]))
    for i in range(len(m1)):
        for j in range(len(m2[0])):
            for k in range(len(m2)):
                result_matrix[i][j] += m1[i][k] * m2[k][j]
    return result_matrix


def save_matrix_to_file(matrix, path):
    output_file = open(path, 'w')
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            output_file.write("%7i" % matrix[i][j])
        output_file.write("\n")


if __name__ == '__main__':
    m1 = random_matrix(6, 4)
    m2 = random_matrix(4, 7)
    result = multiply(m1, m2)
    save_matrix_to_file(result, 'matrix.txt')
