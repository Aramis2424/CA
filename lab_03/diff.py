def read_table_():
    table = open('table.txt', 'r')
    data = []
    table.readline()
    for line in table:
        points = line.split()
        data.append([float(points[0]), float(points[1])])
    data.sort()
    count = len(data) - 1
    arr_x = []
    arr_y = []
    for i in range(len(data)):
        arr_x.append(data[i][0])
        arr_y.append(data[i][1])
    table.close()
    return data, arr_x, arr_y, count


def find_index_interval(data, n, in_x):
    count = 0
    while in_x > data[count][0]:
        count += 1

    start = count - n // 2 - 1
    end = count + (n // 2) + (n % 2) - 1

    if end > len(data) - 1:
        start -= end - len(data) + 1
        end = len(data) - 1
    elif start < 0:
        end += -start
        start = 0
    return start, end


def separated_diff(x, y, count):
    diff = []
    for i in range(count):
        diff.append([0] * (count + 1))
    for i in range(count):
        diff[i][0], diff[i][1] = x[i], y[i]

    i = 2
    add_count = count - 1

    while i < (count + 1):
        j = 0
        while j < add_count:
            diff[j][i] = round((diff[j + 1][i - 1] - diff[j][i - 1]) / (diff[i - 1][0] - diff[0][0]), 5)
            j += 1
        i += 1
        add_count -= 1

    return diff


def polinom_Newton(x, y, count, in_x):
    diff = separated_diff(x, y, count)
    pol = diff[0][3] * 2 + 3 * diff[0][4] * in_x - diff[0][4] * 2 * diff[0][0] - diff[0][4] * 6 * diff[1][0]
    return pol


def mif(x):
    data, arr_x, arr_y, count = read_table_()

    flag = False

    if not flag:
        x0, xn = find_index_interval(data, 3, x)

        ax = arr_x[x0: xn + 1]
        ay = arr_y[x0: xn + 1]

        root_Newton = polinom_Newton(ax, ay, 3 + 1, x)

    return root_Newton
