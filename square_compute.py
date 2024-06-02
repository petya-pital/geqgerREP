import  numpy as np

def geiger_method(observed_times, initial_guess, stations, max_iterations=1000, tolerance=1e-5, alpha=0.01):
    t0, x0, y0, z0, v = initial_guess
    n = len(observed_times)

    for iteration in range(max_iterations):
        travel_times = np.round(compute_travel_times(x0, y0, z0, v, stations), 3)
        residuals = np.round(observed_times - (t0 + travel_times), 3)

        # Вычисление частных производных
        partial_derivatives = np.round(travel_times_derivatives(x0, y0, z0, v, stations), 3)

        # Решение системы линейных уравнений с регуляризацией (исключая обновление скорости)
        A = np.round(np.dot(partial_derivatives.T, partial_derivatives) + alpha * np.eye(4), 3)
        b = np.round(np.dot(partial_derivatives.T, residuals), 3)
        delta_theta = np.round(np.linalg.solve(A, b), 3)

        # Обновление параметров (без обновления скорости)
        t0 = np.round(t0 + delta_theta[0], 3)
        x0 = np.round(x0 + delta_theta[1], 3)
        y0 = np.round(y0 + delta_theta[2], 3)
        z0 = np.round(z0 + delta_theta[3], 3)

        # Вывод текущих приближений и критерия согласия
        misfit = np.linalg.norm(residuals)
        #print(f"Iteration {iteration + 1}: Misfit = {misfit:.3f}, t0 = {t0}, x0 = {x0}, y0 = {y0}, z0 = {z0}, v = {v}")

        # Проверка критерия остановки
        if np.linalg.norm(delta_theta) < tolerance:
            break

    return t0, x0, y0, z0, v


def travel_times_derivatives(x, y, z, v, stations):
    # Вычисление частных производных времени прохождения
    derivatives = []
    for (xi, yi, zi) in stations:
        dTdx = (x - xi) / (v * np.sqrt((x - xi) ** 2 + (y - yi) ** 2 + (z - zi) ** 2))
        dTdy = (y - yi) / (v * np.sqrt((x - xi) ** 2 + (y - yi) ** 2 + (z - zi) ** 2))
        dTdz = (z - zi) / (v * np.sqrt((x - xi) ** 2 + (y - yi) ** 2 + (z - zi) ** 2))
        derivatives.append([1, dTdx, dTdy, dTdz])
    return np.array(derivatives)


def compute_travel_times(x, y, z, v, stations):
    # Вычисление времени прохождения от гипоцентра до станции
    travel_times = []
    for (xi, yi, zi) in stations:
        travel_time = np.sqrt((x - xi) ** 2 + (y - yi) ** 2 + (z - zi) ** 2) / v
        travel_times.append(travel_time)
    return np.array(travel_times)