class Cell:
    """Класс для хранения координат клетки (строка, столбец)"""
    def __init__(self, row, col):
        self.row = row
        self.col = col

class State:
    """Вспомогательный класс для поиска пути в графе (используется в build_path)"""
    def __init__(self, cell, prev_dir, next_cells):
        self.cell = cell
        self.prev_dir = prev_dir  # Направление, откуда пришли: 'v' (вертикаль) или 'h' (горизонталь)
        self.next_cells = next_cells # Список доступных клеток для следующего шага

def solve(a, b, costs):
    """
    Основная функция: балансировка и метод северо-западного угла.
    a - запасы, b - потребности, costs - матрица стоимостей.
    """
    assert len(costs) == len(a)
    assert len(costs[0]) == len(b)
    a_sum = sum(a)
    b_sum = sum(b)

    # 1. СВЕДЕНИЕ К ЗАКРЫТОЙ МОДЕЛИ (Балансировка)
    if a_sum > b_sum:
        # Если предложение превышает спрос, добавляем фиктивного потребителя
        b.append(a_sum - b_sum)
        for row in costs:
            row.append(0) # Стоимость перевозки к нему равна 0
    elif a_sum < b_sum:
        # Если спрос превышает предложение, добавляем фиктивного поставщика
        a.append(b_sum - a_sum)
        costs.append([0] * len(b))

    # Матрица перевозок (x) и копии для работы алгоритма
    x = [[0] * len(b) for _ in range(len(a))]
    a_copy = a[:]
    b_copy = b[:]

    # 2. МЕТОД СЕВЕРО-ЗАПАДНОГО УГЛА (Начальный опорный план)
    indexes_for_baza = [] # Список базисных (заполненных) клеток
    i, j = 0, 0
    while True:
        if a_copy[i] < b_copy[j]:
            # Поставщик i полностью исчерпан
            x[i][j] = a_copy[i]
            indexes_for_baza.append(Cell(i, j))
            b_copy[j] -= a_copy[i]
            a_copy[i] = 0
            i += 1
        else:
            # Потребитель j полностью удовлетворен
            x[i][j] = b_copy[j]
            indexes_for_baza.append(Cell(i, j))
            a_copy[i] -= b_copy[j]
            b_copy[j] = 0
            j += 1

        # Если все запасы и потребности распределены — выходим
        if sum(a_copy) == 0 and sum(b_copy) == 0:
            print("Метод северо-западного угла завершен")
            break

    # Считаем стоимость первого плана
    result = sum(x[cell.row][cell.col] * costs[cell.row][cell.col] for cell in indexes_for_baza)
    print(f"Z = {result} (метод северо-западного угла)")

    # Переходим к оптимизации
    potential_method(a, b, x, costs, indexes_for_baza)


