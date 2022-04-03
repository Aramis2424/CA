class Coefs_string:
    def __init__(self, x, y, a=None, b=None, c=None, d=None, h=None, f=None, E=None, n=None):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.h = h
        self.f = f
        self.E = E
        self.n = n

    def h_calc(self, prev_str=None):
        if prev_str:
            self.h = self.x - prev_str.x

    def E_calc(self, prev=None, prev_prev=None):
        if prev_prev:
            self.E = -(prev.h / (prev_prev.h * prev.E + 2 * (prev_prev.h + prev.h)))

    def f_calc(self, prev=None, prev_prev=None):
        if prev and prev_prev:
            self.f = 3 * ((self.y - prev.y) / self.h - (prev.y - prev_prev.y) / prev.h)

    def n_calc(self, prev=None, prev_prev=None):
        if prev_prev:
            self.n = (prev.f - prev_prev.h * prev.n) \
                     / (prev_prev.h * prev.E + 2 * (prev_prev.h + prev.h))

    def c_calc(self, prev=None, next=None):
        if prev and next:
            self.c = -self.h * next.c / (prev.h * self.E + 2 * (prev.h + self.h)) + \
                     (self.f - prev.h * self.n) / (prev.h * self.E + 2 * (prev.h + self.h))

    def a_calc(self, prev=None):
        if prev:
            self.a = prev.y

    def b_calc(self, prev=None, next=None):
        if prev and next:
            self.b = (self.y - prev.y) / self.h - self.h * (next.c + 2 * self.c) / 3

    def d_calc(self, next=None):
        if next:
            self.d = (next.c - self.c) / (3 * self.h)
