from prettytable import PrettyTable

FILE_WITH_TABLE = 'data\\data.txt'
FILE_WITH_DOUBLE_TABLE = 'data\\double_data.txt'

MODE_EXIT = '0'
MODE_INPUT_FROM_FILE = '1'
MODE_INTERPOLATION = '2'
MODE_PRINT_TABLE = '3'

NOT_ENOUGH_DATA = 10


def inputTableFromFile(filename=FILE_WITH_TABLE):
    table = []
    with open(filename, 'r') as fin:
        s = fin.readline()
        while s:
            table.append(list(map(float, s.split(" "))))
            s = fin.readline()

    return table


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
from prettytable import PrettyTable


import numexpr as ne
import numexpr as ne


def showGraphUsePol(table, polStr, plt, label, color):
    X, Y = [], []
    x = table[0][0]
    while x <= table[0][-1]:
        Y.append(ne.evaluate(polStr))
        X.append(x)
        x += (table[0][-1] - table[0][0]) / 50

    plt.plot(X, Y, color, ms=5, label=label)



def showGraphUsePoints(X, Y, plt, label, color):
    plt.plot(X, Y, color, ms=5, label=label)
import matplotlib.pyplot as plt
import random


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
# Table -- двумерный массив вида [[x][y]]
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

    def inputFromTXTFile(self, filename=FILE_WITH_DOUBLE_TABLE):
        with open(filename, 'r') as fin:
            self.inputFromOpenTXTFile(fin)

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

    def print(self):
        resTable = PrettyTable()
        resTable.field_names = ['Y\X'] + [str(x) for x in self.x]

        for i in range(len(self.y)):
            add = [f"{self.y[i]}"]
            for j in range(len(self.z[i])):
                add.append(str(self.z[i][j]))
            resTable.add_row(add)

        print(resTable)

    """ Задача -- провести двумерную интерполяцию (то есть по x, y предсказать z) """
    # nx, ny -- степени полиномов
    # Сначала нужно выбрать ближайшие к x nx + 1 значений и ближайшие к y ny + 1 значений
    # построить таблицу из x и z, провести для каждой строчки интреполяцию Ньютона
    # составить таблицу y и полученных значений
    # провести интреполяцию для них (она будет одна)
    def doubleNewtonInter(self, x, y, nx, ny, showComments=False):
        indXStart, indXEnd = findNearestInd(self.x, x, nx)
        indYStart, indYEnd = findNearestInd(self.y, y, ny)

        YTable = []  # результативная таблица "по строкам"
        for k in range(indYStart, indYEnd):
            tableForNewton = [[self.x[i] for i in range(indXStart, indXEnd)],
                              [self.z[x][k] for x in range(indXStart, indXEnd)]]

            tableNewton, polStr, pol = interpolationNewton(tableForNewton, x)
            YTable += [float(pol)]

        # теперь последняя интерполяция по y и YTable
        tableForNewton = [[self.y[i] for i in range(indYStart, indYEnd)], YTable]
        tableNewton, polStr, pol = interpolationNewton(tableForNewton, y)
        return pol


class TripleTable:
    def __init__(self):
        self.z = []     # одномерный массив
        self.xy = []    # одномерный массив из doubleTable

    def inputFromTXTFile(self, filename=FILE_WITH_DOUBLE_TABLE):
        with open(filename, 'r') as fin:
            isInputTable = True
            while isInputTable:
                self.xy.append(DoubleTable())
                self.z.append(float(fin.readline()))
                isInputTable = self.xy[-1].inputFromOpenTXTFile(fin)

    def print(self):
        for i, z in enumerate(self.z):
            print(f'Z = {z}')
            self.xy[i].print()
            print('   ')

    def tripleNewtonInter(self, x, y, z, nx, ny, nz, showComments=False):
        indZStart, indZEnd = findNearestInd(self.z, z, nz)
        if showComments:
            print('indZStart =', indZStart, '; indZEnd =', indZEnd)

        ZTable = []                                     # результативная таблица "по строкам"
        for k in range(indZStart, indZEnd):
            ZTable += [float(self.xy[k].doubleNewtonInter(x, y, nx, ny))]

        if showComments:
            print('ZTable =', ZTable)

        # теперь последняя интерполяция по z и ZTable
        tableForNewton = [[self.z[i] for i in range(indZStart, indZEnd)], ZTable]
        tableNewton, polStr, pol = interpolationNewton(tableForNewton, z)
        return pol

# t = TripleTable()
# t.inputFromTXTFile(r'..\data\t.txt')
#
# print(t.tripleNewtonInter(1.5, 1.5, 1.5, 1, 1, 1, True))

