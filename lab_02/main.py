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
def choose_dots(x, array, count):
    i = 0
    while i < len(array) and i < x:
        i += 1

    if i < count // 2 + 1:
        start, end = 0, count + 1
    elif i > len(array) - count:
        start, end = len(array) - count - 1, len(array)
    else:
        start = i - count // 2 - 1 if x != array[i] or count % 2 == 1 else i - count // 2
        end = i + count // 2 + 1 if count % 2 == 1 or x == array[i] else i + count // 2

    dots = [i for i in range(start, end)]
    return dots

def main():
    '''Инициализация'''
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
    #print(matr)

    #n_x = int(input('Введите степень полинома Ньютона для x: '))
    #x = float(input('Введите значение x: '))
    x = 3.5
    n_x = 3
    #n_y = int(input('Введите степень полинома Ньютона для y: '))
    #y = float(input('Введите значение y: '))
    y = 2.5
    n_y = 2
    #n_z = int(input('Введите степень полинома Ньютона для z: '))
    #z = float(input('Введите значение z: '))
    z = 3.5
    n_z = 3



    '''Интерполяция'''
    #Соседние точки
    dots_z = choose_dots(z, matr, n_z)
    dots_y = choose_dots(y, matr, n_y)
    dots_x = choose_dots(x, matr, n_z)

    kvazi_x = dots_x.copy()
    y_inter_tab = []
    z_inter_tab = []

    #Двумерная интерполяция
    for i in range(dots_z[0], dots_z[-1]+1):
        for j in range(dots_y[0], dots_y[-1]+1):
            kvazi_y = matr[i][j][dots_z[0]:dots_z[-1]+1]
            print(kvazi_x, kvazi_y)
            kvazi_dots = [i for i in kvazi_y]
            values = div_diff_arr(kvazi_dots, kvazi_x, kvazi_y)
            y_inter = inter_newton(x, values, kvazi_x, dots_x)
            y_inter_tab += [y_inter]
            #print(y_inter_tab)
        kvazi_x2 = dots_y.copy()
        kvazi_y2 = y_inter_tab.copy()
        kvazi_dots1 = [i for i in range(len(y_inter_tab))]
        values = div_diff_arr(kvazi_dots1, kvazi_x2, kvazi_y2)
        z_inter = inter_newton(y, values, kvazi_x2, dots_x)
        z_inter_tab += [z_inter]
        #print(z_inter_tab)
        y_inter_tab.clear()

    #Трехмерная интерполяция
    kvazi_x3 = dots_z.copy()
    kvazi_y3 = z_inter_tab.copy()
    kvazi_dots3 = [i for i in range(len(z_inter_tab))]
    values = div_diff_arr(kvazi_dots3, kvazi_x3, kvazi_y3)
    res = inter_newton(z, values, kvazi_x3, dots_x)

    print(f'Значение функции u = f{x, y, z} =', round(res, 3))

if __name__ == "__main__":
    main()
