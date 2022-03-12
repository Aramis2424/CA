from model.TripleTable import *


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

def menu():
    print("Menu:\n"
          "    0 - EXIT\n"
          "    1 - input table from file\n"
          "    2 - perform interpolation\n"
          "    3 - print table with data")
    return input("Input command: ")


if __name__ == '__main__':
    mode = menu()
    table = TripleTable()
    while mode != MODE_EXIT:
        if mode == MODE_INPUT_FROM_FILE:
            try:
                filename = input(r"Input filename with data or 1 if you want to use data\t.txt): ")
                table.inputFromTXTFile(filename if filename != '1' else r'data\t.txt')
                print("INPUT DATA ---> SUCCESS")
            except FileNotFoundError:
                print('Error with filename')
            except ValueError:
                print('Error with data in file')

        elif mode == MODE_PRINT_TABLE:
            table.print()

        elif mode == MODE_INTERPOLATION:
            try:
                x = float(input('Input x [float]: '))
                y = float(input('Input y [float]: '))
                z = float(input('Input z [float]: '))
                nx = int(input('Input x degree (nx) [int]: '))
                ny = int(input('Input y degree (ny) [int]: '))
                nz = int(input('Input z degree (nz) [int]: '))
            except:
                print('Invalid input')
                mode = menu()
                continue
            res = table.tripleNewtonInter(x, y, z, nz, ny, nz, True)
            print('Res =', res)

        mode = menu()

