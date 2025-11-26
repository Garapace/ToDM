import math

EPSILON = 1e-6
iterations = 0


def function(x1, x2):
    """f(x1, x2) = x1^2 + 3 x2^2 + cos(x1 + x2)"""
    return x1**2 + 3 * x2**2 + math.cos(x1 + x2)


def gradient(x1, x2):
    """Градиент функции"""
    df_dx1 = 2 * x1 - math.sin(x1 + x2)
    df_dx2 = 6 * x2 - math.sin(x1 + x2)
    return [df_dx1, df_dx2]


def first_method(x):
    """Градиентный метод с постоянным шагом"""
    global iterations
    iterations = 0

    lambda_step = 0.7
    f_x = function(x[0], x[1])

    while True:
        grad = gradient(x[0], x[1])
        x_new = [x[0] - lambda_step * grad[0],
                 x[1] - lambda_step * grad[1]]

        f_new = function(x_new[0], x_new[1])

        if f_new > f_x:
            lambda_step /= 2

        x = x_new

        if abs(f_new - f_x) < EPSILON:
            break

        f_x = f_new
        iterations += 1

    return x


def second_method(xb):
    """Метод Хука–Дживса"""
    global iterations
    iterations = 0

    lambda_step = 0.1
    alpha = 2.0

    x = xb[:]
    fxb = function(xb[0], xb[1])

    while lambda_step > EPSILON:
        iterations += 1

        x_min = xb[:]
        found = False

        # исследующий поиск
        for i in range(2):
            x_pos = x_min[:]
            x_neg = x_min[:]

            x_pos[i] += lambda_step
            x_neg[i] -= lambda_step

            if function(x_pos[0], x_pos[1]) < fxb:
                fxb = function(x_pos[0], x_pos[1])
                x_min = x_pos[:]
                found = True

            elif function(x_neg[0], x_neg[1]) < fxb:
                fxb = function(x_neg[0], x_neg[1])
                x_min = x_neg[:]
                found = True

        if found:
            # шаг по образцу
            x_new = [
                x_min[i] + alpha * (x_min[i] - xb[i])
                for i in range(2)
            ]

            f_new = function(x_new[0], x_new[1])

            if f_new < fxb:
                xb = x_new
                fxb = f_new
            else:
                xb = x_min
        else:
            lambda_step /= 2

    return xb


def main():
    x0_1 = [1.0, 1.0]
    x0_2 = [1.0, 1.0]

    # --- метод Хука–Дживса ---
    x_min2 = second_method(x0_2)
    fx_min2 = function(x_min2[0], x_min2[1])
    print("Минимум функции f(x1, x2) = x1^2 + 3x2^2 + cos(x1 + x2) | Метод Хука–Дживса.")
    print(f"Точка минимума:\t\t\t({x_min2[0]}, {x_min2[1]})")
    print(f"Значение в точке минимума:\t{fx_min2}")
    print(f"Количество итераций:\t\t{iterations}")
    
    print()
    
    # --- метод гадиента с постоянным шагом ---
    x_min1 = first_method(x0_1)
    fx_min1 = function(x_min1[0], x_min1[1])
    print("Минимум функции f(x1, x2) = x1^2 + 3x2^2 + cos(x1 + x2) | Метод Хука–Дживса.")
    print(f"Точка минимума:\t\t\t({x_min1[0]}, {x_min1[1]})")
    print(f"Значение в точке минимума:\t{fx_min1}")
    print(f"Количество итераций:\t\t{iterations}")


if __name__ == "__main__":
    main()
