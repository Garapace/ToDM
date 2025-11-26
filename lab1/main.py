import math

# константы
EPSILON = 1e-6    # заданная точность 10^-6
DELTA = EPSILON/2 # допустимая погрешность
iterations = 0    # количество итераций для метода


def function(x):
    """ f(x) = x^2/2 - cos(x) """
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


def method_tangent(a, b):
    """ Метод касательных """
    global iterations
    iterations = 0
    xm = 0

    while abs(b - a) > EPSILON:
        fa, fb = function(a), function(b)
        dfa, dfb = function_first_derivative(a), function_first_derivative(b)
        xm = (a * dfa - b * dfb - fa + fb) / (dfa - dfb)

        if function_first_derivative(xm) > 0:
            b = xm
        else:
            a = xm

        iterations += 1

    return xm


def method_newton(a):
    """ Метод Ньютона """
    global iterations
    iterations = 0
    x0 = a

    while True:
        xk = x0 - function_first_derivative(x0) / function_second_derivative(x0)
        if abs(xk - x0) < EPSILON and abs(function(xk) - function(x0)) < EPSILON:
            break
        x0 = xk
        iterations += 1

    return xk


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
    x_min2 = method_tangent(a, b)
    min_f2 = function(x_min2)
    print("Минимум функции f(x) = x^2/2 - cos(x) | метод касательных")
    print(f"Xmin =\t\t\t\t{x_min2}")
    print(f"Минимальное значение функции:\t{min_f2}")
    print(f"Количество итераций:\t\t{iterations}\n")
    
    # --- метод деления отрезка пополам ---
    x_min3 = method_newton(a)
    min_f3 = function(x_min3)
    print("Минимум функции f(x) = x^2/2 - cos(x) | метод ньютона")
    print(f"Xmin =\t\t\t\t{x_min3}")
    print(f"Минимальное значение функции:\t{min_f3}")
    print(f"Количество итераций:\t\t{iterations}\n")


if __name__ == "__main__":
    main()
