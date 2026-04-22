import numpy as np
import matplotlib.pyplot as plt


def f(x):
    """Целевая функция: f(x) = x1² + 3x2² + cos(x1 + x2)"""
    return x[0] ** 2 + 3 * x[1] ** 2 + np.cos(x[0] + x[1])


def g(x):
    return 2*x[0] + 2*x[1] + 3

def P(x, A=2, q=3):
    g_x = g(x)
    return A * (g_x ** q) if g_x > 0 else 0


def penalty_function(x, A=2, q=3):
    return f(x) + P(x, A, q)


# Метод Нелдера-Мида с учетом штрафа
def nelder_mead_with_penalty(x0, max_iter=1000, tol=1e-6, A=3, q=3):
    """
    Реализация метода Нелдера-Мида с учетом штрафной функции.

    :param func: Целевая функция (без штрафа).
    :param x0: Начальная точка.
    :param max_iter: Максимальное количество итераций.
    :param tol: Точность завершения.
    :param A: Коэффициентw штрафа.
    :param q: Степень штрафа.
    :return: Найденная точка, значение функции, количество итераций, история симплексов.
    """
    # Коэффициенты метода Нелдера-Мида
    alpha, gamma, rho, sigma = 0.7, 2, 0.75, 0.75

    # Инициализация симплекса
    n = len(x0)
    simplex = [x0]
    shift = 0.5
    for i in range(n):
        vertex = np.copy(x0)
        vertex[i] += shift
        simplex.append(vertex)
    simplex = np.array(simplex)

    simplex_history = [np.array(simplex)]
    iteration = 0
    k = 10
    # Основной цикл оптимизации
    while iteration < max_iter:
        iteration += 1

        # Сортировка вершин симплекса по значению объединенной функции
        simplex = sorted(simplex, key=lambda x: penalty_function(x, k * A, q))
        f_values = [penalty_function(x, k * A, q) for x in simplex]

        # Проверка на сходимость
        if np.abs(f_values[-1] - f_values[0]) < tol:
            break

        # Центр масс, исключая наихудшую точку
        centroid = np.mean(simplex[:-1], axis=0)

        # Отражение
        x_reflected = centroid + alpha * (centroid - simplex[-1])
        f_reflected = penalty_function(x_reflected, k * A, q)

        if f_values[0] <= f_reflected < f_values[-2]:
            simplex[-1] = x_reflected
        elif f_reflected < f_values[0]:
            # Расширение
            x_expanded = centroid + gamma * (x_reflected - centroid)
            f_expanded = penalty_function(x_expanded, k * A, q)
            simplex[-1] = x_expanded if f_expanded < f_reflected else x_reflected
        else:
            # Сжатие
            x_contracted = centroid + rho * (simplex[-1] - centroid)
            f_contracted = penalty_function(x_contracted, k * A, q)
            if f_contracted < f_values[-1]:
                simplex[-1] = x_contracted
            else:
                # Редукция
                best_point = simplex[0]
                simplex = np.array([best_point + sigma * (x - best_point) for x in simplex])

        simplex_history.append(np.array(simplex))
        k += 10

    return simplex[0], f_values[0], iteration, simplex_history


# Начальная точка
x0 = np.array([1.0, 1.0])

# Запуск метода Нелдера-Мида
minimum, f_min, iterations, simplex_history = nelder_mead_with_penalty(x0)

print("Минимум функции с учетом штрафа:", minimum)
print("Значение функции в минимуме (с учетом штрафа):", f_min)
print("Количество итераций:", iterations)

# Построение графика
x_range = np.linspace(-5, 5, 200)  # Расширим диапазон для лучшего обзора
y_range = np.linspace(-5, 5, 200)
X, Y = np.meshgrid(x_range, y_range)

# ВАЖНО: Используем вашу целевую функцию f(x)
Z = np.zeros_like(X)
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        Z[i,j] = f([X[i,j], Y[i,j]])

plt.figure(figsize=(10, 8))
plt.contour(X, Y, Z, levels=50, cmap="viridis")
plt.colorbar(label="f(x)")

# Отображение симплексов
for simplex in simplex_history:
    plt.plot(simplex[:, 0], simplex[:, 1], 'k-', alpha=0.4)
    plt.plot(simplex[:, 0], simplex[:, 1], 'ko', markersize=3)

# Ограничение: 2x₁ + 2x₂ + 3 > 0
x_line = np.linspace(-5, 5, 200)
y_line = (-2 * x_line - 3) / 2  # Из уравнения 2x₁ + 2x₂ + 3 = 0
plt.plot(x_line, y_line, 'r--', linewidth=2, label='Ограничение: 2x₁ + 2x₂ + 3 > 0')

# Закрасим допустимую область (где 2x₁ + 2x₂ + 3 > 0)
plt.fill_between(x_line, y_line, 2, alpha=0.2, color='green', label='Допустимая область')

# Точки минимума
plt.plot(x0[0], x0[1], 'bo', markersize=8, label='Начальная точка (x0)')
plt.plot(minimum[0], minimum[1], 'ro', markersize=8, label='Минимум с учетом штрафа')

plt.xlabel("$x_1$")
plt.ylabel("$x_2$")
plt.title("Минимизация функции методом Нелдера-Мида с учетом штрафа")
plt.legend()
plt.grid(True, alpha=0.3)
plt.xlim(-5, 5)
plt.ylim(-5, 5)
plt.show()