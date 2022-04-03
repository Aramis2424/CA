#Кубические сплайны


from sympy import Symbol, diff, lambdify


def inter_newton(x, val, tab_x, dots):
    sub_x = 1
    res = 0
    sres = ''
    ssub_x = ''

    k = 1
    for i in range(len(val)):
        while i - k >= 0:
            sub_x *= (x - tab_x[dots[i-k]]) # x - 0,25 ...

            if str(round(tab_x[dots[i-k]], 3)) == '0.0' or\
                str(round(tab_x[dots[i-k]], 3)) == '0':
                ssub_x += 'x' + '*'
            else:
                if '-' in str(tab_x[dots[i-k]]):
                    new_str = str(round(tab_x[dots[i-k]], 3)).replace('-', '+')
                    ssub_x += '(' + 'x' + new_str + ')' + '*'
                else:
                    ssub_x += '(' + 'x' + '-' +\
                            str(round(tab_x[dots[i-k]], 3)) + ')' + '*'
            k += 1

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

    return res, sres


def div_diff_count(dots, tab_x, tab_y):
    if (len(dots) == 1):
        #print(tab_y[dots[0]])
        return tab_y[dots[0]]

    a1 = ((div_diff_count(dots[:len(dots) - 1], tab_x, tab_y)
        - div_diff_count(dots[1:], tab_x, tab_y))
        / (tab_x[dots[0]] - tab_x[dots[len(dots) - 1]]))

    return a1


def div_diff_arr(dots, tab_x, tab_y):
    dd_arr = []

    for i in range(len(dots)):
        a = div_diff_count(dots[0:i+1], tab_x, tab_y)
        dd_arr.append(a)

    return dd_arr


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


def interpolate_1(func_tab, arg):
    n = len(func_tab)

    # индекс ближайшего к аргументу элемента
    i_elem = min(range(n), key = lambda i: abs(func_tab[i][0] - arg))
    #print(i_elem)

    # h = x_i_ - x_i-1_
    h = [0 if not i else func_tab[i][0] - func_tab[i - 1][0]\
        for i in range(n)]

    # для вычисления c_i_
    A = [0 if i < 2 else h[i-1] for i in range(n)]
    B = [0 if i < 2 else -2 * (h[i - 1] + h[i]) for i in range(n)]
    D = [0 if i < 2 else h[i] for i in range(n)]
    F = [0 if i < 2 else -3 * ((func_tab[i][1] - func_tab[i - 1][1]) /\
        h[i] - (func_tab[i - 1][1] - func_tab[i - 2][1]) /\
        h[i - 1]) for i in range(n)]

    # прямой ход
    ksi = [0 for i in range(n + 1)]
    nude = [0 for i in range(n + 1)]
    for i in range(2, n):
        ksi[i + 1] = D[i] / (B[i] - A[i] * ksi[i])
        nude[i + 1] = (A[i] * nude[i] + F[i]) / (B[i] - A[i] * ksi[i])

    # обратный ход
    c = [0 for i in range(n + 1)]
    for i in range(n - 2, -1, -1):
        c[i] = ksi[i + 1] * c[i + 1] + nude[i + 1]

    a = [0 if i < 1 else func_tab[i-1][1] for i in range(n)]
    b = [0 if i < 1 else (func_tab[i][1] - func_tab[i - 1][1]) / h[i] - h[i] /\
        3 * (c[i + 1] + 2 * c[i]) for i in range(n)]
    d = [0 if i < 1 else (c[i + 1] - c[i]) / (3 * h[i]) for i in range(n)]

    return a[i_elem] + b[i_elem] * (arg - func_tab[i_elem - 1][0]) +\
           c[i_elem] * ((arg - func_tab[i_elem - 1][0]) ** 2) +\
           d[i_elem] * ((arg - func_tab[i_elem - 1][0]) ** 3)


def interpolate_2(func_tab, arg, p0):
    n = len(func_tab)

    # индекс ближайшего к аргументу элемента
    i_elem = min(range(n), key = lambda i: abs(func_tab[i][0] - arg))
    #print(i_elem)

    # h = x_i_ - x_i-1_
    h = [0 if not i else func_tab[i][0] - func_tab[i - 1][0]\
        for i in range(n)]

    # для вычисления c_i_
    A = [0 if i < 2 else h[i-1] for i in range(n)]
    B = [0 if i < 2 else -2 * (h[i - 1] + h[i]) for i in range(n)]
    D = [0 if i < 2 else h[i] for i in range(n)]
    F = [0 if i < 2 else -3 * ((func_tab[i][1] - func_tab[i - 1][1]) /\
        h[i] - (func_tab[i - 1][1] - func_tab[i - 2][1]) /\
        h[i - 1]) for i in range(n)]

    # прямой ход
    ksi = [0 for i in range(n + 1)]
    nude = [0 for i in range(n + 1)]
    for i in range(2, n):
        ksi[i + 1] = D[i] / (B[i] - A[i] * ksi[i])
        nude[i + 1] = (A[i] * nude[i] + F[i]) / (B[i] - A[i] * ksi[i])

    # обратный ход
    c = [0 for i in range(n + 1)]
    for i in range(n - 2, -1, -1):
        c[i] = ksi[i + 1] * c[i + 1] + nude[i + 1]

    c[1] = p0

    a = [0 if i < 1 else func_tab[i-1][1] for i in range(n)]
    b = [0 if i < 1 else (func_tab[i][1] - func_tab[i - 1][1]) / h[i] - h[i] /\
        3 * (c[i + 1] + 2 * c[i]) for i in range(n)]
    d = [0 if i < 1 else (c[i + 1] - c[i]) / (3 * h[i]) for i in range(n)]

    return a[i_elem] + b[i_elem] * (arg - func_tab[i_elem - 1][0]) +\
           c[i_elem] * ((arg - func_tab[i_elem - 1][0]) ** 2) +\
           d[i_elem] * ((arg - func_tab[i_elem - 1][0]) ** 3)


