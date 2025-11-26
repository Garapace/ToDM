M = 1e4  # Большое число для искусственного добавления ограничений в таблицу

simplex_table = [                           # Начальная таблица симплекс-метода
    [-20*M, -3*M-3, -4*M+2, 0, 0, M, 0],    # Строки с коэффициентами целевой функции и переменными
    [11,         2,      1, 1, 0, 0, 0],    # Ограничения задачи
    [10,        -3,      2, 0, 1, 0, 0],
    [20,         3,      4, 0, 0, -1, 1]
]

solution = [0, 0, 0, 0, 0, 0] # Начальное решение
indexes = []                  # Список индексов ведущих строк и столбцов


# Функция для поиска ведущего столбца
def find_leading_column(matrix):
    temp_matrix = matrix[0].copy()
    temp_matrix.pop(0)
    lead_column = temp_matrix.index(min(temp_matrix))
    return lead_column + 1


# Функция для поиска ведущей строки
def find_leading_row(matrix):
    lead_column = find_leading_column(matrix)
    quotients = []
    for i in range(1, len(matrix)):
        if matrix[i][lead_column] > 0:
            quotients.append(matrix[i][0] / matrix[i][lead_column])
        else:
            quotients.append(1e8)
    lead_row = quotients.index(min(quotients))
    return lead_row + 1


# Функция для обновления симплекс-таблицы
def write_new_table(matrix):
    lead_row = find_leading_row(matrix)
    lead_column = find_leading_column(matrix)
    new_matrix = []
    matrix_row = []
    lead_element = matrix[lead_row][lead_column]
    for i in range(len(matrix)):
        if i != lead_row:
            for j in range(len(matrix[0])):
                if j != lead_column:
                    matrix_row.append(
                        matrix[i][j] - (matrix[i][lead_column] * matrix[lead_row][j]) / lead_element
                    )
                else:
                    matrix_row.append(0)
        else:
            for j in range(len(matrix[0])):
                matrix_row.append(matrix[i][j] / lead_element)
        new_matrix.append(matrix_row.copy())
        matrix_row.clear()
    return new_matrix


# Функция для проверки, завершено ли решение симплекс-метода
def simplex_done(matrix):
    for i in range(len(matrix[0])):
        if matrix[0][i] < 0:
            return False
    return True


# Основной цикл симплекс-метода
while not(simplex_done(simplex_table)):
    indexes.append((find_leading_row(simplex_table), find_leading_column(simplex_table)))
    simplex_table = write_new_table(simplex_table)

# Находим решение
for cortez in indexes:
    solution[cortez[1] - 1] = simplex_table[cortez[0]][0]

print(f"x1 = {round(solution[0], 6)}")
print(f"x2 = {round(solution[1], 6)}")
print(f"F = {round(simplex_table[0][0], 6)}")
