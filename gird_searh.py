import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import event_file_reader as er


# Функция для расчета теоретического времени прибытия P-волны в 3D
def theoretical_arrival_time(station, hypocenter, velocity=6.0):
    distance = np.linalg.norm(station - hypocenter)
    return distance / velocity


# Функция для расчета суммы квадратов остатков
def residual_sum_squares(hypocenter, observed_times, stations):
    residuals = 0
    for i, station in enumerate(stations):
        if observed_times[i] != np.inf:  # Учитываем только станции, где P-волна прибыла
            theoretical_time = theoretical_arrival_time(station, hypocenter)
            residuals += (theoretical_time - observed_times[i]) ** 2
    return residuals


# Алгоритм поиска по сетке с адаптивным шагом
def adaptive_grid_search(initial_hypocenter, initial_step, stations, observed_times):
    current_hypocenter = np.array(initial_hypocenter)
    current_step = initial_step
    grid_size = 50000  # Начальная длина ребра сетки в км

    while grid_size >= 1:  # Продолжаем, пока размер сетки не станет меньше 1 км
        offsets = np.linspace(-current_step, current_step, 3)
        grid = np.array(np.meshgrid(offsets, offsets, offsets)).T.reshape(-1, 3) + current_hypocenter
        residuals = [residual_sum_squares(point, observed_times, stations) for point in grid]

        min_residual_index = np.argmin(residuals)
        min_residual = residuals[min_residual_index]
        best_hypocenter = grid[min_residual_index]

        print(f"Current best at {best_hypocenter} with residual {min_residual} and grid size {grid_size}")

        if min_residual_index == 13:  # Проверяем, минимум в центре ли?
            current_step /= 3
        else:
            current_hypocenter = best_hypocenter

        grid_size = current_step * 2

    return best_hypocenter


# Параметры симуляции
stations = np.array([[10, 10, 0], [20, 10, 5], [30, 20, 10], [40, 5, 15]])
actual_hypocenter = [15, 15, 5]
observed_times = [theoretical_arrival_time(st, actual_hypocenter) for st in stations[:2]] + [np.inf, np.inf]

# Параметры для алгоритма
initial_hypocenter = [0, 0, 0]
initial_step = 50000 / 3  # Шаг сетки, так что начальная длина ребра - 50000 км

# Запуск поиска по сетке
final_hypocenter = adaptive_grid_search(initial_hypocenter, initial_step, stations, observed_times)

print("Фактический гипоцентр:", actual_hypocenter)
print("Оцененный гипоцентр через адаптивный поиск по сетке:", final_hypocenter)
def load_file_as_byte_array(file_path):
    with open(file_path, "rb") as file:
        byte_array = file.read()
    return byte_array
f = load_file_as_byte_array("test.event")
ev = er.try_read(f)
stations=[]
dt=ev.header.datchiki
observed_times=[]
initional=[0,0,0,0]
ngates=0
ev.header.printMe()

for d in dt:
     print(d.Introduction)
     if d.Introduction:#range(5):
        stations.append((d.x,d.y,d.z))
        observed_times.append(d.introInX)
        initional[0]+=d.x
        initional[1]+= d.y
        initional[2] += d.z
        initional[3] += d.introInX
        ngates+=1
initial_hypocenter=stations[0]
initial_step = 50000 / 3  # Шаг сетки, так что начальная длина ребра - 50000 км

# Запуск поиска по сетке
final_hypocenter = adaptive_grid_search(initial_hypocenter, initial_step, stations, observed_times)

print("Фактический гипоцентр:", actual_hypocenter)
print("Оцененный гипоцентр через адаптивный поиск по сетке:", final_hypocenter)