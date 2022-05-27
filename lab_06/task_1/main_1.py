from math import sqrt
from numpy.polynomial.legendre import leggauss


# Функция f(t) - степень черноты полупрозрачного однородного по объему цилиндра
#с большим отношением длины к радиусу
def f():
    main_func = lambda x, y: sqrt(x**2 + y**2)
    return main_func


def g_func(y):
    return 1 - sqrt(1 - y * y), 1 + sqrt(1 - y * y)


# Конвертация функции с двумя переменными в функцию с одной переменной
#(вторая переменная считается константой)
def to_single_temp(f, value):
    return lambda y: f(value, y)


# Преобразование переменной t в x, [a;b] - интервал интегрирования
def convert_t_to_x(t, a, b):
    return (b + a) / 2 + (b - a) * t / 2


# Метод интегрирования, использующий формулу Симпсона
def simpson(func, a, b, degree):
    if degree < 3 or degree % 2 == 0:
        print("Неверные данные для Симпсона")
        exit(-1)
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


def main():
##    N = int(input("Введите N для внешней функции: "))
##    M = int(input("Введите M для внутренней функции: "))
##
##    t = float(input("Введите параметр t: "))

##    external_method = gauss if (int(input("Внешняя функция:\n1) Функция Гаусса\n"
##                      "2) Функция Симпсона\n\Ваш выбор: ")) == 1) else simpson
##    internal_method = gauss if (int(input("Внутренняя функция:\n1) Функция Гаусса\n"
##                      "2) Функция Симпсона\nВаш выбор: ")) == 1) else simpson

    N = 10
    M = 55
    external_method = gauss
    internal_method = simpson

    res = lambda: integrate_2_dims(f(), [[0, 2], [-1, 1]],
        [N, M], [external_method, internal_method])

    print("Интеграл I = ", round(res(), 3), sep="")

if __name__ == "__main__":
    main()