def potential_method(a, b, x, costs, indexes_for_baza):
    """Оптимизация плана методом потенциалов"""
    m, n = len(a), len(b)

    while True:
        # Сортировка для удобства обхода
        indexes_for_baza.sort(key=lambda cell: (cell.row, cell.col))

        # 3. РАСЧЕТ ПОТЕНЦИАЛОВ (u_i + v_j = c_ij)
        u = [0] * m
        v = [0] * n
        fill_u = [False] * m
        fill_v = [False] * n
        fill_u[0] = True # Полагаем первый потенциал u0 = 0

        # Итеративно находим все u и v для базисных клеток
        while not all(fill_u) or not all(fill_v):
            for cell in indexes_for_baza:
                i, j = cell.row, cell.col
                if fill_u[i]:
                    v[j] = costs[i][j] - u[i]
                    fill_v[j] = True
                elif fill_v[j]:
                    u[i] = costs[i][j] - v[j]
                    fill_u[i] = True

        # 4. ПРОВЕРКА НА ОПТИМАЛЬНОСТЬ
        # Считаем оценки для пустых клеток: delta = u_i + v_j - c_ij
        not_optimal_cells = []
        economies = []
        for i in range(m):
            for j in range(n):
                # Если клетка НЕ в базисе
                if all(cell.row != i or cell.col != j for cell in indexes_for_baza):
                    diff = u[i] + v[j] - costs[i][j]
                    if diff > 0: # Если оценка положительна, план можно улучшить
                        not_optimal_cells.append(Cell(i, j))
                        economies.append(diff)

        # Если нет клеток с положительной оценкой — план оптимален
        if not not_optimal_cells:
            print("Метод потенциалов завершен")
            print(f"ui = {u}")
            print(f"vi = {v}")
            break

        # 5. ВВОД НОВОЙ КЛЕТКИ В БАЗИС
        # Выбираем клетку с максимальной "экономией" (оценкой)
        max_economy = max(economies)
        cells_with_max_economy = [cell for cell, economy in zip(not_optimal_cells, economies) if economy == max_economy]
        # Из них выбираем ту, где стоимость перевозки меньше
        min_cost_cell = min(cells_with_max_economy, key=lambda cell: costs[cell.row][cell.col])
        indexes_for_baza.append(min_cost_cell)

        # 6. ПОСТРОЕНИЕ ЦИКЛА ПЕРЕСЧЕТА
        path = build_path(min_cost_cell, indexes_for_baza)
            
        # Определяем "минусовые" клетки в цикле (те, что на нечетных позициях)
        minus_cells = path[1::2]
        # Находим минимальный объем перевозки среди минусовых клеток (тета)
        min_x_value = min(x[cell.row][cell.col] for cell in minus_cells)

        # Перераспределяем груз: в плюсовые добавляем тета, из минусовых вычитаем
        for idx, cell in enumerate(path):
            if idx % 2 == 0:
                x[cell.row][cell.col] += min_x_value
            else:
                x[cell.row][cell.col] -= min_x_value

        # Выводим из базиса ту клетку, где значение стало нулевым
        for cell in minus_cells:
            if x[cell.row][cell.col] == 0:
                # Удаляем объект с такими же координатами
                for b_cell in indexes_for_baza:
                    if b_cell.row == cell.row and b_cell.col == cell.col:
                        indexes_for_baza.remove(b_cell)
                        break
                break

    # Итоговый расчет целевой функции Z после оптимизации
    result = sum(x[cell.row][cell.col] * costs[cell.row][cell.col] for cell in indexes_for_baza)
    print(f"Z = {result} (метод потенциалов)")


def build_path(start_cell, baza_cells):
    """
    Поиск замкнутого пути (цикла) в таблице.
    Использует стек и поиск с возвратом (backtracking).
    """
    # Начало поиска: ищем клетки в той же строке, что и стартовая
    stack = [State(start_cell, 'v',
                   [cell for cell in baza_cells if cell.row == start_cell.row and cell.col != start_cell.col])]

    while stack:
        head = stack[-1]

        # Если путь >= 4 клеток и мы можем вернуться в начало по прямой — цикл найден
        if len(stack) >= 4 and ((head.cell.row == start_cell.row) or (head.cell.col == start_cell.col)):
            break

        # Если в текущем направлении ходов больше нет — возвращаемся назад
        if not head.next_cells:
            stack.pop()
            continue

        # Делаем следующий шаг и меняем направление (v -> h или h -> v)
        next_cell = head.next_cells.pop()
        next_dir = 'h' if head.prev_dir == 'v' else 'v'
        
        # Ищем клетки для следующего шага (перпендикулярно текущему)
        next_cells = [
            cell for cell in baza_cells
            if (cell.col == next_cell.col if next_dir == 'h' else cell.row == next_cell.row)
               and (cell.row != next_cell.row if next_dir == 'h' else cell.col != next_cell.col)
        ]

        stack.append(State(next_cell, next_dir, next_cells))

    return [state.cell for state in stack]


if __name__ == "__main__":
    # Тестовые данные
    a = [30, 50, 20]
    b = [15, 15, 40, 30]
    costs = [
        [1, 8, 2, 3],
        [4, 7, 5, 1],
        [5, 3, 4, 4]
    ]
    solve(a, b, costs)