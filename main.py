import numpy as np
import pandas as pd
import event_file_reader as er
import square_compute as sc
import gird_searh as gs
import solve_hypocentr as sh
import  writer
import seismic_sensors as ss
import  visual
#file_path='Осинниковская 22_10_2021 05_51_12.event'
# sc.geiger_from_file_path('test.event',90000,0.001,True,initial_guess=[0,0, 25248.0, 6.0])
# gs.gird_serch_from_file_path('test.event',0.0001,True,True,[22608.0, 25248.0, 6.0 ] )
# sc.geiger_from_file_path(file_path,45000,0.00001,True,initial_guess=[0,47859.0, 30610.0, -17.0])
#file_path='Антоновская 29_05_2024 22_44_43.event'
#gs.gird_serch_from_file_path(file_path,0.0001,True,True,istep=500000)
#sc.geiger_from_file_path(file_path,990000,0.000001,True)
# Загрузка данных из Excel файла, пропуская первые 4 строки с метаданными
# events_data = pd.read_excel('Antonovskaya_joint_test.xlsx', skiprows=4, engine='openpyxl')
#
# # Создание списка объектов EventDate
# list_of_events = [
#     sh.EventDate(
#         date=row['Дата и время UTC+7'],
#         real_coordinates=[row['X'], row['Y'], row['Z']],
#         speed=row['V'],
#         number_of_sensors=row['N датчиков'],
#         arrival_times=row[['intro_1', 'intro_2', 'intro_3', 'intro_4', 'intro_5', 'intro_6', 'intro_7']].tolist()
#     )
#     for index, row in events_data.iterrows()
# ]
#
# # Вывод первых нескольких объектов для проверки
# print(list_of_events[:3])
# # Считываем данные из файла
# data = np.loadtxt('Antonovskaya_gauges.txt', dtype=str, encoding='utf-8-sig')
#
# # Массив с типами датчиков
# sensor_types = data[:, 0]
# data[:, 1:4] = np.char.replace(data[:, 1:4], ',', '.')
# # Массив с координатами
# coordinates = data[:, 1:4].astype(float)
#
# print("Типы датчиков:")
# print(sensor_types)
# print("Координаты:")
# print(coordinates)
# problem_instance = sh.create_problem(list_of_events[0], coordinates)
# print(problem_instance)
# sc.gieger_from_problem(problem_instance,990,0.000001,True)
# workbook = writer.create_excel_file('имя', 'м', 100, 0.01, 6)
#
# # Пример добавления новых данных после создания файла
# ws = workbook.active
# ws.append(['Новые данные', '123', '456', '789', '', '10', '20', '30', '40', '', '0.5'])
#
# # После окончания работы с файлом его нужно сохранить и можно закрыть
# workbook.save('имя.xlsx')
# workbook.close()
filepath='Antonovskaya_joint_test.xlsx'
filepath2='Antonovskaya_gauges.txt'
filepath3='newAntonovskaya_joint_test.xlsx'
#sc.massive_calculation_from_file_path(filepath,filepath2,99,0.000001)
visual.plot_coordinates_from_excel(filepath3)
