import  event_file_reader as er
import seismic_sensors as ss
import numpy as np
from scipy.linalg import lstsq


def calculate_travel_time_and_derivatives(x, y, z, x0, y0, z0, v):
    """
    Рассчитывает время прохождения волны и его частные производные
    от гипоцентра до станции с округлением до 6 знаков после запятой.
    """
    dx = x0 - x
    dy = y0 - y
    dz = z0 - z
    dist = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
    epsilon = 1e-6
    dist = np.fmax(dist, epsilon)  # Использование np.fmax для векторных операций

    time = np.round(dist / v, 6)
    dtdx = np.round(dx / (v * dist), 6)
    dtdy = np.round(dy / (v * dist), 6)
    dtdz = np.round(dz / (v * dist), 6)
    return time, dtdx, dtdy, dtdz



def geiger_method(x, y, z, t, v, initial_guess, max_iter, tolerance,alpha=0.0001):
    # """
    # Реализация метода Гейгера для определения гипоцентра.
    # """
    # t0, x0, y0, z0 = initial_guess
    # for iteration in range(max_iter):
    #     A = []
    #     b = []
    #     for xi, yi, zi, ti, vi in zip(x, y, z, t, v):
    #         T, dTdx, dTdy, dTdz = calculate_travel_time_and_derivatives(xi, yi, zi, x0, y0, z0, vi)
    #         A.append([1, dTdx, dTdy, dTdz])
    #         b.append(np.round(ti - (t0 + T), 6))
    #
    #
    #     A = np.array(A)
    #     b = np.array(b)
    #     delta = lstsq(A, b)[0]
    #     delta = np.round(delta, 6)
    #     print('iteration ', iteration, ' from ', max_iter - 1)
    #     print('old focal: ',initial_guess)
    #     print('sdvig= ',delta)
    #     print('norm of shift =',np.linalg.norm(delta),'critical value= ',tolerance)
    #     print('new focal: ',t0, x0, y0, z0)
    #     t0 = np.round(t0 + delta[0], 6)
    #     x0 = np.round(x0 + delta[1], 6)
    #     y0 = np.round(y0 + delta[2], 6)
    #     z0 = np.round(z0 + delta[3], 6)
    #
    #     # Проверка сходимости
    #     if np.linalg.norm(delta) < tolerance:
    #         break
    #
    # return t0, x0, y0, z0
    t0, x0, y0, z0 = initial_guess
    for iteration in range(max_iter):
        A = []
        b = []
        for xi, yi, zi, ti, vi in zip(x, y, z, t, v):
            T, dTdx, dTdy, dTdz = calculate_travel_time_and_derivatives(xi, yi, zi, x0, y0, z0, vi)
            A.append([1, dTdx, dTdy, dTdz])
            b.append(ti - (t0 + T))

        A = np.array(A)
        b = np.array(b)
        ATA = np.dot(A.T, A) + alpha * np.eye(4)  # Регуляризация
        ATb = np.dot(A.T, b)
        delta = lstsq(ATA, ATb)[0]
        if iteration<3000 or iteration%1000==0:
            print('iteration ', iteration, ' from ', max_iter - 1)
            print('old focal: ', initial_guess)
            print('sdvig= ', delta)
            print('norm of shift =', np.linalg.norm(delta), 'critical value= ', tolerance)


        t0 += delta[0]
        x0 += delta[1]
        y0 += delta[2]
        z0 += delta[3]
        if iteration < 3000 or iteration % 1000 == 0:
            print('new focal: ', t0, x0, y0, z0)
        if np.linalg.norm(delta) < tolerance:
            break

    return np.round([t0, x0, y0, z0], 6)  # Округление только в конце
