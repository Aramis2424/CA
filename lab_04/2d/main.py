from numpy import arange
import matplotlib.pyplot as plt
import pylab


class Point:
    def __init__(self, x, y, weight):
        self.x = x
        self.y = y
        self.weight = weight


def print_table(table):
    print("---------------------------------------")
    print("|      X    |      Y     |   weight   |")
    print("|-------------------------------------|")
    for i in range(len(table)):
        print(f"|{table[i].x:^10.2f} | {table[i].y:^10.2f} |"+\
              f" {table[i].weight:^10.2f} |")
    print("---------------------------------------")
    print()


# Возвращает массив точек из структур(x, y, вес)
def read_from_file(file_input):
    dots = list()
    with open(file_input, "r") as f:
        line = f.readline()
        while line:
            x, y, weight = map(float, line.split())
            dots.append(Point(x, y, weight))
            line = f.readline()
    return dots


def append_right_side(matrix, dots):
    for i in range(len(matrix)):
        res = 0
        for j in range(len(dots)):
            res += dots[j].weight * dots[j].y * (dots[j].x ** i) # ф-ла (6)
        matrix[i].append(res)


# Находим коэффициент
def get_coef(dots, degree):
    coefficient = 0
    for i in range(len(dots)):
        coefficient += dots[i].weight * (dots[i].x ** degree)
    return coefficient


def find_slae_matrix(dots, degree):
    matrix = [[get_coef(dots, j + i)  # получится degree * 2
              for i in range(degree + 1)]
              for j in range(degree + 1)]
    print(matrix)
    append_right_side(matrix, dots)
    print('\n',matrix)
    return matrix


def get_polynomial_coefficients(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i == j:
                continue
            multiplication = matrix[j][i] / matrix[i][i]
            for k in range(0, len(matrix) + 1):
                matrix[j][k] -= multiplication * matrix[i][k]

    for i in range(len(matrix)):
        multiplication = matrix[i][i]
        for j in range(len(matrix[i])):
            matrix[i][j] /= multiplication

    # Последний элемент каждой строки
    return [matrix[i][-1] for i in range(len(matrix))]


# Добаляем график для каждого полинома
def add_plot(coeffs, label, start, end, n):
    pylab.subplot (1, 2, n)

    list_x = []
    list_y = []
    step = (end - start) / 1000

    for x in arange(start, end + step, step):
        list_x.append(x)
        y = 0
        for k in range(len(coeffs)):
            y += coeffs[k] * x ** k # Считаем у по ф-ле (3) (yk = x**k)
        list_y.append(y)

    plt.plot(list_x, list_y, label=label)

    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid()


def add_table(table, label, n):  # Рисуем точки на графики в мпл
    pylab.subplot (1, 2, n)
    table_x = [table[i].x for i in range(len(table))]
    table_y = [table[i].y for i in range(len(table))]

    plt.plot(table_x, table_y, 'o', label=label)


def main():
    filename = 'input.txt'

    degrees = [1, 2, 7] # Ввод степеней различных полиномов

    for k in range(1, 3): # Делаем для двух файлов
        filename = f'input{k}.txt'
        points = read_from_file(filename) # Массив точек
        add_table(points, "dots", k) # Рисуем точки на графике
        print_table(points)

        for i in range(len(degrees)): # По кол-ву введеных полиномов
            slae_matrix = find_slae_matrix(points, degrees[i]) # Находим СЛАУ
            coeffs = get_polynomial_coefficients(slae_matrix) # Находим коэф-ты
            add_plot(coeffs, f"n = {degrees[i]}", # Рисуем полином на графике
                     points[0].x, points[-1].x, k)

    plt.show()


if __name__ == "__main__":
    main()








##    filenames = input("Enter filenames: ").split()
##    label = input("Enter labels: ").split(',')

##    degrees = list(map(int, input("Enter polynomial degree: ").split()))

##    for i in range(1, 3):
##        filename = f'input{i}.txt'
##        points = read_from_file(filename)
##        add_table(points, "Table", i)
##        print_table(points)
##        for i in range(len(degrees)):
##            slae_matrix = find_slae_matrix(points, degrees[i])
##            coeffs = get_polynomial_coefficients(slae_matrix)
##            add_plot(coeffs, f"n = {degrees[i]}",
##                     points[0].x, points[-1].x, i)
##
##
##def print_arr(arr):
##    for elem in arr:
##        print(round(elem, 3), end = '  ')
##    print()
