from numpy.polynomial.legendre import leggauss
from numpy import arange, linspace, ndarray
import matplotlib.pyplot as plt
from math import pi, cos, sin, exp, sqrt

def func(x, y): # функция интегрирования
    return sqrt(x * x + y * y)


# Конвертация функции с двумя переменными в функцию с одной переменной
#(вторая переменная считается константой)
def to_single_temp(f, value): # +++++++++++++
    return lambda y: f(value, y)


def g_func(y): # корень кривой G
    return 1 - sqrt(1 - y * y), 1 + sqrt(1 - y * y)


# Метод интегрирования, использующий формулу Симпсона
def simpson(func, a, b, degree): # +++++++++++++
    if degree < 3 or degree % 2 == 0:
        print("Неверные данные для Симпсона")
        exit(-1)

    h = (b - a) / (degree - 1)
    x = a
    res = 0

    for i in range((degree - 1) // 2):
        res += func(x) + 4 * func(x + h) + func(x + 2 * h)
        x += 2 * h

    return res * (h / 3)


# Преобразование переменной t в x, [a;b] - интервал интегрирования
def convert_t_to_x(t, a, b):  # +++++++++++++
    return (b + a) / 2 + (b - a) * t / 2


# Метод интегрирования, использующий формулу Гаусса
def gauss(func, a, b, degree):  # +++++++++++++
    args, coefs = leggauss(degree)
    res = 0
    for i in range(degree):
        res += (b - a) / 2 * coefs[i] * func(convert_t_to_x(args[i], a, b))
    return res


def solution(hy, hx, method):
    y_arr = list(linspace(-1, 1, hy))
    x_arr = []
    for y in y_arr:
        xa, xb = g_func(y)
        Fx = to_single_temp(func, y)
        if method == 1:
            x_arr.append(gauss(Fx, xa, xb, hx))
        else:
            x_arr.append(simpson(Fx, xa, xb, hx))

    return y_arr, x_arr


def f(x, x_arr, y_arr): # Возвращает f(x)
        i = 0
        min_sub = abs(x_arr[0] - x)
        cur_i = 0
        while (i < len(x_arr)):# and abs(x_arr[i] - x) > 1e-3):
            if abs(x_arr[i] - x) < min_sub:
                min_sub = abs(x_arr[i] - x)
                cur_i = i
            i += 1

        return y_arr[cur_i]


def main():
    nSim = 51
    nG = 50

    method = 0 # simpson - gauss = 0
               # gauss - simpson = 1

    if method == 1:
        ny = nSim
        nx = nG
    else:
        ny = nG
        nx = nSim

    y_arr, Fy_arr = solution(ny, nx, method)
    Fy = lambda x: f(x, y_arr, Fy_arr)

    if method == 1:
        res = simpson(Fy, -1, 1, ny)
    else:
        res = gauss(Fy, -1, 1, ny)
    print(round(res, 3))


if __name__ == "__main__":
    main()






##def Func(F, y): # ???
##    return lambda x: F(x, y)