def geiger_from_file_path(file_path,max_iterarions,tolerance,prt=True,ah=True, initial_guess=None):
    ev = er.load_event_from_path(file_path)
    ssa = ss.SeismicSensorArray.from_header(ev.header)
    stations = np.array(ssa.locations)
    v = ssa.velocities
    t = ssa.observed_times
    indmin=np.argmin(ssa.observed_times)
    if initial_guess == None:
        initial_guess = [0, ssa.locations[indmin][0], ssa.locations[indmin][1],
                         ssa.locations[indmin][2]]
    result= geiger_method(stations[:, 0], stations[:, 1], stations[:, 2], t, v, initial_guess,max_iter=max_iterarions,tolerance=tolerance)
    if prt:
        print("Оцененные значения: время", result[0], ", координаты (", result[1], ", ", result[2], ", ", result[3], ")")
        if ah:
            actual_hypocenter=[ev.catInfo.x,ev.catInfo.y,ev.catInfo.z]
            print("Фактический гипоцентр:", actual_hypocenter)
    return result

# Вызов функции
# result = geiger_method(stations[:, 0], stations[:, 1], stations[:, 2], t, v, initial_guess)
# print("Оцененные значения: время", result[0], ", координаты (", result[1], ", ", result[2], ", ", result[3], ")")
#
# # def geiger_method(observed_times, initial_guess, stations, max_iterations=1000, tolerance=1e-5, alpha=0.01):
#     t0, x0, y0, z0, v = initial_guess
#     n = len(observed_times)
#     for iteration in range(max_iterations):
#         travel_times = np.round(compute_travel_times(x0, y0, z0, v, stations), 3)
#         residuals = np.round(observed_times - (t0 + travel_times), 3)
#
#         # Вычисление частных производных
#         partial_derivatives = np.round(travel_times_derivatives(x0, y0, z0, v, stations), 3)
#
#         # Решение системы линейных уравнений с регуляризацией (исключая обновление скорости)
#         A = np.round(np.dot(partial_derivatives.T, partial_derivatives) + alpha * np.eye(4), 3)
#         b = np.round(np.dot(partial_derivatives.T, residuals), 3)
#         delta_theta = np.round(np.linalg.solve(A, b), 3)
#
#         # Обновление параметров (без обновления скорости)
#         t0 = np.round(t0 + delta_theta[0], 3)
#         x0 = np.round(x0 + delta_theta[1], 3)
#         y0 = np.round(y0 + delta_theta[2], 3)
#         z0 = np.round(z0 + delta_theta[3], 3)
#
#         # Вывод текущих приближений и критерия согласия
#         misfit = np.linalg.norm(residuals)
#         #print(f"Iteration {iteration + 1}: Misfit = {misfit:.3f}, t0 = {t0}, x0 = {x0}, y0 = {y0}, z0 = {z0}, v = {v}")
#
#         # Проверка критерия остановки
#         if np.linalg.norm(delta_theta) < tolerance:
#             break
#
#     return t0, x0, y0, z0, v
#
#
# def travel_times_derivatives(x, y, z, v, stations):
#     # Вычисление частных производных времени прохождения
#     derivatives = []
#     for (xi, yi, zi) in stations:
#         dTdx = (x - xi) / (v * np.sqrt((x - xi) ** 2 + (y - yi) ** 2 + (z - zi) ** 2))
#         dTdy = (y - yi) / (v * np.sqrt((x - xi) ** 2 + (y - yi) ** 2 + (z - zi) ** 2))
#         dTdz = (z - zi) / (v * np.sqrt((x - xi) ** 2 + (y - yi) ** 2 + (z - zi) ** 2))
#         derivatives.append([1, dTdx, dTdy, dTdz])
#     return np.array(derivatives)
#
#
# def compute_travel_times(x, y, z, v, stations):
#     # Вычисление времени прохождения от гипоцентра до станции
#     travel_times = []
#     for (xi, yi, zi) in stations:
#         travel_time = np.sqrt((x - xi) ** 2 + (y - yi) ** 2 + (z - zi) ** 2) / v
#         travel_times.append(travel_time)
#     return np.array(travel_times)