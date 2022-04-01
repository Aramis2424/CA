from sympy import diff, Symbol

#Копирование каждого элемента массива 1 раз: [1, 2] -> [1, 1, 2, 2]
def dup_arr(arr):
    i = 0
    while i < len(arr):
        arr.insert(i+1, arr[i])
        i += 2

#Считаем полином, по заданному аргументу, точкам "разделенной разности"
#и известным значениям "х"
def inter_newton(x, val, tab_x, dots):
    # x - это то, что ввели
    # val - значения из верхней строки таблицы
    # tab_x - это то, что имелось изначально [, 0.25, 0.50, 0.75, 1.0]
    # dots - это индексы ближайших точек

    sub_x = 1
    res = 0

    sres = ''
    ssub_x = ''

    k = 1
    for i in range(len(val)):
        while i - k >= 0:
            sub_x *= (x - tab_x[dots[i-k]]) # x - 0,25 ...

            if str(round(tab_x[dots[i-k]], 3)) == '0.0':
                ssub_x += 'x' + '*'
            else:
                if '-' in str(tab_x[dots[i-k]]):
                    new_str = str(round(tab_x[dots[i-k]], 3)).replace('-', '+')
                    ssub_x += '(' + 'x' + new_str + ')' + '*'
                else:
                    ssub_x += '(' + 'x' + '-' +\
                            str(round(tab_x[dots[i-k]], 3)) + ')' + '*'
            k += 1

        #print(sub_x)
        if (ssub_x and ssub_x[-1] == '*'):
            ssub_x = ssub_x[0:-1:1]

        res += (val[i] * sub_x) # 1,128*(x-0,25)
        if ssub_x == '':
            sres += str(round(val[i], 3)) + '+'
        else:
            if '-' in str(round(val[i], 3)):
                sres = sres[0:-1:1]
            sres += str(round(val[i], 3)) + '*' + ssub_x + '+'

        sub_x = 1
        ssub_x = ''
        k = 1

    sres = sres[0:-1:1]
##    if (sres[-1] == '*'):
##        sres = sres[0:-1:1]
    print(sres)
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
    table_x = [ -0.50, -0.25, 0.0, 0.25, 0.50, 0.75, 1.0 ]
    table_y = [ 0.707, 0.924, 1.0, 0.924, 0.707, 0.383, 0 ]

    nn = 2
    x = 0.6


    #Полином Ньютона
    n = nn
    dots = choose_dots(x, table_x, n)
    #print(dots)
    values = div_diff_arr(dots, table_x, table_y)
    #print(values)
    res = inter_newton(x, values, table_x, dots)

    print(res)


if __name__ == "__main__":
    x = Symbol('x')
    print(diff(0.707-1.296*(x-0.5)-0.472*(x-0.75)*(x-0.5)))
    exit()
    main()
