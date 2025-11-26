import math

# константы
EPSILON = 1e-6    # заданная точность 10^-6
DELTA = EPSILON/2 # допустимая погрешность
iterations = 0    # количество итераций для метода


def function(x):
    """ f(x) = -x^3 + 3(1 + x)(ln(x + 1) - 1) """
    return (-x**3 + 3*(1 + x) * (math.log(x + 1) - 1))


def function_first_derivative(x):
    """ Первая производная f'(x) """
    return 3 * math.log(x + 1) - 3 * x ** 2


def function_second_derivative(x):
    """ Вторая производная f''(x)"""
    return 3 / (x + 1) - 6 * x


def method_dichotomy(a, b):
    """ Метод деления пополам (метод бисекции | метод дихотомии) """
    global iterations
    iterations = 0

    while abs(b - a) > EPSILON:
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
    a = -0.5
    b = 0.5

    # --- Метод деления пополам ---
    x_min1 = method_dichotomy(a, b)
    min_f1 = function(x_min1)
    print("Минимум функции f(x) = -x^3 + 3(1+x)(ln(x+1)-1). Метод деления пополам.")
    print(f"Xmin = {x_min1}")
    print(f"Минимальное значение функции: {min_f1}")
    print(f"Количество итераций: {iterations}\n")

    # --- Метод касательных ---
    x_min2 = method_tangent(a, b)
    min_f2 = function(x_min2)
    print("Минимум функции f(x) = -x^3 + 3(1+x)(ln(x+1)-1). Метод касательных.")
    print(f"Xmin = {x_min2}")
    print(f"Минимальное значение функции: {min_f2}")
    print(f"Количество итераций: {iterations}\n")

    # --- Метод Ньютона ---
    x_min3 = method_newton(a)
    min_f3 = function(x_min3)
    print("Минимум функции f(x) = -x^3 + 3(1+x)(ln(x+1)-1). Метод Ньютона.")
    print(f"Xmin = {x_min3}")
    print(f"Минимальное значение функции: {min_f3}")
    print(f"Количество итераций: {iterations}\n")


if __name__ == "__main__":
    main()
