# константы
import math


EPSILON = 1e-6    # заданная точность 10^-6
DELTA = EPSILON/2 # допустимая погрешность
iterations = 0    # количество итераций для метода

def function(x):
    """ f(x) = x^2/2 - cos(x)   """
    return x**2/2 - math.cos(x)

def function_first_derivative(x):
    """ Первая произодная функции
        f(x)  = x^2/2 - cos(x)
        f'(x) = sin(x) + x      """
    return math.sin(x) + x

def function_second_derivative(x):
    """ Вторая производная функции
        f(x)   = x^2/2 - cos(x)
        f''(x) = cos(x) + 1     """
    return math.cos(x) + 1

def method_dichotomy(a, b):
    """ Метод деления пополам (метод бисекции | метод дихотомии)"""
    global iterations
    iterations = 0
    
    while (abs(b - a) > EPSILON):
        x1 = (a + b - DELTA) / 2
        x2 = (a + b + DELTA) / 2
        
        if function(x1) >= function(x2):
            a = x1
        else:
            b = x2
        iterations += 1
    
    return (a + b) / 2

def method_dichotomy(a, b):
    """ Метод деления пополам (метод бисекции | метод дихотомии)"""
    global iterations
    iterations = 0
    
    while (abs(b - a) > EPSILON):
        x1 = (a + b - DELTA) / 2
        x2 = (a + b + DELTA) / 2
        
        if function(x1) >= function(x2):
            a = x1
        else:
            b = x2
        iterations += 1
    
    return (a + b) / 2
def method_dichotomy(a, b):
    """ Метод деления пополам (метод бисекции | метод дихотомии)"""
    global iterations
    iterations = 0
    
    while (abs(b - a) > EPSILON):
        x1 = (a + b - DELTA) / 2
        x2 = (a + b + DELTA) / 2
        
        if function(x1) >= function(x2):
            a = x1
        else:
            b = x2
        iterations += 1
    
    return (a + b) / 2


def main():
    a = 0
    b = 3
    
    # --- метод деления отрезка пополам ---
    x_min1 = method_dichotomy(a, b)
    min_f1 = function(x_min1)
    print("Минимум функции f(x) = x^2/2 - cos(x) | метод деления отрезка пополам")
    print(f"Xmin =\t\t\t\t{x_min1}")
    print(f"Минимальное значение функции:\t{min_f1}")
    print(f"Количество итераций:\t\t{iterations}\n")
    
    # --- метод деления отрезка пополам ---
    x_min1 = method_dichotomy(a, b)
    min_f1 = function(x_min1)
    print("Минимум функции f(x) = x^2/2 - cos(x) | метод деления отрезка пополам")
    print(f"Xmin =\t\t\t\t{x_min1}")
    print(f"Минимальное значение функции:\t{min_f1}")
    print(f"Количество итераций:\t\t{iterations}\n")
    
    # --- метод деления отрезка пополам ---
    x_min1 = method_dichotomy(a, b)
    min_f1 = function(x_min1)
    print("Минимум функции f(x) = x^2/2 - cos(x) | метод деления отрезка пополам")
    print(f"Xmin =\t\t\t\t{x_min1}")
    print(f"Минимальное значение функции:\t{min_f1}")
    print(f"Количество итераций:\t\t{iterations}\n")


if __name__ == "__main__":
    main()
