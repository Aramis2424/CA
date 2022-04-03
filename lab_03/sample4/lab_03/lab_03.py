from matplotlib import pyplot as plt
import xlrd
from class_of_string import *



class Dot:
    def __init__(self, arg, val):
        if type(arg) == list:
            buf = arg
            self.arg = buf[0]
            self.val = buf[1]
        else:
            self.arg = arg
            self.val = val


class Coefs_table:
    def __init__(self, fname):
        self.fname = fname
        self.table = []
        self.dots = []

    def read_and_sort_dots(self):
        with open(self.fname) as f:
            line = f.readline()
            while line:
                line = line.strip('\n')
                self.dots.append(Dot(list(map(float, line.split())), 0))
                line = f.readline()

        self.dots = dots_sort(self.dots)

    def fill_table(self, var=1, x=None):
        self.read_and_sort_dots()
        for dot in self.dots:
            self.table.append(Coefs_string(dot.arg, dot.val))

        for i in range(1, len(self.table)):
            self.table[i].h_calc(self.table[i - 1])

        for i in range(2, len(self.table)):
            self.table[i].f_calc(self.table[i - 1], self.table[i - 2])

        if var == 1:
            self.table[2].E = self.table[2].n = self.table[1].c = 0
            obj = Coefs_string(0, 0, c=0)
        if var == 2:
            self.table[2].E = 0
            self.table[2].n = Newton_way__(3, self.dots[0].arg, self.dots)
            self.table[1].c = Newton_way__(3, self.dots[0].arg, self.dots)
            obj = Coefs_string(0, 0, c=0)
        if var == 3:
            self.table[2].E = self.table[2].n = 0
            self.table[2].n = Newton_way__(3, self.dots[0].arg, self.dots)
            self.table[1].c = Newton_way__(3, self.dots[0].arg, self.dots)
            obj = Coefs_string(0, 0, c=Newton_way__(3, self.dots[-1].arg, self.dots))

        for i in range(3, len(self.table)):
            self.table[i].E_calc(self.table[i - 1], self.table[i - 2])
            self.table[i].n_calc(self.table[i - 1], self.table[i - 2])

        for i in range(len(self.table) - 1, 1, -1):
            if i == len(self.table) - 1:
                self.table[i].c_calc(self.table[i - 1], obj)
            else:
                self.table[i].c_calc(self.table[i - 1], self.table[i + 1])

        for i in range(1, len(self.table)):
            self.table[i].a_calc(self.table[i - 1])

        for i in range(len(self.table) - 1, 0, -1):
            if i == len(self.table) - 1:
                self.table[i].b_calc(self.table[i - 1], obj)
            else:
                self.table[i].b_calc(self.table[i - 1], self.table[i + 1])

        for i in range(len(self.table) - 1, 0, -1):
            if i == len(self.table) - 1:
                self.table[i].d_calc(obj)
            else:
                self.table[i].d_calc(self.table[i + 1])

    def print_table(self):
        i = 0
        f = '.4f'
        for line in self.table:
            try:
                print(
                    f'{i}: x={line.x:{f}}, y={line.y:{f}}, h={line.h:{f}}, f={line.f:{f}}, E={line.E:{f}}, n={line.n:{f}}, c={line.c:{f}}, a={line.a:{f}}, b={line.b:{f}}, d={line.d:{f}}')
            except:
                print(
                    f'{i}: x={line.x}, y={line.y}, h={line.h}, f={line.f}, E={line.E}, n={line.n}, c={line.c}, a={line.a}, b={line.b}, d={line.d}')
            i += 1


def culc_func_for_newton(args, dictt):
    if len(args) == 1:
        return dictt[args[0]]
    if len(args) == 2:
        return (dictt[args[0]] - dictt[args[1]]) / (args[0] - args[1])
    else:
        return (culc_func_for_newton(args[:-1], dictt) - culc_func_for_newton(args[1:], dictt)) / (args[0] - args[-1])


def culc_func_for_ermit(args, dictt):
    if len(args) == 1:
        return dictt[args[0]][0]
    if len(args) == 2 and args[0] != args[1]:
        return (dictt[args[0]][0] - dictt[args[1]][0]) / (args[0] - args[1])
    elif len(args) == 2 and args[0] == args[1]:
        return dictt[args[0]][1]
    else:
        return (culc_func_for_ermit(args[:-1], dictt) - culc_func_for_ermit(args[1:], dictt)) / (args[0] - args[-1])


def find_start_and_stop(n, x, dots):
    if n + 1 > len(dots):
        print('Недостаточно точек для заданного n!')
        exit(1)

    index = 0
    for dot in dots:
        if dot.arg < x:
            index += 1

    half1 = (n + 1) // 2
    half2 = (n + 1) - half1

    start_ind = (index - half1) if (index - half1 >= 0) else 0
    stop_ind = (index + half2) if (index + half2 <= len(dots)) else len(dots)

    if start_ind == 0:
        stop_ind += abs(index - half1)

    if stop_ind == len(dots):
        start_ind -= index + half2 - len(dots)

    return start_ind, stop_ind


