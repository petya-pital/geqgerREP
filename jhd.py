import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def theoretical_time(pointA, pointB, velocity):
    distance = np.linalg.norm(pointA - pointB)
    return distance / velocity

def calculate_partial_derivatives(x, y, z, x0, y0, z0, v):
    """
    Рассчитывает время прохождения волны и его частные производные
    """
    dx = x0 - x
    dy = y0 - y
    dz = z0 - z
    dist = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
    dtdx = dx / (v * dist)
    dtdy = dy / (v * dist)
    dtdz = dz / (v * dist)
    return np.round(dtdx, 6), np.round(dtdy, 6), np.round(dtdz, 6)




# class JHD_data():
#     def __init__(self,Sensors):
#         self.sensors=Sensors
#         self.numS=len(Sensors)
#         self.events=[]
#         self.numE=len(self.events)
#     def add_event(self,event:sc.EventDate):
#         self.events.append(event)
#         self.numE+=self.numE
#     # def get_observed_times(self):
#     #     # observed_times=[]
#     #     # for s in self.sensors

# Функция для создания матрицы весов (п
def create_weight_matrix(times):
    times = np.asarray(times).flatten()  # Преобразование в одномерный массив
    weights = np.where(times == -1, 0, 1)
    return np.diag(weights)
# Функция для красивого вывода уравнений типа 3
def print_equations_type_3(equations):
    for idx, (W_j, A_j, r_j) in enumerate(equations):
        print(f"Уравнение типа 3 для события {idx + 1}:")
        print("W_j:")
        print(W_j)
        print("A_j:")
        print(A_j)
        print("r_j:")
        print(r_j)
        print("\n")
# Функция для создания уравнений типа 3
def create_equations_type_3(observed_times, initial_estimates, num_events, num_stations, stations):
    equations = []

    for j in range(num_events):
        # print(f"observed_times[{j}] = {observed_times[j]}")  # Добавьте эту строку для отладки
        W_j = create_weight_matrix(observed_times[j])
        A_j = np.zeros((num_stations, 4))
        r_j = np.zeros(num_stations)
        t0, x0, y0, z0 = initial_estimates[j]
        # print(x0, y0, z0)
        for i in range(num_stations):
            x, y, z = stations[i].x, stations[i].y, stations[i].z
            # print(x,y,z)
            partials = calculate_partial_derivatives(x, y, z, x0, y0, z0, v=3000)
            # print(partials)
            A_j[i, :] = [1, partials[0], partials[1], partials[2]]
            r_j[i] = observed_times[j][i] - (initial_estimates[j][0] + stations[i].correction)
            # r_j[i] = observed_times[j, i] - (initial_estimates[j, 0] + stations[i].correction)
            r_j[i] = np.round(r_j[i], 6)
        # print(A_j)
        equations.append((W_j, A_j, r_j))
    return equations


# Функция для создания и решения уравнения типа 4 методом наименьших квадратов
def solve_joint_hypocenter(equations, num_events, num_stations):
    W_block = []
    A_block = []
    r_block = []

    # Создание блоков
    for j in range(num_events):
        W_j, A_j, r_j = equations[j]
        W_block.append(np.hstack([np.zeros_like(W_j) if k != j else W_j for k in range(num_events)]))
        A_block.append(np.hstack([np.zeros_like(A_j) if k != j else A_j for k in range(num_events)]))
        r_block.append(W_j @ r_j)

    # Сборка матриц и векторов
    W_block = np.vstack(W_block)
    A_block = np.vstack(A_block)
    r_block = np.hstack(r_block)

    # Сборка полной матрицы системы
    G = np.hstack([A_block, W_block])

    # Решение системы уравнений методом наименьших квадратов
    solution = np.linalg.lstsq(G, r_block, rcond=None)[0]

    # Извлечение решения
    delta_X = solution[:4 * num_events].reshape(num_events, 4)
    delta_S = solution[4 * num_events:]

    return delta_X, delta_S
def get_focal_parameters(delta_X, num_events):
    focal_parameters = []
    for j in range(num_events):
        event_params = delta_X[j, :4]
        focal_parameters.append(event_params)
    return focal_parameters

# Функция для печати фокальных параметров гипоцентров
def print_focal_parameters(focal_parameters):
    for idx, params in enumerate(focal_parameters):
        print(f"Событие {idx + 1} --- Вычисленные координаты (время, x, y, z): {params}")

