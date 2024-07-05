import os
import numpy as np
import solve_hypocentr as sc


def compute_travel_time(hypo, station, velocity):
    distance = np.sqrt((hypo[0] - station.x) ** 2 + (hypo[1] - station.y) ** 2 + (hypo[2] - station.z) ** 2)
    return distance / velocity if distance != 0 else np.inf


def joint_hypocenter_determination(num_events, num_sensors, initial_hypocenters, stations, velocity, observed_times,
                                   max_iterations, tol, patience=10, regularization=0.1):
    hypocenters = np.array(initial_hypocenters, dtype=float)
    best_hypocenters = np.copy(hypocenters)
    best_rmse = np.inf
    no_improvement_iters = 0

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
                adjustments, _, _, _ = np.linalg.lstsq(A.T @ A + regularization * I, A.T @ b, rcond=None)
                hypocenters[event_idx] += adjustments
                total_adjustment += np.sum(np.abs(adjustments))
            except np.linalg.LinAlgError:
                print(f"LinAlgError at iteration {iteration} for event {event_idx}")
                continue

        h_coords = extract_coordinates(hypocenters)
        current_rmse = compute_rmse(real_cords, h_coords)
        if current_rmse < best_rmse:
            best_rmse = current_rmse
            best_hypocenters = np.copy(hypocenters)
            no_improvement_iters = 0
        else:
            no_improvement_iters += 1

        if no_improvement_iters >= patience or total_adjustment < tol:
            print(f"Converged at iteration {iteration}")
            break

    return best_hypocenters


def normalize_observed_times(observed_times):
    normalized_times = []
    for event_times in observed_times:
        min_time = min([t for t in event_times if t >= 0])  # найти минимальное ненулевое время
        normalized_event_times = [(t - min_time) if t >= 0 else t for t in event_times]
        normalized_times.append(normalized_event_times)
    return normalized_times


def extract_coordinates(hypocenters):
    return np.array(hypocenters)[:, :3]


def compute_rmse(computed_hypocenters, real_hypocenters):
    computed_coords = extract_coordinates(computed_hypocenters)
    differences = computed_coords - np.array(real_hypocenters)
    squared_diff = np.square(differences)
    mse = np.mean(squared_diff)
    rmse = np.sqrt(mse)
    return rmse


def generate_initial_hypocenters(num_events, stations):
    avg_x = np.mean([station.x for station in stations])
    avg_y = np.mean([station.y for station in stations])
    avg_z = np.mean([station.z for station in stations])
    initial_hypocenters = [[avg_x, avg_y, avg_z, 0] for _ in range(num_events)]
    return initial_hypocenters


def run_experiment(a, b, c, real_cords, norm_times, stations, num_sensors, velocity, tol):
    num_events = len(real_cords)
    initial_hypocenters = generate_initial_hypocenters(num_events, stations)
    results_filename = f"{a}_{b}.txt"

    with open(results_filename, "w") as results_file:
        print(f"Creating results file: {results_filename}")
        for max_iterations in range(a, b + 1, c):
            hypocenters = joint_hypocenter_determination(num_events, num_sensors, initial_hypocenters, stations,
                                                         velocity,
                                                         norm_times, max_iterations, tol)
            h_coords = extract_coordinates(hypocenters)
            rmse = compute_rmse(real_cords, h_coords)
            results_file.write(f"Число итераций равно = {max_iterations}, RMSE = {rmse}\n")
            print(f"Число итераций равно = {max_iterations}, RMSE = {rmse}")
    print(f"Results written to {results_filename}")


# Проверяем существование файлов перед использованием
excel_file = 'Antonovskaya_joint_test.xlsx'
stations_file = 'Antonovskaya_gauges.txt'

if not os.path.isfile(excel_file):
    print(f"File not found: {excel_file}")
    exit(1)

if not os.path.isfile(stations_file):
    print(f"File not found: {stations_file}")
    exit(1)

# Подготовка данных
# edl = sc.create_list_event_date_from_exel(excel_file)
# real_cords = sc.create_real_cords_from_event_date_list(edl)
# observed_times, num_events = sc.create_observed_times_list_and_num_events(edl)
# norm_times = normalize_observed_times(observed_times)
#
# stations, num_sensors = sc.create_stations_and_num_stations(stations_file)
# velocity = 3000
# tol = 0.001
#
# # Параметры для эксперимента
# a = 1000
# b = 5000
# c = 500
#
# run_experiment(a, b, c, real_cords, norm_times, stations, num_sensors, velocity, tol)
