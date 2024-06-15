import pandas as pd
import numpy as  np

import square_compute

class Problem:
    def __init__(self, locations, velocities, observed_times, real_hypocenter_location):
        self.locations = locations
        self.velocities = velocities
        self.observed_times = observed_times
        self.real_hypocenter_location = real_hypocenter_location

    def __repr__(self):
        return (f"Problem(locations={self.locations}, velocities={self.velocities}, "
                f"observed_times={self.observed_times}, real_hypocenter_location={self.real_hypocenter_location})")

def create_problem(event_date, locations):
    observed_times = event_date.arrival_times
    speed = event_date.speed  # Используем скорость из объекта EventDate

    # Фильтрация данных, исключение -1 из observed_times и соответствующих координат из locations
    valid_indices = [i for i, time in enumerate(observed_times) if time != -1]
    filtered_locations = [locations[i] for i in valid_indices]
    filtered_observed_times = [observed_times[i] for i in valid_indices]
    filtered_velocities = [speed for _ in valid_indices]  # Все скорости равны значению speed

    # Создание объекта Problem
    problem = Problem(
        locations=filtered_locations,
        velocities=filtered_velocities,
        observed_times=filtered_observed_times,
        real_hypocenter_location=event_date.real_coordinates  # предполагаем, что это гипоцентр
    )

    return problem

# Определение класса EventDate
class EventDate:
    def __init__(self, date, real_coordinates, speed, number_of_sensors, arrival_times):
        self.date = date
        self.real_coordinates = real_coordinates
        self.speed = speed
        self.number_of_sensors = number_of_sensors
        self.arrival_times = arrival_times

    def __repr__(self):
        return (f"EventDate(date={self.date}, real_coordinates={self.real_coordinates}, "
                f"speed={self.speed}, number_of_sensors={self.number_of_sensors}, "
                f"arrival_times={self.arrival_times})")

# Загрузка данных из Excel файла, пропуская первые 4 строки с метаданными
events_data = pd.read_excel('Antonovskaya_joint_test.xlsx', skiprows=4, engine='openpyxl')

# Создание списка объектов EventDate
list_of_events = [
    EventDate(
        date=row['Дата и время UTC+7'],
        real_coordinates=[row['X'], row['Y'], row['Z']],
        speed=row['V'],
        number_of_sensors=row['N датчиков'],
        arrival_times=row[['intro_1', 'intro_2', 'intro_3', 'intro_4', 'intro_5', 'intro_6', 'intro_7']].tolist()
    )
    for index, row in events_data.iterrows()
]

# Вывод первых нескольких объектов для проверки
print(list_of_events[:3])
# Считываем данные из файла
data = np.loadtxt('Antonovskaya_gauges.txt', dtype=str, encoding='utf-8-sig')

# Массив с типами датчиков
sensor_types = data[:, 0]
data[:, 1:4] = np.char.replace(data[:, 1:4], ',', '.')
# Массив с координатами
coordinates = data[:, 1:4].astype(float)

print("Типы датчиков:")
print(sensor_types)
print("Координаты:")
print(coordinates)
problem_instance = create_problem(list_of_events[0], coordinates)
print(problem_instance)
square_compute.gieger_from_problem(problem_instance,990,0.000001,True)
