import numpy as np
from scipy.optimize import minimize
import event_file_reader as er
#import square_compute as sc
import gird_searh
import seismic_sensors
import points
import pandas as pd
import numpy as  np

#import square_compute

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
    date=event_date
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
        # self.number_of_sensors = number_of_sensors
        self.arrival_times = arrival_times

    def __repr__(self):
        return (f"EventDate(date={self.date}, real_coordinates={self.real_coordinates}, "
                f"speed={self.speed} "
                f"arrival_times={self.arrival_times})")

def  create_list_event_date_from_exel(filepath):
    events_data = pd.read_excel(filepath, skiprows=4, engine='openpyxl')
    list_of_events = [
        EventDate(
            date=row['Дата и время UTC+7'],
            real_coordinates=[row['X'], row['Y'], row['Z']],
            speed=row['V'],
            # number_of_sensors=row['N датчиков'],
            arrival_times=row[['intro_1', 'intro_2', 'intro_3', 'intro_4', 'intro_5', 'intro_6', 'intro_7']].tolist()
        )
        for index, row in events_data.iterrows()
    ]
    print(list_of_events)
    return list_of_events

def create_location(filepath):
    data = np.loadtxt(filepath, dtype=str, encoding='utf-8-sig')

    # Массив с типами датчиков
    sensor_types = data[:, 0]
    data[:, 1:4] = np.char.replace(data[:, 1:4], ',', '.')
    # Массив с координатами
    coordinates = data[:, 1:4].astype(float)

# Загрузка данных из Excel файла, пропуская первые 4 строки с метаданными
def create_list_of_problem_from_file(filepath1,filepath2):
    edl=create_list_event_date_from_exel(filepath1)
    l=create_location(filepath2)
    list_of_problem = []
    for ed in edl:
        list_of_problem.append(create_problem(ed,l))


    result=list_of_problem
    print(result)
    return result
# Создание списка объектов EventDate

def calculate_travel_time(x, y, z, x0, y0, z0, v):
    """Рассчитывает время прохождения волны от гипоцентра до станции."""
    return np.sqrt((x - x0)**2 + (y - y0)**2 + (z - z0)**2) / v

def objective_function(params, x, y, z, t, v):
    """Функция потерь, которую мы минимизируем: сумма квадратов временных остатков."""
    if t.all !=np.inf:
        t0, x0, y0, z0 = params
        residuals = t - (t0 + calculate_travel_time(x, y, z, x0, y0, z0, v))
        return np.sum(residuals**2)
    else:
        return 0

def find_hypocenter(x, y, z, t, v, initial_guess):
    """Находит гипоцентр, минимизируя функцию потерь."""
    result = minimize(objective_function, initial_guess, args=(x, y, z, t, v),
                      method='BFGS', options={'disp': True})
    return result.x
# ev=er.load_event_from_path("test.event")
# ssa=seismic_sensors.SeismicSensorArray.from_header(ev.header)
# # Пример данных: координаты станций, времена прихода и скорости распространения
#
# stations=np.array(ssa.locations)
# v=ssa.velocities
# t=ssa.observed_times
# # Начальное предположение о времени и местоположении гипоцентра
# initial_guess = [0, 0,0,0]  # t0, x0, y0, z0
#
# # Вызов функции для поиска гипоцентра
# hypocenter = find_hypocenter(stations[:, 0], stations[:, 1], stations[:, 2], t, v, initial_guess)
# print(f"Оценка гипоцентра: время {hypocenter[0]}, координаты ({hypocenter[1]}, {hypocenter[2]}, {hypocenter[3]})")
# filepath='Antonovskaya_joint_test.xlsx'
# filepath2='Antonovskaya_gauges.txt'
# filepath3='newAntonovskaya_joint_test.xlsx'
# # create_problem_from_file(filepath,filepath2)
# l=create_location(filepath2)
# led=create_list_event_date_from_exel(filepath)
# create_problem(led[0],l)
#create_list_of_problem_from_file(filepath,filepath2)
#sc.massive_calculation_from_file_path(filepath,filepath2,1000,0.1)