import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import pandas as pd
import matplotlib.pyplot as plt


def plot_coordinates_from_excel(filepath):
    # Чтение данных из файла Excel начиная с четвертой строки
    df = pd.read_excel(filepath, skiprows=3, engine='openpyxl')

    # Инициализация списков для реальных и вычисленных координат
    real_coords = []
    calculated_coords = []
    labels = []

    # Проход по строкам DataFrame для извлечения координат и подписей
    for _, row in df.iterrows():
        # Извлечение имени пары из первой ячейки
        label = row.iloc[0]

        # Реальные координаты (X, Y, Z) находятся в столбцах 3-5
        real_coord = (row.iloc[2], row.iloc[3], row.iloc[4])

        # Вычисленные координаты (X, Y, Z) находятся в столбцах 8-10
        calculated_coord = (row.iloc[7], row.iloc[8], row.iloc[9])

        # Добавление координат и подписей в соответствующие списки
        real_coords.append(real_coord)
        calculated_coords.append(calculated_coord)
        labels.append(label)

    # Преобразование списков в массивы для удобства работы с matplotlib
    real_coords = np.array(real_coords)
    calculated_coords = np.array(calculated_coords)

    # Построение графика
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Добавление точек реальных координат
    ax.scatter(real_coords[:, 0], real_coords[:, 1], real_coords[:, 2], c='blue', label='Real Coordinates')

    # Добавление точек вычисленных координат
    ax.scatter(calculated_coords[:, 0], calculated_coords[:, 1], calculated_coords[:, 2], c='red',
               label='Calculated Coordinates')

    # Добавление подписей и линий к каждой паре точек
    for real, calc, label in zip(real_coords, calculated_coords, labels):
        ax.text(real[0], real[1], real[2], label, color='blue')
        ax.text(calc[0], calc[1], calc[2], label, color='red')
        ax.plot([real[0], calc[0]], [real[1], calc[1]], [real[2], calc[2]], c='gray')

    # Настройка графика
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_zlabel('Z Coordinate')
    ax.legend()

    # Отображение графика
    plt.show()
# Пример вызова функции
#plot_coordinates_from_excel('имя.xlsx')


def plot_hypocenter(sensor_locations, real_hypocenter, calculated_hypocenter):
    """
    Визуализирует в 3D координаты датчиков и гипоцентра.

    :param sensor_locations: массив координат датчиков (N x 3)
    :param real_hypocenter: массив с фактическими координатами гипоцентра (1 x 3)
    :param calculated_hypocenter: массив с вычисленными координатами гипоцентра (1 x 3)
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Разбиение координат датчиков
    xs, ys, zs = zip(*sensor_locations)

    # Отображение координат датчиков
    ax.scatter(xs, ys, zs, c='blue', label='Sensor Locations', marker='o')

    # Отображение фактического гипоцентра
    ax.scatter(*real_hypocenter, c='red', label='Real Hypocenter', marker='^', s=100)

    # Отображение вычисленного гипоцентра
    ax.scatter(*calculated_hypocenter, c='green', label='Calculated Hypocenter', marker='s', s=100)

    # Настройка графика
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_zlabel('Z Coordinate')
    ax.legend()

    plt.show()


# Пример использования функции
# sensor_locs = [(10, 20, 30), (20, 30, 40), (30, 40, 50)]
# real_hypo = (15, 25, 35)
# calc_hypo = (15, 30, 35)
#
# plot_hypocenter(sensor_locs, real_hypo, calc_hypo)