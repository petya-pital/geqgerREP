import numpy as np
import pandas as pd
import event_file_reader as er
import square_compute as sc
import gird_searh as gs
import solve_hypocentr as sh
import  writer
import seismic_sensors as ss
import  visual
import test_calcs as tc
import grid_straightforward_search as gss

# filepath='Antonovskaya_joint_test.xlsx'
# filepath2='Antonovskaya_gauges.txt'
# filepath3='newAntonovskaya_joint_test.xlsx'
# tc.gss_massive_calculation_from_file_path(filepath,filepath2,4,200)
# # tc.geiger_massive_calculation_from_file_path(filepath,filepath2,99,0.000001)
# visual.plot_coordinates_from_excel(filepath3)
def show_intro():
    print("Добро пожаловать в нашу программу!")
    print("Эта программа поможет вам выполнить следующие функции:")
    print("чтение данных  о событии/событиях")
    print("расчет  коррдинат гипоцентра разными методами ")
    print("анализ и/или визуализация результатов")
    print("Чтобы начать, просто следуйте подсказкам на экране.")
    print( 'print "exit" for exit, "help" for help ')
def show_help():
    print('now this is no help')
def evenfilechoise(filepath1):
    ev = er.load_event_from_path(filepath1)
    real_cord=[ev.catInfo.x,ev.catInfo.y,ev.catInfo.z]
    ssa=ss.SeismicSensorArray.from_header(ev.header)
    indmin = np.argmin(ssa.observed_times)
    minot = ssa.observed_times[indmin]
    ssa.observed_times -= minot
    calc_cord=[ssa.locations[indmin][0], ssa.locations[indmin][1], ssa.locations[indmin][2]]
    print("Выберите метод 1-гейгер, 21-сеткаSF,22-сеткаAdaptive 3-JHD")
    c=int(input())
    if c==3:
        print("в разработке, возвращаем к началу")
        evenfilechoise()
    elif c==21:
        print('метод сетка.')
        print("число узлов?")
        num_cells=int(input())
        print('значение масштабирующего коэффициента?')
        scale_factor=int(input())
        gss.find_hypo_from_event(ev,num_cells,scale_factor)
    elif c==22:
        print('метод адаптивная сетка.')
        print("длина минмального ребра, км?")
        min_step= float(input())
        print('Начальная длина ребра сетки в км?')
        ini_step= int(input())
        gs.gird_serch_from_event(ev,m_step=min_step,istep=ini_step)
    elif c==1:
        print('метод гейгер.')
        print("максимальное число итераций?")
        m_iter=int(input())
        print('целевой сдвиг ?')
        pogr=float(input())
        r=sc.geiger_from_file_path(filepath1, m_iter, pogr)
        calc_cord=(r[1],r[2],r[3])
    else:
        print('invalid command,try again')
        evenfilechoise()
    print('1 - графикб 2 -- вернуться к выбору метода решения, 3 -- вернутся к выбору метода ввода')
    ch=int(input())
    if ch==1:
        visual.plot_hypocenter(ssa.locations,real_cord,calc_cord)
    elif ch==2:
        evenfilechoise(filepath1)
    elif ch==3:
        main()
def main():
    show_intro()
    print("выберите способ ввода:")
    print("1. из файла типа event \n2. Из exel файлов\nprint \"-1\" for exit, \"0\" for help")
    while True:

            choice=int(input())
            if choice == 0:
                show_help()
            elif  choice == -1:
                print("Завершение работы программы.")
                break
            elif choice == 1:
                print("Вы выбрали ввод данных из файла типа event.")
                print("введите имя файла")
                filepath1 = input()
                evenfilechoise(filepath1)
            elif choice == 1:
                print("Вы выбрали ввод данных из двух файлов типа exel and txt")
                print("введите имя txt файла с координатами датчиков")
                filepath1=input()
                print("введите имя exel файла с пакетом данных о событиях")
                filepath2 = input()

        # функция ввода данных

if __name__ == "__main__":

    # ev=er.load_event_from_path('test.event')
    # f=gss.find_hypo_from_event(ev)
    # print("Estimated hypocenter:", f[0], "with error:", f[1])
    # sc.geiger_from_file_path('test.event',10000,0.01)
    # gs.gird_serch_from_file_path('test.event')
    # main()
    r=sc.geiger_from_file_path('test.event', 10000, 0.01)
    print(r)
    t=(r[1],r[2],r[3])
    ev=er.load_event_from_path('test.event')
    rc=(ev.catInfo.x,ev.catInfo.y,ev.catInfo.z)
    ssa=ss.SeismicSensorArray.from_header(ev.header)
    visual.plot_hypocenter(ssa.locations,rc,t)