# Функция для получения координат гипоцентров без времени
def get_coordinates_without_time(focal_parameters):
    coordinates = []
    for params in focal_parameters:
        coordinates.append(params[1:])  # Пропускаем первый элемент (время)
    return coordinates

# Функция для сравнения реальных и вычисленных координат
def compare_real_and_computed(real_coords, computed_coords):
    for idx, (real, computed) in enumerate(zip(real_coords, computed_coords)):
        print(f"Событие {idx + 1} --- Реальные координаты: {real}, Вычисленные координаты: {computed}")

# Функция для отрисовки пар реальных и вычисленных координат
def plot_comparison(real_coords, computed_coords):
    real_coords = np.array(real_coords)
    computed_coords = np.array(computed_coords)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Реальные координаты
    ax.scatter(real_coords[:, 0], real_coords[:, 1], real_coords[:, 2], c='b', marker='o', label='Реальные координаты')
    # Вычисленные координаты
    ax.scatter(computed_coords[:, 0], computed_coords[:, 1], computed_coords[:, 2], c='r', marker='^', label='Вычисленные координаты')

    for i in range(len(real_coords)):
        ax.plot([real_coords[i, 0], computed_coords[i, 0]],
                [real_coords[i, 1], computed_coords[i, 1]],
                [real_coords[i, 2], computed_coords[i, 2]], 'k--')

    ax.set_xlabel('X координата')
    ax.set_ylabel('Y координата')
    ax.set_zlabel('Z координата')
    ax.legend()
    plt.show()
def plot_comparison_all(real_coords, computed_coords):
    real_coords = np.array(real_coords)
    computed_coords = np.array(computed_coords)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Реальные координаты
    ax.scatter(real_coords[:, 0], real_coords[:, 1], real_coords[:, 2], c='b', marker='o', label='Реальные координаты')
    # Вычисленные координаты
    ax.scatter(computed_coords[:, 0], computed_coords[:, 1], computed_coords[:, 2], c='r', marker='^', label='Вычисленные координаты')

    # Соединение пар реальных и вычисленных координат
    for i in range(len(real_coords)):
        ax.plot([real_coords[i, 0], computed_coords[i, 0]],
                [real_coords[i, 1], computed_coords[i, 1]],
                [real_coords[i, 2], computed_coords[i, 2]], 'k--')

    ax.set_xlabel('X координата')
    ax.set_ylabel('Y координата')
    ax.set_zlabel('Z координата')
    ax.legend()
    plt.show()
# num_events = 3
# num_stations = 2
# observed_times = np.array([
#     [10.0, 12.0],
#     [14.0, 16.0],
#     [18.0, 20.0]
# ])
# initial_estimates = np.array([
#     [0, 0,0, 0],
#     [0, 0, 0, 0],
#     [0, 0, 0, 0]
# ])
# st1 = Station(33, 433, 335, correction=0)
# st2 = Station(6377, 533, 47, correction=0)
# stations = [st1, st2]
# equations = create_equations_type_3(observed_times, initial_estimates, num_events, num_stations, stations)
# delta_X, delta_S = solve_joint_hypocenter(equations, num_events, num_stations)
#
# print("Delta X:\n", delta_X)
# print("Delta S:\n", delta_S)
#
#
# print(calculate_partial_derivatives(1.0 ,33.0 ,3.0, 3 ,4, 5, 3000))
# num_events = 3
# delta_X = np.array([
#     [0.1, 1.1, 2.1, 3.1],
#     [0.2, 4.1, 5.1, 6.1],
#     [0.3, 7.1, 8.1, 9.1]
# ])
# real_coords = np.array([
#     [1, 2, 3],
#     [4, 5, 6],
#     [7, 8, 9]
# ])
#
# # Получение фокальных параметров
# focal_parameters = get_focal_parameters(delta_X, num_events)
# print_focal_parameters(focal_parameters)
#
# # Получение координат без времени
# coordinates_without_time = get_coordinates_without_time(focal_parameters)
# print("Координаты без времени:")
# print(coordinates_without_time)
#
# # Сравнение реальных и вычисленных координат
# compare_real_and_computed(real_coords, coordinates_without_time)
#
# # Отрисовка пар реальных и вычисленных координат
# plot_comparison(real_coords, coordinates_without_time)
# # Отрисовка пар реальных и вычисленных координат
# plot_comparison_all(real_coords, coordinates_without_time)