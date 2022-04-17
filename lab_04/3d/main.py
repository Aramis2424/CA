from numpy import arange
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from numpy import linspace


class Point:
    def __init__(self, x=0, y=0, z=0, weight=1):
        self.x = x
        self.y = y
        self.z = z
        self.weight = weight


def print_table(table):
    print("----------------------------------------------------")
    print("|      X    |      Y     |     Z      |   weight   |")
    print("|--------------------------------------------------|")
    for i in range(len(table)):
        print( f"|{table[i].x:^10.2f} | {table[i].y:^10.2f} |"+\
               f" {table[i].z:^10.2f} | {table[i].weight:^10.2f} |")
    print("----------------------------------------------------")


def read_dots(file_input):
    dots = list()
    with open(file_input, "r") as f:
        line = f.readline()
        while line:
            x, y, z, weight = map(float, line.split())
            dots.append(Point(x, y, z, weight))
            line = f.readline()
    return dots


def find_slae_matrix_3d(dots, n):
    rn = 0
    for i in range(0, n + 1):
        rn += i + 1
    res = [[0 for i in range(0, rn)] for j in range(0, rn)]
    col = [0 for i in range(0, rn)]
    v = 0
    for i in range(0, n + 1):
        for j in range(0, i + 1):
            for h in range(len(dots)):
                c = 0
                for k in range(0, n + 1):
                    for l in range(0, k + 1):
                        coef = dots[h].weight * dots[h].x ** (i - j) *\
                                dots[h].y ** j
                        res[v][c] += coef * dots[h].x ** (k - l) *\
                                dots[h].y ** l
                        c += 1
                col[v] += coef * dots[h].z
            v += 1

    for i in range(len(col)):
        res[i].append(col[i])
    return res


# Функция метод Гаусса
def method_gauss(matrix):
    n = len(matrix)
    for k in range(n):
        for i in range(k + 1, n):
            if matrix[k][k] == 0:
                continue
            coeff = -(matrix[i][k] / matrix[k][k])
            for j in range(k, n + 1):
                matrix[i][j] += coeff * matrix[k][j]
    a = [0 for i in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            matrix[i][n] -= a[j] * matrix[i][j]
        if matrix[i][i] == 0:
            continue
        a[i] = matrix[i][n] / matrix[i][i]
    return a


def draw_plot(coeffs, degree, points, n):
    table_x = [points[i].x for i in range(len(points))]
    table_y = [points[i].y for i in range(len(points))]
    table_z = [points[i].z for i in range(len(points))]

    x = list(linspace(min(table_x), max(table_x), 20))
    y = list(linspace(min(table_y), max(table_y), 20))

    fig = figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.scatter(table_x, table_y, table_z)

    res_x = []
    res_y = []
    res_z = []
    for elx in x:
        for ely in y:
            elz = 0
            i = 0
            for k in range(0, degree + 1):
                for l in range(0, k + 1):
                    elz += coeffs[i] * elx ** (k - l) * ely ** l
                    i += 1
            res_x.append(elx)
            res_y.append(ely)
            res_z.append(elz)

    ax.plot_trisurf(res_x, res_y, res_z, color='green', alpha=0.4)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.ylabel('Z')

    plt.grid()


# 7 dots
def main():
    deg_arr = [1, 2]
    filename = 'input3.txt'

    points = read_dots(filename)
    print_table(points)

    for i in range(2):
        degree = deg_arr[i]

        slae_matrix = find_slae_matrix_3d(points, degree)
        coeffs = method_gauss(slae_matrix)
        print(coeffs)

        draw_plot(coeffs, degree, points, i+1)
    plt.show()

if __name__ == "__main__":
    main()
