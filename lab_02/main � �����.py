#Функция
def f(x, y, z):
    return x**2 + y**2 + z**2

#Считаем полином, по заданному аргументу, точкам "разделенной разности"
#и известным значениям "х"
def inter_newton(x, val, tab_x, dots):
    sub_x = 1
    res = 0

    k = 1
    for i in range(len(val)):
        while i - k >= 0:
            sub_x *= (x - tab_x[dots[i-k]])
            k += 1

        res += (val[i] * sub_x)
        sub_x = 1
        k = 1

    return res

#Рекурсивно считаем разделенную разность
def div_diff_count(dots, tab_x, tab_y):
    if (len(dots) == 1):
        #print(tab_y[dots[0]])
        return tab_y[dots[0]]

    a1 = ((div_diff_count(dots[:len(dots) - 1], tab_x, tab_y)
        - div_diff_count(dots[1:], tab_x, tab_y))
        / (tab_x[dots[0]] - tab_x[dots[len(dots) - 1]]))

    return a1

#Формируем массив точек, на основе которых нужно посчитать разделенную разность
#Возвращаем массив, содержащий точки "разделенной разности",
#по которым считается полином Ньютона
def div_diff_arr(dots, tab_x, tab_y):
    dd_arr = []

    for i in range(len(dots)):
        a = div_diff_count(dots[0:i+1], tab_x, tab_y)
        dd_arr.append(a)

    return dd_arr

#Выбираем точки в таблицы, расположенные "вокруг" заданной точки
#Возвращаем массив индексов таких точек
def choose_dots(arg, table, n):
    center = -1
    for i in range(len(table)):
        if arg - i <= 0:
            center = i
            break

    if center < 0:
        print('Точка за пределами таблицы')

    l = [center]
    n_copy = n - 1
    il = 1
    ir = 1

    while n_copy >= 0:

        if center - il >= 0:
            l.append(center - il)
            n_copy -= 1
            if n_copy < 0:
                break
        if center + ir < len(table):
            l.append(center + ir)
            n_copy -= 1

        il += 1
        ir += 1

    l.sort()

    return l


def main():
    #инициализация
    n = 5
    matr = []
    arr_x = []
    matr_xy = []
    for z in range(n):
        for y in range(n):
            for x in range(n):
                arr_x.append(f(x, y, z))
            arr_x_copy = arr_x.copy()
            matr_xy.append(arr_x_copy)
            arr_x.clear()
        matr_xy_copy = matr_xy.copy()
        matr.append(matr_xy_copy)
        matr_xy.clear()

    #n_x = int(input('Введите степень полинома Ньютона для x: '))
    #x = float(input('Введите значение x: '))
    x = 0.5
    n_x = 3
    #n_y = int(input('Введите степень полинома Ньютона для y: '))
    #y = float(input('Введите значение y: '))
    y = 2.5
    n_y = 2
    #n_z = int(input('Введите степень полинома Ньютона для z: '))
    #z = float(input('Введите значение z: '))
    z = 3.5
    n_z = 3
##    print(matr[2][3][4])
##    return 0

##    table_x = [  0, 1, 2, 3, 4 ]
##    table_y = [  0, 1, 2, 3, 4 ]

    #nn = int(input('Введите степень полинома Ньютона: '))
    nn = 2
    #x = float(input('Введите значение аргумента: '))
    x = 0.5

    #Интерполяция
    dots_z = choose_dots(z, matr, n_z)
    dots_y = choose_dots(y, matr, n_y)
    dots_x = choose_dots(x, matr, n_x)
    print(dots_z)
    print(dots_y)
    print(dots_x)
    ##values = div_diff_arr(dots, table_x, table_y)
    #print(values)
    ##res = inter_newton(x, values, table_x, dots)
    ##print(f'Значение функции в {x} по полиному Ньютона:', round(res, 3))

if __name__ == "__main__":
    main()
