from prettytable import PrettyTable
import numexpr as ne
import matplotlib.pyplot as plt
import random

MODE_EXIT = '0'
MODE_INTERPOLATION = '1'

NOT_ENOUGH_DATA = 10

# Находит индексы в массиве, из которых нужно будет вытащить count + 1 значение
# j не включается
def findNearestInd(array, x, count):
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

def printResultTable(table, name, flag='Newton'):
    print(name)
    print('-------------------------------------')
    for i in range(len(table)):
        if i == 0:
            print(f'X:', end=' ')
        elif i == 1:
            print(f'Y:', end=' ')
        elif i == 2 and flag == 'Hermite':
            print(f"Y':", end=' ')
        else:
            print(f'{i}:', end=' ')
        for j in range(len(table[i])):
            print('%+2.3f' % table[i][j], end=' ')
        print()
    print('-------------------------------------')


# Функция составляет полином Ньютона на основе высчитанной таблицы
def NewtonPolynomial(tableNewton):
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
def interpolationNewton(tableNewton, x, printComments=False):
    j = 1
    while len(tableNewton[-1]) != 1:
        tableNewton.append([(tableNewton[-1][i] - tableNewton[-1][i + 1]) /
                            (tableNewton[0][i] - tableNewton[0][i + j]) for i in range(len(tableNewton[-1]) - 1)])
        j += 1

    polStr = NewtonPolynomial(tableNewton)
    pol = ne.evaluate(polStr)

    if printComments:
        printResultTable(tableNewton, "NEWTON TABLE")
        print('P(x) =', polStr)
        print('-------------------------------------')
        print('P(%2.3f) = %2.5f' % (x, ne.evaluate(polStr)))
        print('-------------------------------------')

    # возвращает таблицу значений полинома, строку-полином, итоговое значение y для введенного x
    return tableNewton, polStr, pol

class DoubleTable:
    def __init__(self):
        self.x = []  # одномерный массив
        self.y = []  # одномерный массив
        self.z = []  # двумерный массив

    def inputFromOpenTXTFile(self, f):
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

    """ Задача -- провести двумерную интерполяцию (то есть по x, y предсказать z) """
    # nx, ny -- степени полиномов
    # Сначала нужно выбрать ближайшие к x nx + 1 значений и ближайшие к y ny + 1 значений
    # построить таблицу из x и z, провести для каждой строчки интреполяцию Ньютона
    # составить таблицу y и полученных значений
    # провести интреполяцию для них (она будет одна)
    def doubleNewtonInter(self, x, y, nx, ny):
        indXStart, indXEnd = findNearestInd(self.x, x, nx) #- сосед. т. по х
        indYStart, indYEnd = findNearestInd(self.y, y, ny) #- сосед. т. по у

        #print(indXStart,indXEnd)
        #print(indYStart,indYEnd)


        YTable = []  # результативная таблица "по строкам"
        for k in range(indYStart, indYEnd):
            tableForNewton = [[self.x[i] for i in range(indXStart, indXEnd)],
                              [self.z[x][k] for x in range(indXStart, indXEnd)]]
            print(tableForNewton)

            tableNewton, polStr, pol = interpolationNewton(tableForNewton, x)
            YTable += [float(pol)]
            #print(YTable)

        # теперь последняя интерполяция по y и YTable
        tableForNewton = [[self.y[i] for i in range(indYStart, indYEnd)], YTable]
        tableNewton, polStr, pol = interpolationNewton(tableForNewton, y)
        #print(pol)
        return pol

class TripleTable:
    def __init__(self):
        self.z = []     # одномерный массив
        self.xy = []    # одномерный массив из doubleTable

    def inputFromTXTFile(self, filename):
        with open(filename, 'r') as fin:
            isInputTable = True
            while isInputTable:
                self.xy.append(DoubleTable())
                self.z.append(float(fin.readline()))
                isInputTable = self.xy[-1].inputFromOpenTXTFile(fin)

    def tripleNewtonInter(self, x, y, z, nx, ny, nz, showComments=False):
        indZStart, indZEnd = findNearestInd(self.z, z, nz)
        if showComments:
            print('indZStart =', indZStart, '; indZEnd =', indZEnd)

        ZTable = []   # результативная таблица "по строкам"
        for k in range(indZStart, indZEnd):
            ZTable += [float(self.xy[k].doubleNewtonInter(x, y, nx, ny))]

        if showComments:
            print('ZTable =', ZTable)

        # теперь последняя интерполяция по z и ZTable
        tableForNewton = [[self.z[i] for i in range(indZStart, indZEnd)], ZTable]
        tableNewton, polStr, pol = interpolationNewton(tableForNewton, z)
        return pol


def menu():
    print("Menu:\n"
          "    0 - EXIT\n"
          "    1 - perform interpolation\n")
    return input("Input command: ")

if __name__ == '__main__':
    #mode = menu()
    table = TripleTable()
    table.inputFromTXTFile(r'data.txt')
    mode = '1'
    while mode != MODE_EXIT:

        if mode == MODE_INTERPOLATION:
            try:
                x = 3.5
                y = 2.5
                z = 3.5
                nx = 3
                ny = 2
                nz = 3
                print()
            except:
                print('Invalid input')
                #mode = menu()
                continue
            res = table.tripleNewtonInter(x, y, z, nz, ny, nz, True)
            print('Res =', res, '\n')

        #mode = menu()
        mode = '0'



##                x = float(input('Input x [float]: '))
##                y = float(input('Input y [float]: '))
##                z = float(input('Input z [float]: '))
##                nx = int(input('Input x degree (nx) [int]: '))
##                ny = int(input('Input y degree (ny) [int]: '))
##                nz = int(input('Input z degree (nz) [int]: '))
