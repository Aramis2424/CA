from prettytable import PrettyTable
import numexpr as ne
import matplotlib.pyplot as plt
import random

MODE_EXIT = '0'
MODE_INTERPOLATION = '1'

NOT_ENOUGH_DATA = 10

# Находит индексы в массиве, из которых нужно будет вытащить count + 1 значение
# j не включается
def find_dots(array, x, count):
    if count >= len(array):
        return NOT_ENOUGH_DATA

    i = 0
    while i < len(array) and array[i] < x:
        i += 1

    if i < count // 2 + 1:
        start, end = 0, count + 1
    elif i > len(array) - count:
        start, end = len(array) - count - 1, len(array)
    else:
        start = i - count // 2 - 1 if x != array[i] or count % 2 == 1 else i - count // 2
        end = i + count // 2 + 1 if count % 2 == 1 or x == array[i] else i + count // 2

    return start, end

# Функция составляет полином Ньютона на основе высчитанной таблицы
def Newton_polynomial(tableNewton):
    pol = '%2.3f' % tableNewton[1][0]
    for k in range(2, len(tableNewton)):
        pol += ' + (%2.3f' % tableNewton[k][0]
        for i in range(k - 1):
            if tableNewton[0][i] == 0:
                pol += ' * x'
            elif tableNewton[0][i] > 0:
                pol += ' * (x - %2.3f)' % tableNewton[0][i]
            else:
                pol += ' * (x + %2.3f)' % abs(tableNewton[0][i])
        pol += ')'
    return pol

# Функция проводит одномерную интерполяцию Ньютона для выбранного значения x
def Newton_interpolation(tableNewton, x):
    j = 1
    while len(tableNewton[-1]) != 1:
        tableNewton.append([(tableNewton[-1][i] - tableNewton[-1][i + 1]) /
                            (tableNewton[0][i] - tableNewton[0][i + j]) for i in range(len(tableNewton[-1]) - 1)])
        j += 1

    polStr = Newton_polynomial(tableNewton)
    pol = ne.evaluate(polStr)

    # возвращает таблицу значений полинома, строку-полином, итоговое значение y для введенного x
    return tableNewton, polStr, pol

class DoubleTable:
    def __init__(self):
        self.x = []  # одномерный массив
        self.y = []  # одномерный массив
        self.z = []  # двумерный массив

    def input_from_open_file(self, f):
        self.x = list(map(float, f.readline().split()))
        s = f.readline()
        while s:
            if s == '\n':
                return 1           # строки в файле еще есть
            s = list(map(float, s.split()))
            self.y.append(s[0])
            self.z.append(s[1:])
            s = f.readline()
        return 0                    # строк в файле больше нет

    # nx, ny -- степени полиномов
    # Сначала нужно выбрать ближайшие к x nx + 1 значений и ближайшие к y ny + 1 значений
    # построить таблицу из x и z, провести для каждой строчки интреполяцию Ньютона
    # составить таблицу y и полученных значений
    # провести интреполяцию для них (она будет одна)
    def two_newtonInter(self, x, y, nx, ny):
        indXStart, indXEnd = find_dots(self.x, x, nx) #- сосед. т. по х
        indYStart, indYEnd = find_dots(self.y, y, ny) #- сосед. т. по у

        #print(indXStart,indXEnd)
        #print(indYStart,indYEnd)


        YTable = []  # результативная таблица "по строкам"
        for k in range(indYStart, indYEnd):
            tableForNewton = [[self.x[i] for i in range(indXStart, indXEnd)],
                              [self.z[x][k] for x in range(indXStart, indXEnd)]]
            #print(tableForNewton)

            tableNewton, polStr, pol = Newton_interpolation(tableForNewton, x)
            YTable += [float(pol)]
            #print(YTable)

        # теперь последняя интерполяция по y и YTable
        tableForNewton = [[self.y[i] for i in range(indYStart, indYEnd)], YTable]
        tableNewton, polStr, pol = Newton_interpolation(tableForNewton, y)
        #print(pol)
        return pol

class TripleTable:
    def __init__(self):
        self.z = []     # одномерный массив
        self.xy = []    # одномерный массив из doubleTable

    def input_from_txt_file(self, filename):
        with open(filename, 'r') as fin:
            isInputTable = True
            while isInputTable:
                self.xy.append(DoubleTable())
                self.z.append(float(fin.readline()))
                isInputTable = self.xy[-1].input_from_open_file(fin)

    def three_newton(self, x, y, z, nx, ny, nz, showComments=False):
        indZStart, indZEnd = find_dots(self.z, z, nz)
        if showComments:
            print('indZStart =', indZStart, '; indZEnd =', indZEnd)

        ZTable = []   # результативная таблица "по строкам"
        for k in range(indZStart, indZEnd):
            ZTable += [float(self.xy[k].two_newtonInter(x, y, nx, ny))]

        if showComments:
            print('ZTable =', ZTable)

        # теперь последняя интерполяция по z и ZTable
        tableForNewton = [[self.z[i] for i in range(indZStart, indZEnd)], ZTable]
        tableNewton, polStr, pol = Newton_interpolation(tableForNewton, z)
        return pol


def menu():
    print("Menu:\n"
          "    0 - EXIT\n"
          "    1 - perform interpolation\n")
    return input("Input command: ")

if __name__ == '__main__':
    #mode = menu()
    table = TripleTable()
    table.input_from_txt_file(r'data.txt')
    mode = '1'
    while mode != MODE_EXIT:

        if mode == MODE_INTERPOLATION:
            try:
                x = 0.5
                y = 1.5
                z = 2.5
                nx = 1
                ny = 2
                nz = 3
                print()
            except:
                print('Invalid input')
                #mode = menu()
                continue
            res = table.three_newton(x, y, z, nz, ny, nz, False)
            print(f'u = f{x, y, z} = ', round(float(res),3), '\n')

        #mode = menu()
        mode = '0'



##                x = float(input('Input x [float]: '))
##                y = float(input('Input y [float]: '))
##                z = float(input('Input z [float]: '))
##                nx = int(input('Input x degree (nx) [int]: '))
##                ny = int(input('Input y degree (ny) [int]: '))
##                nz = int(input('Input z degree (nz) [int]: '))
