
def dup_arr(arr):
    i = 0
    while i < len(arr):
        arr.insert(i+1, arr[i])
        i += 2

#Считаем полином Ньютона, по заданному аргументу, точкам "разделенной разности"
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

def div_diff_count_ermit(dots, tab_x, tab_y, tab_y1):
    if (len(dots) == 1):
        #print(tab_y[dots[0]])
        return tab_y[dots[0]]

    if (len(dots) == 2):
        if (tab_y[dots[0]] == tab_y[dots[1]]):
            return tab_y1[dots[0]]

    a1 = ((div_diff_count_ermit(dots[:len(dots) - 1], tab_x, tab_y, tab_y1)
        - div_diff_count_ermit(dots[1:], tab_x, tab_y, tab_y1))
        / (tab_x[dots[0]] - tab_x[dots[len(dots) - 1]]))

    return a1

def div_diff_arr_ermit(dots, tab_x, tab_y, tab_y1):
    dd_arr = []

    for i in range(len(dots)):
        a = div_diff_count_ermit(dots[0:i+1], tab_x, tab_y, tab_y1)
        dd_arr.append(a)

    return dd_arr

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
#Возвращаем массив, содержащий точки "разделенной разности", по которым считается полином Ньютона
def div_diff_arr(dots, tab_x, tab_y):
    dd_arr = []

    for i in range(len(dots)):
        a = div_diff_count(dots[0:i+1], tab_x, tab_y)
        dd_arr.append(a)

    return dd_arr

#Выбираем точки в таблицы, расположенные "вокруг" заданной точки
#Возвращаем массив индексов таких точек
def choose_dots(x, table_x, n):
    center = -1
    for i in range(len(table_x)):
        if x - table_x[i] <= 0:
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
        if center + ir < len(table_x):
            l.append(center + ir)
            n_copy -= 1

        il += 1
        ir += 1

    l.sort()

    return l

def main():
    #инициализация
    #table_x = [ -0.50, -0.25, 0.0, 0.25, 0.50, 0.75, 1.0 ]
    #table_y = [ 0.707, 0.924, 1.0, 0.924, 0.707, 0.383, 0 ]

    table_x = [ 0.0, 0.15, 0.30, 0.45, 0.60, 0.75, 0.90, 1.05 ]
    table_y = [ 1.000000, 0.838771, 0.655336, 0.450447, 0.225336, -0.018310, -0.278390, -0.552430 ]
    table_y1 = [ -1.000000, -1.14944, -1.29552, -1.43497, -1.56464, -1.68164, -1.78333, -1.86742 ]

    #n = int(input('Введите степень полинома Ньютона: '))
    n = 2
    #тут еще Эрмит

    #x = float(input('Введите значение аргумента: '))
    x = 0.525

    #Полином Ньютона
    dots = choose_dots(x, table_x, n)
    #print(dots)
    values = div_diff_arr(dots, table_x, table_y)
    #print(values)
    res = inter_newton(x, values, table_x, dots)
    print(f'Значение функции в {x} по полиному Ньютона:', round(res, 3))

    #Обратная интерполяция
    y = 0
    n = 2
    dots = choose_dots(y, table_y, n)
    values = div_diff_arr(dots, table_y, table_x)
    res = inter_newton(y, values, table_y, dots)
    print('Корень заданной функции по обратной интерполяции:', round(res, 3))

    #Полином Эрмита
    dup_arr(table_x)
    dup_arr(table_y)
    dup_arr(table_y1)

    dots = choose_dots(x, table_x, n)
    #print(dots)
    values = div_diff_arr_ermit(dots, table_x, table_y, table_y1)
    #print(values)
    res = inter_newton(x, values, table_x, dots)
    print(f'Значение функции в {x} по полиному Эрмита:', round(res, 3))




if __name__ == "__main__":
    main()