""" Осталось с прошлой лабы
# countEntries -- необходимая степень полинома (то есть будет найдено на 1 значение больше)
def findNearestEntries(table, x, countEntries):
    ansTable = []
    if countEntries >= len(table):
        return tools.NOT_ENOUGH_DATA
    table.sort(key=lambda i: i[0])
    i = 0
    while i < len(table) and table[i][0] < x:
        i += 1
    if i < countEntries // 2 + 1:
        for j in range(countEntries + 1):
            ansTable.append(table[j])
    elif i > len(table) - countEntries:
        for j in range(len(table) - countEntries - 1, len(table)):
            ansTable.append(table[j])
    else:
        for j in range(i - countEntries // 2 - 1 if x != table[i][0] or countEntries % 2 == 1 else i - countEntries // 2,
                       i + countEntries // 2 + 1 if countEntries % 2 == 1 or x == table[i][0] else i + countEntries // 2):
            ansTable.append(table[j])
    return ansTable
def dividedDifferenceHermiteTwo(x1, y1, yDerivative1, x2, y2, yDerivative2):
    if x1 == x2:
        return yDerivative1
    else:
        return (y1 - y2) / (x1 - x2)
def dividedDifferenceHermiteThree(x1, y1, yDerivative1, x2, y2, yDerivative2, x3, y3, yDerivative3):
    return (dividedDifferenceHermiteTwo(x1, y1, yDerivative1, x2, y2, yDerivative2) -
            dividedDifferenceHermiteTwo(x1, y1, yDerivative1, x3, y3, yDerivative3)) / (x1 - x3)
def HermitePolynomial(tableHermite):
    tableHermite.pop(2)                     # удалили столбец с производной
    return NewtonPolynomial(tableHermite)
def interpolationHermite(table, x, degree, printComments=False):
    nearestEntries = findNearestEntries(table, x, degree // 2)
    if nearestEntries == tools.NOT_ENOUGH_DATA:
        return tools.NOT_ENOUGH_DATA
    # теперь эту таблицу нужно раздвоить
    i = 0
    while len(nearestEntries) != degree + 1:
        nearestEntries.insert(i, nearestEntries[i])
        i += 2
    tableHermite = [[i[0] for i in nearestEntries], [i[1] for i in nearestEntries], [i[2] for i in nearestEntries], []]
    # добавили строку y(xi, xj)
    for i in range(len(tableHermite[-2]) - 1):
        tableHermite[-1].append(dividedDifferenceHermiteTwo(tableHermite[0][i], tableHermite[1][i], tableHermite[2][i],
                                                             tableHermite[0][i + 1], tableHermite[1][i + 1], tableHermite[2][i + 1]))
    # работаем дальше также, как в Ньютоне
    j = 2
    while len(tableHermite[-1]) != 1:
        tableHermite.append([(tableHermite[-1][i] - tableHermite[-1][i + 1]) /
                            (tableHermite[0][i] - tableHermite[0][i + j]) for i in range(len(tableHermite[-1]) - 1)])
        j += 1
    polStr = HermitePolynomial(tableHermite.copy())
    pol = ne.evaluate(polStr)
    if printComments:
        printResultTable(tableHermite, "HERMITE TABLE", 'Hermite')
        print('H(x) =', polStr)
        print('-------------------------------------')
        print('H(%2.3f) = %2.5f' % (x, ne.evaluate(polStr)))
        print('-------------------------------------')
    return tableHermite, polStr, pol
def allNewtonInter(table, x, startDegree=1, endDgree=5, printOwnGraph=False, pltGraph=None):
    resX = []
    allDegree = []
    if printOwnGraph:
        pltGraph.figure(figsize=[10, 10])
        pltGraph.suptitle('NewtonPolinom', fontsize=15, fontweight='bold')
        pltGraph.grid(True)
    if pltGraph != None:
        pltGraph.grid(True)
        pltGraph.title.set_text('Newton')
        graph.showGraphUsePoints([table[i][0] for i in range(len(table))], [table[i][1] for i in range(len(table))], pltGraph,
                                 f'start points', 'mo')
    for degree in range(startDegree, endDgree + 1):
        t, p, val = interpolationNewton(table, x, degree, printComments=False)
        resX.append(val)
        if pltGraph != None:
            graph.showGraphUsePol(t, p, pltGraph, f'degree = {degree}', "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]))
            randColor = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            pltGraph.plot(x, val, marker='o', label='%d: (%1.3f, %1.3f)' % (degree, x, val), color=randColor)
            allDegree.append(degree)
    if pltGraph != None:
        pltGraph.legend(loc=0)
    if printOwnGraph:
        pltGraph.legend(loc=0)
        pltGraph.savefig('Newton.svg')
        pltGraph.show()
    return allDegree, resX
def allHermiteInter(table, x, minCountNodes=1, maxCountNodes=3, printOwnGraph=False, pltGraph=plt):
    res = []
    allDegree = []
    if printOwnGraph:
        pltGraph.figure(figsize=[10, 10])
        pltGraph.suptitle('HermitePolinom', fontsize=15, fontweight='bold')
    pltGraph.grid(True)
    pltGraph.title.set_text('Hermite')
    graph.showGraphUsePoints([table[i][0] for i in range(len(table))], [table[i][1] for i in range(len(table))], pltGraph,
                             f'start points', 'mo')
    for degree in range(minCountNodes, maxCountNodes + 1):
        t, p, val = interpolationHermite(table, x, degree * 2 - 1, printComments=False)
        res.append(val)
        if degree != 1:
            randColor = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            graph.showGraphUsePol(t, p, pltGraph, f'count = {degree}', randColor)
        randColor = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        pltGraph.plot(x, val, marker='o', label='%d: (%1.3f, %1.3f)' % (degree, x, val), color=randColor)
        allDegree.append(degree * 2 - 1)
    pltGraph.legend(loc=0)
    if printOwnGraph:
        pltGraph.savefig('Hermite.svg')
        pltGraph.show()
    return allDegree, res
def isRootExist(table):
    for i in range(len(table) - 1):
        if table[i][1] * table[i + 1][1] < 0:
            return True
    return False
def roots(table, degree=3, printComments=False):
    if not isRootExist(table):
        print("No roots")
        return
    newTable = [[table[i][1], table[i][0], table[i][2]] for i in range(len(table))]
    tableNewton, polStr, pol = interpolationNewton(newTable, 0, degree, True)
    return tableNewton, polStr, pol
"""

