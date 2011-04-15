#!/usr/bin/env python
import multiply
import unittest


class TestMatrixMultiplication(unittest.TestCase):

    def test_zero_matrix_creation(self):
        """Tests the creation of a zero matrix"""
        matrix = multiply.zero_matrix(5, 4)
        rows = len(matrix)
        cols = len(matrix[0])
        self.assertEqual(rows, 5)
        self.assertEqual(cols, 4)
        for row in range(len(matrix)):
            self.assertEqual(matrix[row], [0, 0, 0, 0])

    def test_random_matrix_creation(self):
        """Tests the creation of a matrix filled with random values"""
        matrix = multiply.random_matrix(6, 4)
        rows = len(matrix)
        cols = len(matrix[0])
        self.assertEqual(rows, 6)
        self.assertEqual(cols, 4)

    def test_matrix_multiplication(self):
        """Test the multiplication of matrices"""
        m1 = [
                [1, 2, 3],
                [2, 4, 6]
        ]
        m2 = [
                [1, 2],
                [2, 4],
                [3, 6]
        ]
        correct_answer = [
                [14, 28],
                [28, 56]
        ]
        result = multiply.multiply(m1, m2)
        self.assertEqual(result, correct_answer)

    def test_wrong_dimensions(self):
        """Test if an exception is raised when matrices cannot be multiplied"""
        m1 = multiply.random_matrix(2, 3)
        m2 = multiply.random_matrix(4, 1)
        self.assertRaises(ValueError, multiply.multiply, m1, m2)


if __name__ == '__main__':
    unittest.main()
