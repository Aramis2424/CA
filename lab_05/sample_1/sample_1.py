from matplotlib.pyplot import *

def run_method(a, b, c, f):
    alpha = [c[0] / b[0]]
    beta = [f[0] / b[0]]
    n = len(f)
    x = [0 for _ in range(n)]

    for i in range(1, n):
        alpha.append(c[i] / (-a[i] * alpha[i - 1] + b[i]))
        beta.append((f[i] + a[i] * beta[i - 1]) / (-a[i] * alpha[i - 1] + b[i]))

    x[n - 1] = beta[-1]

    for i in range(n-1, 0, -1):
        x[i - 1] = alpha[i] * x[i] + beta[i]

    return x

def k_func(x, a = 0.0134, b = 1, c = 4.35e-4, m = 1):
    f = a * (b + c *(x ** m))
    return f

def p_func(x, r = 0.5):
    f = 2 / r * alpha_func(x)
    return f

def alpha_func(x, a = 1.94e-2, d = 1.5e3, g = 0.2e-2):
    f = a * ((x / d - 1) ** 4) + g
    return f

def f_func(x, t = 300):
    f = t * p_func(x)
    return f

def dk_func(x, a = 0.0134, c = 4.35e-4, m = 1):
    f = a * c * m * (x ** (m - 1))
    return f

def dp_func(x, r = 0.5, a = 1.94e-2, d = 1.5e3, g = 0.2e-2):
    f = (8 * a) / (d * r) * ((x / d - 1) ** 3)
    return f

def df_func(x, t = 300):
    f = t * dp_func(x)
    return f

def run_coefs(y, h, f0, t):
    a, b, c, d = [], [], [], []
    a_coef = 0
    a.append(a_coef)
    c_coef = (k_func(y[0]) + k_func(y[1])) / 2
    c.append(c_coef)
    b_coef = c_coef + p_func(y[0]) * h * h
    b.append(b_coef)
    d_coef = f_func(y[0]) * h * h + f0 * h
    d.append(d_coef)

    for i in range(1, len(y) - 1):
        a_coef = (k_func(y[i - 1]) + k_func(y[i])) / 2
        a.append(a_coef)
        c_coef = (k_func(y[i]) + k_func(y[i + 1])) / 2
        c.append(c_coef)
        b_coef = a_coef + c_coef + p_func(y[i]) * h * h
        b.append(b_coef)
        d_coef = f_func(y[i]) * h * h
        d.append(d_coef)

    a_coef = (k_func(y[-2]) + k_func(y[-1])) / 2
    a.append(a_coef)
    c_coef = 0
    c.append(c_coef)
    b_coef = a_coef + p_func(y[-1]) * h * h + alpha_func(y[-1]) * h
    b.append(b_coef)
    d_coef = f_func(y[-1]) * h * h + alpha_func(y[-1]) * h * t
    d.append(d_coef)
    return a, b, c, d

def d_run_coefs(y, a, b, c, d, h):
    a1, b1, c1, d1 = [], [], [], []
    kip = dk_func(y[0 + 1]) / 2
    ki = dk_func(y[0]) / 2
    a_coef = 0
    a1.append(a_coef)
    b_coef = -(ki + h * h * dp_func(y[0])) * y[0] - b[0] + ki * y[1] + df_func(y[0]) * h * h
    b1.append(b_coef)
    c_coef = kip * y[0] + kip * y[1] + c[0]
    c1.append(c_coef)
    d_coef = -b[0] * y[0] + c[0] * y[1] + d[0] 
    d1.append(d_coef)

    for i in range(1, len(y) - 1):
        kim = dk_func(y[i - 1]) / 2
        kip = dk_func(y[i + 1]) / 2
        ki = dk_func(y[i]) / 2
        a_coef = kim * y[i - 1] + a[i] - kim * y[i]
        a1.append(a_coef)
        b_coef = ki * y[i - 1] - (2 * ki + h * h * dp_func(y[i])) * y[i] - b[i] + ki * y[i + 1] + df_func(y[i]) * h * h
        b1.append(b_coef)
        c_coef = kip * y[i] + kip * y[i + 1] + c[i]
        c1.append(c_coef)
        d_coef = a[i] * y[i - 1] - b[i] * y[i] + c[i] * y[i + 1] + d[i] 
        d1.append(d_coef)

    kim = dk_func(y[-1 - 1]) / 2
    ki = dk_func(y[-1]) / 2
    a_coef = kim * y[-2] + a[-1] - kim * y[-1]
    a1.append(a_coef)
    b_coef = ki * y[-2] - (ki + h * h * dp_func(y[-1])) * y[-1] - b[-1] + df_func(y[-1]) * h * h
    b1.append(b_coef)
    c_coef = 0
    c1.append(c_coef)
    d_coef = a[-1] * y[-2] - b[-1] * y[-1] + d[-1] 
    d1.append(d_coef)
    return a1, b1, c1, d1

def solution(f0, t0, l, n):
    h = l / n
    y = []
    for _ in range(n):
        y.append(t0)
    if abs(f0) < 1e-3:
        return y
    max_e = 10
    while max_e > 0.05:
        a, b, c, d = run_coefs(y, h, f0, t0)
        y = run_method(a, b, c, d)
        a1, b1, c1, d1 = d_run_coefs(y, a, b, c, d, h)
        b1 = list(map(lambda x: -x, b1))
        delta_y = run_method(a1, b1, c1, d1)
        # print(delta_y)
        max_e = abs(delta_y[0] / y[0])
        for i in range(len(delta_y)):
            e = abs(delta_y[i] / y[i])
            if max_e < e:
                max_e = e
        for i in range(len(delta_y)):
            y[i] += delta_y[i]
    return y

def main():
    n = 100
    f0 = 0.01
    t0 = 300
    l = 10
    y = solution(f0, t0, l, n)
    h = l / n
    x = [i * h for i in range(n)]
    print(y)
    plot(x, y)
    #ylim(bottom=0)
    show()

main()