def Newton_way(n, x, dots, printFl=0):
    start_ind, stop_ind = find_start_and_stop(n, x, dots)

    res = 0
    func_dict = {}
    for i in range(start_ind, stop_ind):
        func_dict[dots[i].arg] = dots[i].val

    if printFl:
        print(func_dict, start_ind, stop_ind)

    for i in range(start_ind, stop_ind):
        j = i - start_ind + 1
        args = []
        loc_sum = 1
        for k in range(j):
            args.append(dots[start_ind + k].arg)
            if k >= 1:
                loc_sum *= (x - dots[start_ind + k - 1].arg)
        loc_sum *= culc_func_for_newton(args, func_dict)
        res += loc_sum

    return res


def Newton_way__(n, x, dots, printFl=0):
    start_ind, stop_ind = find_start_and_stop(n, x, dots)

    res = 0
    func_dict = {}
    for i in range(start_ind, stop_ind):
        func_dict[dots[i].arg] = dots[i].val

    # if printFl:
    #     print(func_dict, start_ind, stop_ind)

    for i in range(start_ind, stop_ind):
        j = i - start_ind + 1
        args = []
        loc_sum = 1
        for k in range(j):
            args.append(dots[start_ind + k].arg)

        if j == 3:
            # if printFl:
            # print(culc_func_for_newton(args, func_dict))
            loc_sum *= culc_func_for_newton(args, func_dict) * 2
            res += loc_sum

        if j == 4:
            # if printFl:
            # print(culc_func_for_newton(args, func_dict), dots[start_ind+1].arg, dots[start_ind+2].arg)
            loc_sum *= culc_func_for_newton(args, func_dict) * (6*x - 2*(dots[start_ind].arg + dots[start_ind+1].arg + dots[start_ind+2].arg))
            res += loc_sum

    # if printFl:
    # print(f'\nprod = {res}')

    return res/2


def Ermit_way(n, x, dots):
    start_ind, stop_ind = find_start_and_stop(n, x, dots)

    res = 0
    func_dict = {}
    for i in range(start_ind, stop_ind):
        func_dict[dots[i].x] = [dots[i].y, dots[i].dir]

    j = -1
    for i in range(start_ind, stop_ind):
        j += 2
        for ii in range(2):
            args = []
            loc_sum = 1
            for l in range(j + ii):
                k = l // 2
                args.append(dots[start_ind + k].x)
                if l >= 1:
                    loc_sum *= (x - dots[start_ind + k].x)

            loc_sum *= culc_func_for_ermit(args, func_dict)
            res += loc_sum

    return res


def Spline_way(x, file, var):
    table = Coefs_table(file)

    table.fill_table(var=var, x=x)

    target_ind = 0
    for i in range(len(table.table)):
        if table.table[i].x <= x:
            target_ind += 1

    if target_ind == 0 or target_ind >= len(table.dots):
        print(x, target_ind, len(table.dots))
        print('Невозможно посчитать значение!')
        exit(1)

    prev_x = table.table[target_ind - 1].x
    res = table.table[target_ind].a + table.table[target_ind].b * (x - prev_x) + table.table[target_ind].c * (
            (x - prev_x) ** 2) + table.table[target_ind].d * ((x - prev_x) ** 3)

    return res


def dots_sort(dots):
    n = len(dots)
    for i in range(n-1):
        flag = True
        for j in range(n-1-i):
            if dots[j].arg > dots[j + 1].arg:
                dots[j], dots[j + 1] = dots[j + 1], dots[j]
                flag = False
        if flag:
            break
    return dots


x = float(input('x >> '))
file = "data.txt"

tbl = Coefs_table(file)
tbl.read_and_sort_dots()
plt.plot([dot.arg for dot in tbl.dots], [dot.val for dot in tbl.dots])
plt.grid()
plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k')

colors = ['orange', 'red', 'green']
for var in range(1, 4):
    print(f'var 2.{var}: ', end='')
    print(f'res={Spline_way(x, file, var)}')
    plt.scatter(x, Spline_way(x, file, 1), c=colors[0])


mid_x = (tbl.dots[-1].arg + tbl.dots[0].arg)/2
first_x = tbl.dots[0].arg + 0.00001
last_x = tbl.dots[-1].arg - 0.00001


print(f'\n                             Куб. сплайн    Ньютон')
print(f'В середине x = {mid_x:8.5f}:    {Spline_way(mid_x, file, 1):12.9f}   {Newton_way(3, mid_x, tbl.dots):12.9f}')
print(f'Лев. край  x = {first_x:8.5f}:    {Spline_way(first_x, file, 1):12.9f}   {Newton_way(3, first_x, tbl.dots):12.9f}')
print(f'Прав. край x = {last_x:8.5f}:    {Spline_way(last_x, file, 1):12.9f}   {Newton_way(3, last_x, tbl.dots):12.9f}')

plt.scatter(mid_x, Spline_way(mid_x, file, 1), c='blue')
plt.scatter(first_x, Spline_way(first_x, file, 1), c=colors[1])
plt.scatter(last_x, Spline_way(last_x, file, 1), c=colors[2])

plt.show()
