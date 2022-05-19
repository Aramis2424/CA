from numpy.polynomial.legendre import leggauss
from numpy import arange
import matplotlib.pyplot as plt
from math import pi, cos, sin, exp

def main_func(tao):
    subfunc = lambda x, y: 2 * cos(x) / (1 - (sin(x) ** 2) * (cos(y) ** 2))
    func = lambda x, y: (4 / pi) * (1 - exp(-tao * subfunc(x, y))) * cos(x) * sin(x)
    return func


def F2_1(F2, val):
    return lambda x: F2(val, x)


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


def graph_for_tao(F, arg, label):
    x = list()
    y = list()
    for tao in arange(arg[0], arg[1] + arg[2], arg[2]):
        x.append(tao)
        y.append(F(tao))
    plt.plot(x, y, label=label)


def integr_2(F, limit, num, integr):
    first = lambda x: integr[1](F2_1(F, x), limit[1][0],
                                limit[1][1], num[1])
    res = integr[0](first, limit[0][0], limit[0][1], num[0])
    return res

def main():
    all_ = False
    while not all_:
        n = int(input("Input N (integer): "))
        m = int(input("Input M (integer): "))
        tao = float(input("Input tao: "))
        flag = bool(int(input("Input first method (0 - Simpson, 1 - Gauss): ")))
        F1 = gauss if flag else simpson
        flag = bool(int(input("Input first method (0 - Simpson, 1 - Gauss): ")))
        F2 = gauss if flag else simpson

        param = lambda tao:integr_2(main_func(tao),
                                    [[0, pi/2], [0, pi/2]],
                                    [n, m], [F1, F2])

        try:
            label = "n = " + str(n) + ", m = " + str(m)
            label += "  S" if F1 == simpson else "  G"
            label += " - S" if F2 == simpson else " - G"
            graph_for_tao(param, [0.05, 10, 0.05], label)
        except ValueError:
            print("Error with method Simpson (arg > 2)")
        except ZeroDivisionError:
            print("Can not use Simpson-Simpson")
        all_ = bool(int(input("Is it all? (0 - No, 1 - Yes): ")))

    plt.legend()
    plt.ylabel("Result")
    plt.xlabel("Tao value")
    plt.show()

main()