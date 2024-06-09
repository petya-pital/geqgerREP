import event_file_reader as er
import seismic_sensors as ss
import numpy as np
from scipy.linalg import lstsq

def calculate_travel_time_and_derivatives(x, y, z, x0, y0, z0, v):
    dx = x0 - x
    dy = y0 - y
    dz = z0 - z
    dist = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
    epsilon = 1e-8  # Уменьшение значения epsilon
    dist = np.fmax(dist, epsilon)

    time = dist / v
    dtdx = dx / (v * dist)
    dtdy = dy / (v * dist)
    dtdz = dz / (v * dist)
    return time, dtdx, dtdy, dtdz

def geiger_method(x, y, z, t, v, initial_guess, max_iter, tolerance, alpha=1e-6):
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
        t0 += delta[0]
        x0 += delta[1]
        y0 += delta[2]
        z0 += delta[3]

        if np.linalg.norm(delta) < tolerance:
            break

    return np.round([t0, x0, y0, z0], 6)  # Округление только в конце

def geiger_from_file_path(file_path, max_iterations, tolerance, prt=True, ah=True):
    ev = er.load_event_from_path(file_path)
    ssa = ss.SeismicSensorArray.from_header(ev.header)
    stations = np.array(ssa.locations)
    v = ssa.velocities
    t = ssa.observed_times
    indmin = np.argmin(ssa.observed_times)
    initial_guess = [ssa.observed_times[indmin], *ssa.locations[indmin]]

    result = geiger_method(stations[:, 0], stations[:, 1], stations[:, 2], t, v, initial_guess, max_iter=max_iterations, tolerance=tolerance)
    if prt:
        print("Оцененные значения: время", result[0], ", координаты (", result[1], ", ", result[2], ", ", result[3], ")")
        if ah:
            actual_hypocenter = [ev.catInfo.x, ev.catInfo.y, ev.catInfo.z]
            print("Фактический гипоцентр:", actual_hypocenter)
    return result
geiger_from_file_path('test.event',40,0.00001,True)