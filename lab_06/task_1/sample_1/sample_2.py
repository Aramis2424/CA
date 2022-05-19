from math import cos, sin, pi, exp
from numpy.polynomial.legendre import leggauss
from numpy import arange
import matplotlib.pyplot as plt


# Функция f(t) - степень черноты полупрозрачного однородного по объему цилиндра
#с большим отношением длины к радиусу
def f(t):
    sub_func = lambda tetta, phi: 2 * cos(tetta) /\
        (1 - sin(tetta) ** 2 * cos(phi) ** 2)
    main_func = lambda tetta, phi: (4 / pi) *\
        (1 - exp(-t * sub_func(tetta, phi))) * cos(tetta) * sin(tetta)
    #print(tetta, phi)
    return main_func


# Конвертация функции с двумя переменными в функцию с одной переменной
#(вторая переменная считается константой)
def to_single_temp(f, value):
    return lambda y: f(value, y)


# Преобразование переменной t в x, [a;b] - интервал интегрирования
def convert_t_to_x(t, a, b):
    return (b + a) / 2 + (b - a) * t / 2


# Метод интегрирования, использующий формулу Симпсона
def simpson(func, a, b, degree):
    if degree < 3 or not degree % 2:
        raise ValueError
    h = (b - a) / (degree - 1)
    x = a
    result = 0
    for i in range((degree - 1) // 2):
        result += func(x) + 4 * func(x + h) + func(x + 2 * h)
        x += 2 * h
    result *= h / 3
    return result

# Метод интегрирования, использующий формулу Гаусса
def gauss(func, a, b, degree):
    args, coeffs = leggauss(degree)
    result = 0
    for i in range(degree):
        result += (b - a) / 2 * coeffs[i] * func(convert_t_to_x(args[i], a, b))
    return result


# Вычисление двукратного интеграла
# f - интегрируемая функция
# limits - пределы интегрирования для каждого из интегралов
#(внутреннего и внешнего)
# degrees - количество узлов для каждого из направлений интегрирования
# integrators - функции интегрирования(внешняя и внутренняя)
def integrate_2_dims(f, limits, degrees, integrators):
    # Интегрирование внутренней функции
    internal_func = lambda x: integrators[1](to_single_temp(f, x),
        limits[1][0], limits[1][1], degrees[1])
    # Интегрирование внешней функции
    return integrators[0](internal_func, limits[0][0], limits[0][1], degrees[0])


# Добавление информации о полученной функции на график
def graph(integrate_func, start, end, step, label):
    x = []
    y = []
    for t in arange(start, end + step, step):
        x.append(t)
        y.append(integrate_func(t))
    plt.plot(x, y, label=label)


cycle = True
while cycle:

    N = int(input("Введите N для внешней функции: "))
    M = int(input("Введите M для внутренней функции: "))

    t = float(input("Введите параметр t: "))

    external_method = gauss if (int(input("Внешняя функция:\n1) Функция Гаусса\n"
                      "2) Функция Симпсона\n\Ваш выбор: ")) == 1) else simpson
    internal_method = gauss if (int(input("Внутренняя функция:\n1) Функция Гаусса\n"
                      "2) Функция Симпсона\nВаш выбор: ")) == 1) else simpson

    res = lambda param: integrate_2_dims(f(param), [[0, pi/2], [0, pi/2]],
        [N, M], [external_method, internal_method])

    print("E(", t, ") = ", res(t), sep="")
    label = "N = " + str(N) + ", M = " + str(M) + ", "
    if external_method == gauss:
        label += "Gauss-Simpson"
    else:
        label += "Simpson-Gauss"
    graph(res, 0.05, 10, 0.05, label)

    cycle = int(input("Завершить работу?\n\n1) Да\n2) Нет\n\nВаш ответ: ")) - 1

plt.legend()
plt.ylabel("e(t)")
plt.xlabel("t")
plt.grid()
plt.show()