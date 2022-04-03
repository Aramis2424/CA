import diff as mmm

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


def read_table(f):
    global x_arr, y_arr, count
    size = int(f.readline())
    count = size
    for i in range(size):
        tmp = f.readline().split()
        x, y = float(tmp[0]), float(tmp[1])
        x_arr.append(x)
        y_arr.append(y)

def find_x_index(x):
    global x_arr, y_arr, count
    find = 0
    for i in range(0, count):
        if x < x_arr[i]:
            find = i
            break
    return find

def interpolate_spline_normal(input_x):
    global x_arr, y_arr, count
    arr_a = [0] * 100
    arr_b = [0] * 100
    arr_d = [0] * 100
    arr_C = [0] * 100

    arr_tmp = [0] * 100
    arr_F = [0] * 100

    arr_K = [0] * 100
    arr_E = [0] * 100

    arr_H = [0] * 100

    for i in range(1, count):
        arr_H[i] = x_arr[i] - x_arr[i - 1]

    for i in range(2, count):
        arr_tmp[i] = -2 * (arr_H[i - 1] + arr_H[i])

        arr_F[i] = -3 * ((y_arr[i] - y_arr[i - 1]) / arr_H[i] - (y_arr[i] - y_arr[i - 2]) / arr_H[i - 1])

        arr_K[i + 1] = arr_H[i] / (arr_tmp[i] - arr_H[i - 1] * arr_K[i])
        arr_E[i + 1] = (arr_H[i - 1] * arr_E[i] + arr_F[i]) / (arr_tmp[i] - arr_H[i - 1] * arr_K[i])

    for i in range(count - 2, 1, -1):
        arr_C[i] = arr_K[i + 1] * arr_C[i + 1] + arr_E[i + 1]

    for i in range(count - 1, 0, -1):
        arr_a[i] = y_arr[i - 1]
        arr_d[i] = (arr_C[i + 1] - arr_C[i]) / (3 * arr_H[i])
        arr_b[i] = (y_arr[i] - y_arr[i - 1]) / arr_H[i] - arr_H[i] * (arr_C[i + 1] + 2 * arr_C[i]) / 3

    x_i = find_x_index(input_x)

    x = input_x - x_arr[x_i - 1]
    x2 = x * x
    x3 = x * x * x

    result = arr_a[x_i] + arr_b[x_i] * x + arr_C[x_i] * x2 + arr_d[x_i] * x3
    print("Сплайн (2.1) = {}".format(result))

def interpolate_spline_first(input_x):
    global x_arr, y_arr, count
    c1 = mmm.mif(x_arr[0])
    arr_a = [0] * 100
    arr_b = [0] * 100
    arr_d = [0] * 100
    arr_C = [0] * 100

    arr_tmp = [0] * 100
    arr_F = [0] * 100

    arr_K = [0] * 100
    arr_E = [0] * 100

    arr_H = [0] * 100
    arr_C[1] = c1

    for i in range(1, count):
        arr_H[i] = x_arr[i] - x_arr[i - 1]

    for i in range(2, count):
        arr_tmp[i] = -2 * (arr_H[i - 1] + arr_H[i])

        arr_F[i] = -3 * ((y_arr[i] - y_arr[i - 1]) / arr_H[i] - (y_arr[i] - y_arr[i - 2]) / arr_H[i - 1])

        arr_K[i + 1] = arr_H[i] / (arr_tmp[i] - arr_H[i - 1] * arr_K[i])
        arr_E[i + 1] = (arr_H[i - 1] * arr_E[i] + arr_F[i]) / (arr_tmp[i] - arr_H[i - 1] * arr_K[i])

    for i in range(count - 2, 1, -1):
        arr_C[i] = arr_K[i + 1] * arr_C[i + 1] + arr_E[i + 1]

    for i in range(count - 1, 0, -1):
        arr_a[i] = y_arr[i - 1]
        arr_d[i] = (arr_C[i + 1] - arr_C[i]) / (3 * arr_H[i])
        arr_b[i] = (y_arr[i] - y_arr[i - 1]) / arr_H[i] - arr_H[i] * (arr_C[i + 1] + 2 * arr_C[i]) / 3

    x_i = find_x_index(input_x)

    x = input_x - x_arr[x_i - 1]
    x2 = x * x
    x3 = x * x * x

    result = arr_a[x_i] + arr_b[x_i] * x + arr_C[x_i] *\
         x2 + arr_d[x_i] * x3
    print("Сплайн (2.2) = {}".format(result))

def interpolate_spline_both(input_x):
    global x_arr, y_arr, count
    c1 = mmm.mif(x_arr[0])
    c2 = mmm.mif(x_arr[-1])
    arr_a = [0] * 100
    arr_b = [0] * 100
    arr_d = [0] * 100
    arr_C = [0] * 100

    arr_tmp = [0] * 100
    arr_F = [0] * 100

    arr_K = [0] * 100
    arr_E = [0] * 100
    arr_H = [0] * 100
    arr_C[1] = c1
    arr_C[count] = c2
    for i in range(1, count):
        arr_H[i] = x_arr[i] - x_arr[i - 1]

    for i in range(2, count):
        arr_tmp[i] = -2 * (arr_H[i - 1] + arr_H[i])

        arr_F[i] = -3 * ((y_arr[i] - y_arr[i - 1]) /\
             arr_H[i] - (y_arr[i] - y_arr[i - 2]) / arr_H[i - 1])

        arr_K[i + 1] = arr_H[i] / (arr_tmp[i] - arr_H[i - 1] * arr_K[i])
        arr_E[i + 1] = (arr_H[i - 1] * arr_E[i] + arr_F[i]) /\
             (arr_tmp[i] - arr_H[i - 1] * arr_K[i])

    for i in range(count - 2, 1, -1):
        arr_C[i] = arr_K[i + 1] * arr_C[i + 1] + arr_E[i + 1]

    for i in range(count - 1, 0, -1):
        arr_a[i] = y_arr[i - 1]
        arr_b[i] = (y_arr[i] - y_arr[i - 1]) /\
            arr_H[i] - arr_H[i] * (arr_C[i + 1] + 2 * arr_C[i]) / 3
        arr_d[i] = (arr_C[i + 1] - arr_C[i]) / (3 * arr_H[i])


    x_i = find_x_index(input_x)

    x = input_x - x_arr[x_i - 1]
    x2 = x * x
    x3 = x * x * x

    result = arr_a[x_i] + arr_b[x_i] * x + arr_C[x_i] *\
        x2 + arr_d[x_i] * x3
    print("Сплайн (2.3) = {}".format(result))


if __name__ == '__main__':
    f = open("table.txt", "r")
    x_arr = []
    y_arr = []
    count = 0
    read_table(f)
    f.close()

    arg = 5.5 ###################

    dots = choose_dots(arg, x_arr, 3)
    values = div_diff_arr(dots, x_arr, y_arr)
    res_newton, pol_newton = inter_newton(arg, values, x_arr, dots)
    res_newton = round(res_newton, 7)
    print(f'Значение f({arg}):')
    print('Ньютон: ', res_newton)

    interpolate_spline_normal(arg)
    interpolate_spline_first(arg)
    interpolate_spline_both(arg)
    #print(mmm.mif(x_arr[0]))