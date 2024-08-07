import numpy as np
from scipy.optimize import minimize
import event_file_reader as er
#import square_compute as sc
import gird_searh
import seismic_sensors
import points
import pandas as pd
import numpy as  np
import jhd
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
        self.number_of_sensors = number_of_sensors
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
            number_of_sensors=row['N датчиков'],
            arrival_times=row[['intro_1', 'intro_2', 'intro_3', 'intro_4', 'intro_5', 'intro_6', 'intro_7']].tolist()
        )
        for index, row in events_data.iterrows()
    ]
    # print(list_of_events)
    return list_of_events

def create_location(filepath):
    data = np.loadtxt(filepath, dtype=str, encoding='utf-8-sig')

    # Массив с типами датчиков
    sensor_types = data[:, 0]
    data[:, 1:4] = np.char.replace(data[:, 1:4], ',', '.')
    # Массив с координатами
    coordinates = data[:, 1:4].astype(float)
    return coordinates

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
#Создаем массив из времен
# наблюдений

def create_observed_times_list_and_num_events(events_date_list):
    num_events=0
    OT_list=[]
    # edl = create_list_event_date_from_exel(filepath)
    for ed in events_date_list:
        OT=ed.arrival_times
        # print(OT)
        OT_list.append(OT)
    # print(OT_list)
    num_events=len(OT_list)
    return OT_list, num_events

def create_initial_estimates(num_events):
    initial_estimates=[]
    for i in range(num_events):
        initial_estimates.append([0, 0, 0, 0])
    # print(initial_estimates)
    return initial_estimates
class Station:
    def __init__(self, x, y, z, name=None, correction=0):
        self.x = x
        self.y = y
        self.z = z
        self.name = name
        self.correction = correction
    def __repr__(self):
        return (f"Station(x={self.x}, y={self.y}, z={self.z} ,name={self.name},correction={self.correction})")

def create_stations_and_num_stations(filepath):
    l = create_location(filepath)
    # print(l)
    stations=[]
    num_stations=len(l)
    for i in range(num_stations):
        station=Station(l[i,0],l[i,1],l[i,2])
        # print(station)
        stations.append(station)
    # print(stations,num_stations)
    return stations,num_stations
def create_real_cords_from_event_date_list(event_date_list):
    real_cords=[]
    for ed in event_date_list:
        real_cords.append(ed.real_coordinates)
    #print(real_cords)
    return real_cords

#
edl=create_list_event_date_from_exel('Antonovskaya_joint_test.xlsx')
real_cords=create_real_cords_from_event_date_list(edl)
OTl, num_events=create_observed_times_list_and_num_events(edl)
print(OTl)
# print(num_events)
ie=create_initial_estimates(num_events)
# print(ie)
stations, num_stations=create_stations_and_num_stations('Antonovskaya_gauges.txt')
print(stations)
# equations=jhd.create_equations_type_3(OTl,ie,num_events,num_stations,stations)
# DeltaX,DeltaS=jhd.solve_joint_hypocenter(equations,num_events,num_stations)
# print(DeltaX,DeltaS,len(DeltaS))
# # focal_param=jhd.get_focal_parameters(DeltaX,num_events)
# jhd.print_focal_parameters(focal_param)
# calc_cords=jhd.get_coordinates_without_time(focal_param)
# jhd.compare_real_and_computed(real_cords,calc_cords)
# jhd.plot_comparison_all(real_cords,calc_cords)


