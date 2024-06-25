import numpy as np
import pandas as pd
import event_file_reader as er
import square_compute as sc
import gird_searh as gs
import solve_hypocentr as sh
import test_calcs
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
def exelinputchoice(file_path1='Antonovskaya_joint_test.xlsx',file_path2='Antonovskaya_gauges.txt'):
    bp=test_calcs.get_base_problem(file_path1,file_path2)
    # print(bp)
    print("подробные вычесления( 1-да,0-нет,по умолчанию 1")
    podr=True
    i=int(input())
    if i==1:
        podr=True
    elif i==0:
        podr=False
    print(podr)
    print("введите номер события(в разработке) или -1 для пакетной обработки")
    choi=int(input())

    if choi==-1:
        print('вывод в файл(1) или в консоль(2)?')
        ch = int(input())
        if ch==1:
            print('введите названия файла для вывода или команду def для файла по умолчанию')
            name=input()
            print("Выберите метод 1-гейгер, 21-сеткаSF,22-сеткаAdaptive 3-JHD")
            c = int(input())
            if c == 3:
                print("в разработке, возвращаем к началу")
                exelinputchoice(file_path1, file_path2)
            elif c == 21:
                # print("в разработке, возвращаем к началу")
                # exelinputchoice(file_path1, file_path2)
                print('метод сетка.')
                print("число узлов?")
                num_cells = int(input())
                print('значение масштабирующего коэффициента?')
                scale_factor = int(input())
                r =tc.gss_massive_calculation_from_file_path(file_path1, file_path2,num_cells,scale_factor)
                # calc_cord = (r[1], r[2], r[3])
            elif c == 22:
                print("в разработке, возвращаем к началу")
                exelinputchoice(file_path1, file_path2)
                # print('метод адаптивная сетка.')
                # print("длина минмального ребра, км?")
                # min_step = float(input())
                # print('Начальная длина ребра сетки в км?')
                # ini_step = int(input())
                # r = gs.gird_serch_from_event(ev, m_step=min_step, istep=ini_step)
                # calc_cord = (r[0], r[1], r[2])
            elif c == 1:
                print('метод гейгер.')
                print("максимальное число итераций?")
                m_iter = int(input())
                print('целевой сдвиг ?')
                pogr = float(input())
                tc.geiger_massive_calculation_from_file_path(file_path1, file_path2, m_iter, pogr, fail_path3=name)
                # calc_cord = (r[1], r[2], r[3])
            else:
                print('invalid command,try again')
                exelinputchoice(file_path1, file_path2)
            print('1 - графикб 2 -- вернуться к выбору метода решения, 3 -- вернутся к выбору метода ввода')
            ch = int(input())
            if ch == 1:
                visual.plot_coordinates_from_excel(name='new' + file_path1)
                print('1-- вернуться к выбору метода решения, 2 -- вернутся к выбору метода ввода')
                chh = int(input())
                if chh == 1:
                    exelinputchoice(file_path1, file_path2)
                elif chh == 2:
                    main()
            elif ch == 2:
                exelinputchoice(file_path1, file_path2)
            elif ch == 3:
                main()
        elif ch==2:
            print("Выберите метод 1-гейгер, 21-сеткаSF,22-сеткаAdaptive 3-JHD")
            c = int(input())
            if c == 3:
                print("в разработке, возвращаем к началу")
                exelinputchoice(file_path1, file_path2)
            elif c == 21:
                # print("в разработке, возвращаем к началу")
                # exelinputchoice(file_path1, file_path2)
                print('метод сетка.')
                print("число узлов?")
                num_cells = int(input())
                print('значение масштабирующего коэффициента?')
                scale_factor = int(input())
                r = tc.gss_massive_calculation_from_base_to_console(bp,num_cells,scale_factor)
                # calc_cord = (r[1], r[2], r[3])
            elif c == 22:
                print("в разработке, возвращаем к началу")
                exelinputchoice(file_path1, file_path2)
                # print('метод адаптивная сетка.')
                # print("длина минмального ребра, км?")
                # min_step = float(input())
                # print('Начальная длина ребра сетки в км?')
                # ini_step = int(input())
                # r = gs.gird_serch_from_event(ev, m_step=min_step, istep=ini_step)
                # calc_cord = (r[0], r[1], r[2])
            elif c == 1:
                print('метод гейгер.')
                print("максимальное число итераций?")
                m_iter = int(input())
                print('целевой сдвиг ?')
                pogr = float(input())
                tc.geiger_massive_calculation_to_console(bp,m_iter, pogr,podr=podr)
                # calc_cord = (r[1], r[2], r[3])
            else:
                print('invalid command,try again')
                exelinputchoice(file_path1, file_path2)
            print('1 - график(в разработке), 2 -- вернуться к выбору метода решения, 3 -- вернутся к выбору метода ввода')
            ch = int(input())
            if ch == 1:
                # visual.plot_coordinates_from_excel(name='new' + file_path1)
                print('1-- вернуться к выбору метода решения, 2 -- вернутся к выбору метода ввода')
                chh = int(input())
                if chh == 1:
                    exelinputchoice(file_path1, file_path2)
                elif chh == 2:
                    main()
            elif ch == 2:
                exelinputchoice(file_path1, file_path2)
            elif ch == 3:
                main()






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
        r=gss.find_hypo_from_event(ev,num_cells,scale_factor)
        calc_cord = (r[1], r[2], r[3])
    elif c==22:
        print('метод адаптивная сетка.')
        print("длина минмального ребра, км?")
        min_step= float(input())
        print('Начальная длина ребра сетки в км?')
        ini_step= int(input())
        r=gs.gird_serch_from_event(ev,m_step=min_step,istep=ini_step)
        calc_cord=(r[0],r[1],r[2])
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
        print('1-- вернуться к выбору метода решения, 2 -- вернутся к выбору метода ввода')
        chh = int(input())
        if chh == 1:
            evenfilechoise(filepath1)
        elif chh == 2:
            main()
    elif ch==2:
        evenfilechoise(filepath1)
    elif ch==3:
        main()
def main():
    show_intro()
    print("выберите способ ввода:")
    print("1. из файла типа event \n2. Из exel файла\nprint \"-1\" for exit, \"0\" for help")
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
            elif choice == 2:
                print("Вы выбрали ввод данных из двух файлов типа exel and txt")
                print('Использовать файлы по умолчанию?1/0')
                defolt=int(input())
                if defolt==0:
                    print("введите имя txt файла с координатами датчиков")
                    filepath1 = input()
                    print("введите имя exel файла с пакетом данных о событиях")
                    filepath2 = input()
                    exelinputchoice(filepath2, filepath1)
                elif defolt==1:
                    exelinputchoice()


        # функция ввода данных

if __name__ == "__main__":

    # ev=er.load_event_from_path('test.event')
    # f=gss.find_hypo_from_event(ev)
    # print("Estimated hypocenter:", f[0], "with error:", f[1])
    # sc.geiger_from_file_path('test.event',10000,0.01)
    # gs.gird_serch_from_file_path('test.event')
    main()

