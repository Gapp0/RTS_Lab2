# Лабораторна робота №2
# Студент групи ІО-71 Єрмоленко В.Р.
#
# Варіант | Число гармонік n | Гранична частота Wгр | Кількість дискретних відліків N
#   06    |         14       |         2000         |             256

from random import uniform
from math import sin
import matplotlib.pyplot as plt
import datetime
import numpy as np

NHARMONIC = 14
LIMFREQ = 2000
NTICKS = 256

# a:  ---/\/\/\/\-------\/\/\/\
# b:  /\/--------/\/\/\/-------
# Rab, Rba, Raa

VARIANT = 3


def correlate_old(x_list, y_list):
    r_list = [0 for i in range(len(x_list))]
    Mx, My = get_M(x_list), get_M(y_list)
    for t in range(len(x_list)):
        r_list[t] = sum((x_list[i] - Mx)*(y_list[i + t] - My) for i in range(len(x_list) - t))/(len(x_list) - 1)
    return r_list


def correalte_real(x_list, y_list):
    #r_list = []
    Mx, My = get_M(x_list), get_M(y_list)
    for t in range(len(x_list)):
        #r_list.append(sum((x_list[i] - Mx)*(y_list[i + t] - My) for i in range(len(x_list) - t))/(len(x_list) - 1))
        yield sum((x_list[i] - Mx)*(y_list[i + t] - My) for i in range(len(x_list) - t))/(len(x_list) - 1)


# public static float[] cor(float[] x, float[] y) {
#         float R[] = new float[x.length / 2];
#         float Mx = expectation(x);
#         float My = expectation(y);
#         for (int t = 0; t < x.length / 2 - 1; t++) {
#             R[t] = 0;
#             for (int i = 0; i < x.length / 2 - 1; i++) {
#                 R[t] += (x[i] - Mx) * (y[i + t] - My);
#             }
#             R[t] /= (x.length - 1);
#             t++;
#         }
#         return R;
#     }

def correlate(x_list, y_list):
    R = [0] * (len(x_list) // 2)
    Mx, My = get_M(x_list), get_M(y_list)

    for t in range(len(x_list) // 2 - 1):
        #R[t] = 0
        for i in range(len(x_list) // 2 - 1):
            R[t] += (x_list[i] - Mx) * (y_list[i + t] - My)
        R[t] /= (len(x_list) - 1)

    return R


def do_plot(a_list):
    plt.plot([i for i in range(len(a_list))], a_list)
    plt.axis([0, len(a_list), min(a_list), max(a_list)])
    plt.show()



def getharm(t):
    x = 0
    for i in range(NHARMONIC):
        x += uniform(0, 1) * sin(LIMFREQ * (i / NHARMONIC) * t + uniform(0, 1))
    return x


def get_x_list(LEN):
    return [getharm(i) for i in range(LEN)]


def get_D(x_list, M_x):
    return sum((x_list[t] - M_x)**2 for t in range(len(x_list))) / (len(x_list) - 1)


def get_M(x_list):
    return sum(x_list) / len(x_list)


def do500to2500():
    x_list = [0] * 500
    for t in range(500):
        for i in range(NHARMONIC):
            x_list[t] += uniform(0, 1) * sin(LIMFREQ * (i / NHARMONIC) * t + uniform(0, 1))
    D_list = []
    for i in range(2500-500+1):
        D_list.append(get_D(x_list, get_M(x_list)))
        x_list.append(getharm(i))
    plt.plot([i for i in range(500, 2500+1)], D_list)
    plt.show()


    # a:  -------/\/\/\/\-------\/\/\/\
    # b:  /\/\/\/--------/\/\/\/-------
    # Rab, Rba, Raa

    x_list = get_x_list(NTICKS)
    y_list = get_x_list(NTICKS)

    quarter = NTICKS // 4
    for i in range(NTICKS):
        if (i <= NTICKS // 4) or (NTICKS // 2 < i <= 3 * NTICKS // 4):
            # Первая или третья четверть
            y_list[i] = 0
        elif (NTICKS // 4 < i <= NTICKS // 2) or (i > 3 * NTICKS // 4):
            # Вторая или четвёртая четверть
            x_list[i] = 0

    cor_xy = correlate(x_list, y_list)
    plt.plot([x for x in range(len(cor_xy))], cor_xy)
    plt.title("Rxy")
    plt.show()
    cor_yx = correlate(y_list, x_list)
    plt.plot([x for x in range(len(cor_xy))], cor_yx)
    plt.title("Ryx")
    plt.show()
    cor_xx = correlate(x_list, x_list)
    plt.plot([x for x in range(len(cor_xy))], cor_xx)
    plt.title("Rxx")
    plt.show()
