from numpy.polynomial.legendre import leggauss
from numpy import arange, linspace, ndarray
import matplotlib.pyplot as plt
from math import pi, cos, sin, exp, sqrt

def func(x, y):
    return sqrt(x * x + y * y)

def Func(F, y):
    return lambda x: F(x, y)

def g_func(y):
    return 1 - sqrt(1 - y * y), 1 + sqrt(1 - y * y)

def simpson(F, a, b, num):
    if (num < 3 or num & 1 == 0):
        raise ValueError

    h = (b - a) / (num - 1)
    x = a
    res = 0

    for i in range((num - 1) // 2):
        res += F(x) + 4 * F(x + h) + F(x + 2 * h)
        x += 2 * h
    
    return res * (h / 3)


def t_x(t, a, b):
    return (b + a) / 2 + (b - a) * t / 2


def gauss(F, a, b, num):
    args, coefs = leggauss(num)
    res = 0

    for i in range(num):
        res += (b - a) / 2 * coefs[i] * F(t_x(args[i], a, b))

    return res

def solution(hy, hx):
    y_arr = list(linspace(-1, 1, hy))
    x_arr = []
    for y in y_arr:
        xa, xb = g_func(y)
        Fx = Func(func, y)
        x_arr.append(gauss(Fx, xa, xb, hx))
    return y_arr, x_arr

def main():
    ny = 55
    nx = 10
    y_arr, Fy_arr = solution(ny, nx)
    # print(len(y_arr), ' ', len(Fy_arr))
    def f(x, x_arr, y_arr):
        i = 0
        while (i < len(x_arr) and abs(x_arr[i] - x) > 1e-6):
            i += 1
        return y_arr[i]
    Fy = lambda x: f(x, y_arr, Fy_arr)
    res = simpson(Fy, -1, 1, ny)
    print(res)
main()