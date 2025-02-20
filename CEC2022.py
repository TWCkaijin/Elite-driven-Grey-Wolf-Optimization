import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import math
from mpl_toolkits.mplot3d import Axes3D

import warnings
warnings.filterwarnings('ignore')


def bent_cigar_function(x, y):
    return x**2 + 1e6 * y**2

def rastrigin_function(x, y, A=10):
    return 2*A + x**2 - A*np.cos(2*np.pi*x) + y**2 - A*np.cos(2*np.pi*y)

def high_conditioned_elliptic_function(x):
    a = 1e6
    d = len(x)
    return np.sum([a**((i-1)/(d-1))*(x[i]**2) for i in range(d)])

def hgbat_function(x):
    a = [-10, -5]
    term1 = np.sum((x - a) ** 2) ** 2
    term2 = np.sum(x - a) ** 2 / 1e6
    return term1 + term2

def rosenbrock_function(x, y):
    return (x-1)**2 + 10*(y-x**2)**2

def griewank_function(x1, x2):
    return (x1 ** 2 + x2 ** 2)/4000.0 - math.cos(x1) * math.cos(x2 / math.sqrt(2)) + 1.0

def ackley_function(x, y):
    term1 = -20.0 * np.exp(-0.2 * np.sqrt(0.5 * (x**2 + y**2)))
    term2 = -np.exp(0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y)))
    term3 = np.exp(1) + 20.0
    return term1 + term2 + term3


if __name__ == '__main__':
    UBX = 0 #eval(input("upper bound"))
    LBX = -2 #eval(input("lower bound"))

    UBY = 2#eval(input("upper bound"))
    LBY = 0 #eval(input("lower bound"))

    X, Y = np.meshgrid(np.arange(LBX, UBX, 0.5), np.arange(LBY, UBY, 0.5))
    function_name = ["bent_cigar_function","rastrigin_function","high_conditioned_elliptic_function",
                "hgbat_function","rosenbrock_function","griewank_function","ackley_function"]

    for i in range(len(function_name)):
        print(f"{i+1}.{function_name[i]}")
    f_index = int(input("Input function index:"))
    match (f_index):
        case 1:
            Z = np.vectorize(bent_cigar_function)(X, Y)

        case 2:
            Z = np.vectorize(rastrigin_function)(X, Y)

        case 3:
            Z = np.zeros_like(X)
            for i in range(len(X)):
                for j in range(len(Y)):
                    point = [X[i, j], Y[i, j]]
                    Z[i, j] = high_conditioned_elliptic_function(point)

        case 4:
            Z = np.zeros((len(X), len(Y)))
            for i in range(len(X)):
                for j in range(len(Y)):
                    Z[i][j] = hgbat_function(np.array([X[i][j], Y[i][j]]))

        case 5:
            Z = np.vectorize(rosenbrock_function)(X, Y)

        case 6:
            Z = np.zeros((len(X), len(Y)))
            for ii in range(len(X)):
                for jj in range(len(Y)):
                    Z[ii,jj] = griewank_function(X[ii,jj], Y[ii,jj])

        case 7:
            Z = ackley_function(X, Y)

        case _:
            print("Function not found")
            exit()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap='plasma')
    fig.colorbar(surf, shrink=0.5, aspect=5)
    #plt.show()

    combined = np.stack((X, Y, Z), axis=-1)

    np.save(f"{function_name[f_index-1]}.npy", combined)