def interpolate_3(func_tab, arg, p0, pn):
    n = len(func_tab)

    # индекс ближайшего к аргументу элемента
    i_elem = min(range(n), key = lambda i: abs(func_tab[i][0] - arg))
    #print(i_elem)

    # h = x_i_ - x_i-1_
    h = [0 if not i else func_tab[i][0] - func_tab[i - 1][0]\
        for i in range(n)]

    # для вычисления c_i_
    A = [0 if i < 2 else h[i-1] for i in range(n)]
    B = [0 if i < 2 else -2 * (h[i - 1] + h[i]) for i in range(n)]
    D = [0 if i < 2 else h[i] for i in range(n)]
    F = [0 if i < 2 else -3 * ((func_tab[i][1] - func_tab[i - 1][1]) /\
        h[i] - (func_tab[i - 1][1] - func_tab[i - 2][1]) /\
        h[i - 1]) for i in range(n)]

    # прямой ход
    ksi = [0 for i in range(n + 1)]
    nude = [0 for i in range(n + 1)]
    for i in range(2, n):
        ksi[i + 1] = D[i] / (B[i] - A[i] * ksi[i])
        nude[i + 1] = (A[i] * nude[i] + F[i]) / (B[i] - A[i] * ksi[i])

    # обратный ход
    c = [0 for i in range(n + 1)]
    for i in range(n - 2, -1, -1):
        c[i] = ksi[i + 1] * c[i + 1] + nude[i + 1]

    c[1] = p0
    c[n] = pn

    a = [0 if i < 1 else func_tab[i-1][1] for i in range(n)]
    b = [0 if i < 1 else (func_tab[i][1] - func_tab[i - 1][1]) / h[i] - h[i] /\
        3 * (c[i + 1] + 2 * c[i]) for i in range(n)]
    d = [0 if i < 1 else (c[i + 1] - c[i]) / (3 * h[i]) for i in range(n)]

    return a[i_elem] + b[i_elem] * (arg - func_tab[i_elem - 1][0]) +\
           c[i_elem] * ((arg - func_tab[i_elem - 1][0]) ** 2) +\
           d[i_elem] * ((arg - func_tab[i_elem - 1][0]) ** 3)


def main():
    ##arg = float(input('Введите x: '))
    arg = 2.5

    #Интерполяция Ньютоном
    table_x = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ]
    table_y = [ 0, 0.496, 0.986, 1.102,  0.972, 0.754,\
                0.539, 0.364, 0.236, 0.148, 0.091]
    n = 3

    dots = choose_dots(arg, table_x, n)
    values = div_diff_arr(dots, table_x, table_y)
    res_newton, pol_newton = inter_newton(arg, values, table_x, dots)
    res_newton = round(res_newton, 7)

    #Производные полинома ньютона
    x = Symbol('x')

    #x==0
    dots = choose_dots(0, table_x, n)
    values = div_diff_arr(dots, table_x, table_y)
    tmp, pol_newton = inter_newton(0, values, table_x, dots)
    #print(pol_newton)
    pol_newton = str(diff(pol_newton, x, 2))
    #print(pol_newton)
    pol_newton = pol_newton.replace('x', '0')
    ppn0 = eval(pol_newton)
    #print(ppn0)

    #x==10
    dots = choose_dots(10, table_x, n)
    values = div_diff_arr(dots, table_x, table_y)
    tmp, pol_newton = inter_newton(10, values, table_x, dots)
    pol_newton = str(diff(pol_newton, x, 2))
    #print(pol_newton)
    pol_newton = pol_newton.replace('x', '10')
    ppnn = eval(pol_newton)
    #print(ppnn)

    #Интерполяция спалйнами
    func_table = [[0, 0], [1, 0.496], [2, 0.986], [3, 1.102], [4, 0.972],\
                  [5, 0.754], [6, 0.539], [7, 0.364], [8, 0.236], [9, 0.148],\
                  [10, 0.091]]

    f_arg1 = round(interpolate_1(func_table, arg), 12)
    f_arg2 = round(interpolate_2(func_table, arg, ppn0), 12)
    f_arg3 = round(interpolate_3(func_table, arg, ppn0, ppnn), 12)

    #Результаты
    print(f"Сплайны (2.1): f(x) в точке {arg}: ", f_arg1)
    print(f"Сплайны (2.2): f(x) в точке {arg}: ", f_arg2)
    print(f"Сплайны (2.3): f(x) в точке {arg}: ", f_arg3)
    print(f"Ньютон:  f(x) в точке {arg}: ", res_newton)


if __name__ == '__main__':
    main()