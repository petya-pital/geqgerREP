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
def evenfilechoise():
    print("Выберите метод 1-гейгер, 2-сетка, 3-JHD")
    c=int(input())
    if c==3:
        print("в разработке, возвращаем к началу")
        evenfilechoise()
    elif c==2:
        print('метод сетка.')
        print("число узлов?")
        num_cells=int(input())
        print('значение масштабирующего коэффициента?')
        scale_factor=int(input())
    elif c==1:
        print('метод гейгер.')
        print("максимальное число итераций?")
        m_iter=int(input())
        print('целевой сдвиг ?')
        pogr=float(input())
    else:
        print('invalid command,try again')
        evenfilechoise()
def main():
    while True:
            show_intro()
            print("выберите способ ввода:")
            print("1. из файла типа event \n2. Из exel файлов\nprint \"-1\" for exit, \"0\" for help")
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
                evenfilechoise()
            elif choice == 1:
                print("Вы выбрали ввод данных из двух файлов типа exel and txt")
                print("введите имя txt файла с координатами датчиков")
                filepath1=input()
                print("введите имя exel файла с пакетом данных о событиях")
                filepath2 = input()

        # функция ввода данных

if __name__ == "__main__":
    ev=er.load_event_from_path('test.event')
    f=gss.find_hypo_from_event(ev)
    print("Estimated hypocenter:", f[0], "with error:", f[1])
    sc.geiger_from_file_path('test.event',10000,0.01)
    gs.gird_serch_from_file_path('test.event')
    # main()

