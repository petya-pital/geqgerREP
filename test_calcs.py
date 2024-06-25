import  event_file_reader as er
import seismic_sensors as ss
import numpy as np
from scipy.linalg import lstsq
import solve_hypocentr as sh
import pandas as pd
import writer
import points as pt
import grid_straightforward_search as gss
import square_compute as sc
def get_base_event(file_path,file_path2):
    events_data = pd.read_excel(file_path, skiprows=4, engine='openpyxl')
    list_of_events = [
        sh.EventDate(
            date=row['Дата и время UTC+7'],
            real_coordinates=[row['X'], row['Y'], row['Z']],
            speed=row['V'],
            number_of_sensors=row['N датчиков'],
            arrival_times=row[['intro_1', 'intro_2', 'intro_3', 'intro_4', 'intro_5', 'intro_6', 'intro_7']].tolist()
        )
        for index, row in events_data.iterrows()
    ]
    data = np.loadtxt(file_path2, dtype=str, encoding='utf-8-sig')

    # Массив с типами датчиков
    sensor_types = data[:, 0]
    data[:, 1:4] = np.char.replace(data[:, 1:4], ',', '.')
    # Массив с координатами
    coordinates = data[:, 1:4].astype(float)
    return list_of_events,coordinates
def get_base_problem(file_path,file_path2):
    base=get_base_event(file_path,file_path2)
    base_problem=[]
    list_event=base[0]
    locations=base[1]
    for ed in list_event:
        base_problem.append(sh.create_problem(ed,locations))
    return base_problem
def geiger_massive_calculation_to_console(base_problem,max_iterarions,tolerance,podr=False,alpha=0.0001,fail_path3='def'):
    for pr in base_problem:
        coord=pr.real_hypocenter_location
        r = sc.gieger_from_problem(pr, max_iterarions, tolerance, alpha=0.0001,prt=podr)
        ws=[]
        ws.append(['real coord', coord[0], coord[1], coord[2], 'calc coord', r[0], r[1], r[2], r[3]])
        print(ws)

def geiger_massive_calculation_from_file_path(file_path,file_path2,max_iterarions,tolerance,alpha=0.0001,fail_path3='def',prt=True):
    events_data = pd.read_excel(file_path, skiprows=4, engine='openpyxl')
    list_of_events = [
        sh.EventDate(
            date=row['Дата и время UTC+7'],
            real_coordinates=[row['X'], row['Y'], row['Z']],
            speed=row['V'],
            number_of_sensors=row['N датчиков'],
            arrival_times=row[['intro_1', 'intro_2', 'intro_3', 'intro_4', 'intro_5', 'intro_6', 'intro_7']].tolist()
        )
        for index, row in events_data.iterrows()
    ]
    data = np.loadtxt(file_path2, dtype=str, encoding='utf-8-sig')

    # Массив с типами датчиков
    sensor_types = data[:, 0]
    data[:, 1:4] = np.char.replace(data[:, 1:4], ',', '.')
    # Массив с координатами
    coordinates = data[:, 1:4].astype(float)
    params = [
        f"метод={'geiger'}",
        f"максимальное число итераций={max_iterarions}",
        f"альфа={alpha}",
        f"точность={tolerance}"
    ]
    workbook = writer.create_excel_file(file_path, params)
    ws = workbook.active
    #ws.append(['Новые данные', '123', '456', '789', '', '10', '20', '30', '40', '', '0.5'])

    # После окончания работы с файлом его нужно сохранить и можно закрыть
#    , '', coord[0], coord[1], coord[2], '', r[0], r[1], r[2], r[3]
    for e in list_of_events:
        coord=np.array(e.real_coordinates)
        pr=sh.create_problem(e,coordinates)
        print(pr)
        r=sc.gieger_from_problem(pr,max_iterarions,tolerance,alpha=0.0001,prt=prt)
        print(r)
        ws.append([e.date, '', coord[0], coord[1], coord[2], '', r[0], r[1], r[2], r[3]])
    if fail_path3=='def':
        workbook.save('new' + file_path)
    else:
        workbook.save(fail_path3)
    workbook.close()
def gss_massive_calculation_from_base_to_console(base_problem,scale=2,num=10):
    for pr in base_problem:
        coord=pr.real_hypocenter_location
        r = sc.gieger_from_problem(pr, scale,num, alpha=0.0001)
        ws=[]
        ws.append(['real coord', coord[0], coord[1], coord[2], 'calc coord', r[0], r[1], r[2], r[3]])
        print(ws)
def gss_massive_calculation_from_file_path(file_path,file_path2,scale=2,num=10):
    events_data = pd.read_excel(file_path, skiprows=4, engine='openpyxl')
    list_of_events = [
        sh.EventDate(
            date=row['Дата и время UTC+7'],
            real_coordinates=[row['X'], row['Y'], row['Z']],
            speed=row['V'],
            number_of_sensors=row['N датчиков'],
            arrival_times=row[['intro_1', 'intro_2', 'intro_3', 'intro_4', 'intro_5', 'intro_6', 'intro_7']].tolist()
        )
        for index, row in events_data.iterrows()
    ]
    data = np.loadtxt(file_path2, dtype=str, encoding='utf-8-sig')

    # Массив с типами датчиков
    sensor_types = data[:, 0]
    data[:, 1:4] = np.char.replace(data[:, 1:4], ',', '.')
    # Массив с координатами
    coordinates = data[:, 1:4].astype(float)
    params = [
        f"метод={'gird_straigthtforward'}",
        f"число клеток={num}",
        f"параметр масштабирования={scale}"
    ]
    workbook = writer.create_excel_file(file_path, params)
    ws = workbook.active
    #ws.append(['Новые данные', '123', '456', '789', '', '10', '20', '30', '40', '', '0.5'])

    # После окончания работы с файлом его нужно сохранить и можно закрыть
#    , '', coord[0], coord[1], coord[2], '', r[0], r[1], r[2], r[3]
    for e in list_of_events:
        coord=np.array(e.real_coordinates)
        pr=sh.create_problem(e,coordinates)
        #print(pr)
        l=gss.HypocenterLocator(pr.locations,pr.observed_times,pr.velocities,scale_factor=2, num_cells=10)
        hypocenter, error = l.find_hypocenter()
        print("Estimated hypocenter:", hypocenter, "with error:", error)
        ws.append([e.date, '', coord[0], coord[1], coord[2], '', '',hypocenter[0], hypocenter[0], hypocenter[0], '', '',error])
    workbook.save('new' + file_path)
    workbook.close()
# filepath='Antonovskaya_joint_test.xlsx'
# filepath2='Antonovskaya_gauges.txt'
# # be=get_base_event(filepath,filepath2)
# bp=get_base_problem(filepath,filepath2)
# # print(bp)
