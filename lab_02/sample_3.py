#Копирование каждого элемента массива 1 раз: [1, 2] -> [1, 1, 2, 2]
def dup_arr(arr):
    i = 0
    while i < len(arr):
        arr.insert(i+1, arr[i])
        i += 2

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

    nn = 2
    x = 0.525

    #Полином Ньютона
    newton = []
    for i in range(1, 6):
        n = i
        dots = choose_dots(x, table_x, n)
        #print(dots)
        values = div_diff_arr(dots, table_x, table_y)
        #print(values)
        res = inter_newton(x, values, table_x, dots)
        if n == nn:
            print(f'Значение функции в {x} по полиному Ньютона:', round(res, 3))
        newton.append(res)

if __name__ == "__main__":
    main()