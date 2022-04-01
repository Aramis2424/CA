# encoding:utf-8
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
"""
Реализация кубического сплайна
"""
x = [3, 4.5, 7, 9]
y = [2.5, 1, 2.5, 0.5]

def calculateEquationParameters(x):
    #parameter - это двумерный массив, используемый для хранения параметров, sizeOfInterval - для хранения количества интервалов
    parameter = []
    sizeOfInterval=len(x)-1;
    i = 1
    # Сначала введите уравнение с равными значениями функций в соседних узлах с обеих сторон уравнения как 2n-2 уравнения
    while i < len(x)-1:
        data = init(sizeOfInterval*4)
        data[(i-1)*4] = x[i]*x[i]*x[i]
        data[(i-1)*4+1] = x[i]*x[i]
        data[(i-1)*4+2] = x[i]
        data[(i-1)*4+3] = 1
        data1 =init(sizeOfInterval*4)
        data1[i*4] =x[i]*x[i]*x[i]
        data1[i*4+1] =x[i]*x[i]
        data1[i*4+2] =x[i]
        data1[i*4+3] = 1
        temp = data[2:]
        parameter.append(temp)
        temp = data1[2:]
        parameter.append(temp)
        i += 1
    # Введите значение функции в конечной точке. Два уравнения плюс предыдущие 2n-2 уравнения, всего 2n уравнений
    data = init(sizeOfInterval * 4 - 2)
    data[0] = x[0]
    data[1] = 1
    parameter.append(data)
    data = init(sizeOfInterval * 4)
    data[(sizeOfInterval - 1) * 4 ] = x[-1] * x[-1] * x[-1]
    data[(sizeOfInterval - 1) * 4 + 1] = x[-1] * x[-1]
    data[(sizeOfInterval - 1) * 4 + 2] = x[-1]
    data[(sizeOfInterval - 1) * 4 + 3] = 1
    temp = data[2:]
    parameter.append(temp)
    # Значение первой производной функции конечной точки равно n-1 уравнениям. Добавьте предыдущие уравнения к 3n-1 уравнениям.
    i=1
    while i < sizeOfInterval:
        data = init(sizeOfInterval * 4)
        data[(i - 1) * 4] = 3 * x[i] * x[i]
        data[(i - 1) * 4 + 1] = 2 * x[i]
        data[(i - 1) * 4 + 2] = 1
        data[i * 4] = -3 * x[i] * x[i]
        data[i * 4 + 1] = -2 * x[i]
        data[i * 4 + 2] = -1
        temp = data[2:]
        parameter.append(temp)
        i += 1
    # Значение второй производной функции конечной точки равно n-1 уравнениям. Добавьте предыдущие уравнения к 4n-2 уравнениям. И вторая производная от значения функции в конечной точке равна нулю, что является двумя уравнениями. Всего имеется 4n уравнений.
    i = 1
    while i < len(x) - 1:
        data = init(sizeOfInterval * 4)
        data[(i - 1) * 4] = 6 * x[i]
        data[(i - 1) * 4 + 1] = 2
        data[i * 4] = -6 * x[i]
        data[i * 4 + 1] = -2
        temp = data[2:]
        parameter.append(temp)
        i += 1
    return parameter



"""
 Инициализировать размер кортежа равным 0
"""
def init(size):
    j = 0
    data = []
    while j < size:
        data.append(0)
        j += 1
    return data

"""
 Функция: вычислить коэффициент сплайн-функции.
 Параметры: параметры - это коэффициент уравнения, а y - зависимая переменная функции, которую нужно интерполировать.
 Возвращаемое значение: коэффициент функции кубической интерполяции.
"""
def solutionOfEquation(parametes,y):
    sizeOfInterval = len(x) - 1
    result = init(sizeOfInterval*4-2)
    i=1
    while i<sizeOfInterval:
        result[(i-1)*2]=y[i]
        result[(i-1)*2+1]=y[i]
        i+=1
    result[(sizeOfInterval-1)*2]=y[0]
    result[(sizeOfInterval-1)*2+1]=y[-1]
    a = np.array(calculateEquationParameters(x))
    b = np.array(result)
    for data_x in b:
        print(data_x)
    return np.linalg.solve(a,b)

"""
 Функция: По заданным параметрам вычислить значение функции кубической функции:
 Параметры: параметры - это коэффициенты квадратичной функции, x - независимая переменная.
 Возвращаемое значение: зависимая переменная функции
"""
def calculate(paremeters,x):
    result=[]
    for data_x in x:
        result.append(paremeters[0]*data_x*data_x*data_x+paremeters[1]*data_x*data_x+paremeters[2]*data_x+paremeters[3])
    return  result


"""
 Функция: нарисовать функцию в изображении
 Параметры: data_x, data_y - дискретные точки. New_data_x, new_data_y - значения, вычисленные функцией интерполяции Лагранжа. x - прогнозируемое значение функции.
 Возвращаемое значение: пусто
"""
def  Draw(data_x,data_y,new_data_x,new_data_y):
        plt.plot(new_data_x, new_data_y, label=u"Подгонка кривой", color="black")
        plt.scatter(data_x,data_y, label=u"Дискретные данные",color="red")
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['axes.unicode_minus'] = False
        plt.title(u"Функция кубического сплайна")
        plt.legend(loc="upper left")
        plt.show()


result=solutionOfEquation(calculateEquationParameters(x),y)
new_data_x1=np.arange(3, 4.5, 0.1)
new_data_y1=calculate([0,0,result[0],result[1]],new_data_x1)
new_data_x2=np.arange(4.5, 7, 0.1)
new_data_y2=calculate([result[2],result[3],result[4],result[5]],new_data_x2)
new_data_x3=np.arange(7, 9.5, 0.1)
new_data_y3=calculate([result[6],result[7],result[8],result[9]],new_data_x3)
new_data_x=[]
new_data_y=[]
new_data_x.extend(new_data_x1)
new_data_x.extend(new_data_x2)
new_data_x.extend(new_data_x3)
new_data_y.extend(new_data_y1)
new_data_y.extend(new_data_y2)
new_data_y.extend(new_data_y3)
Draw(x,y,new_data_x,new_data_y)