import math

# Константы
EPSILON = 1e-6
DELTA = EPSILON / 2
iter_count = 0


def function(x):
    """f(x) = -x^3 + 3(1 + x)(ln(x + 1) - 1)"""
    return (-x**3 + 3*(1 + x) * (math.log(x + 1) - 1))


def dev_function(x):
    """Первая производная f'(x)"""
    return 3 * math.log(x + 1) - 3 * x ** 2


def dev_sec_function(x):

    """Вторая производная f''(x)"""
    return 3 / (x + 1) - 6 * x


def first_method(a, b):
    """Метод деления пополам"""
    global iter_count
    iter_count = 0

    while abs(b - a) > EPSILON:
        x1 = (a + b - DELTA) / 2
        x2 = (a + b + DELTA) / 2

        if function(x1) >= function(x2):
            a = x1
        else:
            b = x2
        iter_count += 1

    return (a + b) / 2


def second_method(a, b):
    """Метод касательных"""
    global iter_count
    iter_count = 0
    xm = 0

    while abs(b - a) > EPSILON:
        fa, fb = function(a), function(b)
        dfa, dfb = dev_function(a), dev_function(b)
        xm = (a * dfa - b * dfb - fa + fb) / (dfa - dfb)

        if dev_function(xm) > 0:
            b = xm
        else:
            a = xm

        iter_count += 1

    return xm


def third_method(a):
    """Метод Ньютона"""
    global iter_count
    iter_count = 0
    x0 = a

    while True:
        xk = x0 - dev_function(x0) / dev_sec_function(x0)
        if abs(xk - x0) < EPSILON and abs(function(xk) - function(x0)) < EPSILON:
            break
        x0 = xk
        iter_count += 1

    return xk


def main():
    a = -0.5
    b = 0.25

    # --- Метод деления пополам ---
    x_min1 = first_method(a, b)
    min_f1 = function(x_min1)
    print("Минимум функции f(x) = -x^3 + 3(1+x)(ln(x+1)-1). Метод деления пополам.")
    print(f"Xmin = {x_min1}")
    print(f"Минимальное значение функции: {min_f1}")
    print(f"Количество итераций: {iter_count}\n")

    # --- Метод касательных ---
    x_min2 = second_method(a, b)
    min_f2 = function(x_min2)
    print("Минимум функции f(x) = -x^3 + 3(1+x)(ln(x+1)-1). Метод касательных.")
    print(f"Xmin = {x_min2}")
    print(f"Минимальное значение функции: {min_f2}")
    print(f"Количество итераций: {iter_count}\n")

    # --- Метод Ньютона ---
    x_min3 = third_method(a)
    min_f3 = function(x_min3)
    print("Минимум функции f(x) = -x^3 + 3(1+x)(ln(x+1)-1). Метод Ньютона.")
    print(f"Xmin = {x_min3}")
    print(f"Минимальное значение функции: {min_f3}")
    print(f"Количество итераций: {iter_count}\n")


if __name__ == "__main__":
    main()
