import numpy as np
import solve_hypocentr as sc
from jhd_experements import compute_travel_time, extract_coordinates, compute_rmse, generate_initial_hypocenters


def joint_hypocenter_determination_single_run(num_events, num_sensors, initial_hypocenters, stations, velocity,
                                              observed_times,
                                              max_iterations, tol, real_cords, step):
    hypocenters = np.array(initial_hypocenters, dtype=float)
    results_filename = f"00__{max_iterations}_step_{step}.txt"

    with open(results_filename, "w") as results_file:
        print(f"Creating results file: {results_filename}")

        for iteration in range(max_iterations):
            total_adjustment = 0
            for event_idx in range(num_events):
                event_hypo = hypocenters[event_idx]
                A = []
                b = []
                for sensor_idx in range(num_sensors):
                    station = stations[sensor_idx]
                    if observed_times[event_idx][sensor_idx] >= 0:  # valid observed time
                        travel_time = compute_travel_time(event_hypo, station, velocity)
                        if travel_time != np.inf:
                            A.append([(event_hypo[0] - station.x) / (velocity * travel_time),
                                      (event_hypo[1] - station.y) / (velocity * travel_time),
                                      (event_hypo[2] - station.z) / (velocity * travel_time),
                                      -1])
                            b.append(observed_times[event_idx][sensor_idx] - travel_time - station.correction)
                A = np.array(A)
                b = np.array(b)
                if A.size == 0 or b.size == 0:
                    continue
                try:
                    I = np.eye(A.shape[1])
                    adjustments, _, _, _ = np.linalg.lstsq(A.T @ A + 0.1 * I, A.T @ b, rcond=None)
                    hypocenters[event_idx] += adjustments
                    total_adjustment += np.sum(np.abs(adjustments))
                except np.linalg.LinAlgError:
                    print(f"LinAlgError at iteration {iteration} for event {event_idx}")
                    continue

            if (iteration + 1) % step == 0:
                h_coords = extract_coordinates(hypocenters)
                current_rmse = compute_rmse(h_coords, real_cords)
                results_file.write(f"Число итераций = {iteration + 1}, текущая ошибка = {current_rmse}\n")
                print(f"Число итераций = {iteration + 1}, текущая ошибка = {current_rmse}")

            if total_adjustment < tol:
                print(f"Converged at iteration {iteration}")
                break

        results_file.write(f"Converged at iteration {iteration}, финальная ошибка = {current_rmse}\n")
        print(f"Results written to {results_filename}")


def normalize_observed_times(observed_times):
    normalized_times = []
    for event_times in observed_times:
        min_time = min([t for t in event_times if t >= 0])  # найти минимальное ненулевое время
        normalized_event_times = [(t - min_time) if t >= 0 else t for t in event_times]
        normalized_times.append(normalized_event_times)
    return normalized_times


# Проверяем существование файлов перед использованием
excel_file = 'Antonovskaya_joint_test.xlsx'
stations_file = 'Antonovskaya_gauges.txt'


# Подготовка данных
edl = sc.create_list_event_date_from_exel(excel_file)
real_cords = sc.create_real_cords_from_event_date_list(edl)
observed_times, num_events = sc.create_observed_times_list_and_num_events(edl)
norm_times = normalize_observed_times(observed_times)

stations, num_sensors = sc.create_stations_and_num_stations(stations_file)
velocity = 3000
tol = 0.001

# Параметры для эксперимента
max_iterations = 500000
step = 5000

initial_hypocenters = generate_initial_hypocenters(num_events, stations)

joint_hypocenter_determination_single_run(num_events, num_sensors, initial_hypocenters, stations, velocity,
                                          norm_times, max_iterations, tol, real_cords, step)
