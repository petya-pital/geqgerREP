import numpy as np
import event_file_reader as er
import points as pn

import seismic_sensors


# Алгоритм поиска по сетке с адаптивным шагом
def adaptive_grid_search( sensors:seismic_sensors.SeismicSensorArray, initial_step=50000,min_step=1,initial_hypocenter=[0,0,0]):
    current_hypocenter = np.array(initial_hypocenter)
    current_step = initial_step
    grid_size = 50000  # Начальная длина ребра сетки в км

    while grid_size >= min_step:  # Продолжаем, пока размер сетки не станет меньше 1 км
        offsets = np.linspace(-current_step, current_step, 3)
        grid = np.array(np.meshgrid(offsets, offsets, offsets)).T.reshape(-1, 3) + current_hypocenter
        residuals = [pn.residual_sum_squares(point, sensors) for point in grid]

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
def gird_serch_from_file_path(file_path,m_step=1,prnt=True,ah=True, initial_guess=None,istep=50000):
    ev=er.load_event_from_path(file_path)
    ssa=seismic_sensors.SeismicSensorArray.from_header(ev.header)
    indmin = np.argmin(ssa.observed_times)
    minot=ssa.observed_times[indmin]
    ssa.observed_times-=minot

    if initial_guess==None:
        # initial_guess = [ssa.observed_times[indmin], ssa.locations[indmin][0], ssa.locations[indmin][1],
        #              ssa.locations[indmin][2]]
        initial_guess = [ssa.observed_times[indmin], ssa.locations[indmin][0], ssa.locations[indmin][1],
                         ssa.locations[indmin][2]]
    print(m_step)
    result=adaptive_grid_search(ssa, min_step=m_step, initial_hypocenter=[ssa.locations[indmin][0],ssa.locations[indmin][1],
                                                                          ssa.locations[indmin][2]],initial_step=istep)
    if prnt:
        print('min_step=',m_step)
        print("Оцененный гипоцентр через адаптивный поиск по сетке:", result)
        if ah:
            actual_hypocenter=[ev.catInfo.x,ev.catInfo.y,ev.catInfo.z]
            print("Фактический гипоцентр:", actual_hypocenter)
    return(result)


# ev=er.load_event_from_path('test.event')
# ssa=seismic_sensors.SeismicSensorArray.from_header(ev.header)
# # final_hypocenter = adaptive_grid_search(ssa)
# # actual_hypocenter=[ev.catInfo.x,ev.catInfo.y,ev.catInfo.z]
# # print("Фактический гипоцентр:", actual_hypocenter)
# # print("Оцененный гипоцентр через адаптивный поиск по сетке:", final_hypocenter)
# # print('min_size=1')
# final_hypocenter = adaptive_grid_search(ssa,min_step=0.01)
#
# # print("Фактический гипоцентр:", actual_hypocenter)
# print("Оцененный гипоцентр через адаптивный поиск по сетке:", final_hypocenter)