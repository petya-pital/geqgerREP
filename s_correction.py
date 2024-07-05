import os
import numpy as np
import solve_hypocentr as sc
import jhd4
def compute_travel_time(hypo, station, velocity):
    """
    Compute the travel time of seismic waves from the hypocenter to the station.

    Parameters:
    hypo : list or numpy array
        Hypocenter coordinates [x, y, z].
    station : object
        Station object with attributes x, y, z, correction.
    velocity : float
        Seismic wave velocity.

    Returns:
    float
        Travel time of seismic waves from the hypocenter to the station.
    """
    distance = np.sqrt((hypo[0] - station.x) ** 2 + (hypo[1] - station.y) ** 2 + (hypo[2] - station.z) ** 2)
    return distance / velocity if distance != 0 else np.inf

def extract_coordinates(hypocenters):
    """
    Extract the spatial coordinates from the hypocenter data.

    Parameters:
    hypocenters : numpy array
        Array of hypocenters with shape (num_events, 4), where the last column is time.

    Returns:
    numpy array
        Array of spatial coordinates with shape (num_events, 3).
    """
    return np.array(hypocenters)[:, :3]

def compute_rmse(computed_hypocenters, real_hypocenters):
    """
    Compute the Root Mean Square Error (RMSE) between computed and real hypocenters.

    Parameters:
    computed_hypocenters : numpy array
        Array of computed hypocenters.
    real_hypocenters : numpy array
        Array of real hypocenters.

    Returns:
    float
        RMSE value.
    """
    computed_coords = extract_coordinates(computed_hypocenters)
    differences = computed_coords - np.array(real_hypocenters)
    squared_diff = np.square(differences)
    mse = np.mean(squared_diff)
    rmse = np.sqrt(mse)
    return rmse

def joint_hypocenter_determination(num_events,real_cords, num_sensors, initial_hypocenters, stations, velocity, observed_times,
                                   max_iterations, tol, patience=10, regularization=0.1):
    """
    Perform the Joint Hypocenter Determination (JHD) algorithm.

    Parameters:
    num_events : int
        Number of seismic events.
    num_sensors : int
        Number of sensors (stations).
    initial_hypocenters : list or numpy array
        Initial guesses for hypocenters.
    stations : list of Station objects
        List of station objects.
    velocity : float
        Seismic wave velocity.
    observed_times : list of lists
        Observed times of seismic waves at each station for each event.
    max_iterations : int
        Maximum number of iterations.
    tol : float
        Tolerance for convergence.
    patience : int, optional
        Number of iterations to allow without improvement before stopping.
    regularization : float, optional
        Regularization parameter.

    Returns:
    numpy array
        Final computed hypocenters.
    """
    hypocenters = np.array(initial_hypocenters, dtype=float)
    best_hypocenters = np.copy(hypocenters)
    best_rmse = np.inf
    no_improvement_iters = 0

    station_corrections = np.zeros(num_sensors)

    for iteration in range(max_iterations):
        total_adjustment = 0
        delta_s = np.zeros(num_sensors)
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
                        b.append(observed_times[event_idx][sensor_idx] - travel_time - station.correction - station_corrections[sensor_idx])
            A = np.array(A)
            b = np.array(b)
            if A.size == 0 or b.size == 0:
                continue
            try:
                I = np.eye(A.shape[1])
                adjustments, _, _, _ = np.linalg.lstsq(A.T @ A + regularization * I, A.T @ b, rcond=None)
                hypocenters[event_idx] += adjustments[:-1]
                total_adjustment += np.sum(np.abs(adjustments[:-1]))
                delta_s += adjustments[-1]
            except np.linalg.LinAlgError:
                print(f"LinAlgError at iteration {iteration} for event {event_idx}")
                continue

        station_corrections += delta_s

        h_coords = extract_coordinates(hypocenters)
        current_rmse = compute_rmse(h_coords, real_cords)
        if current_rmse < best_rmse:
            best_rmse = current_rmse
            best_hypocenters = np.copy(hypocenters)
            no_improvement_iters = 0
        else:
            no_improvement_iters += 1

        if no_improvement_iters >= patience or total_adjustment < tol:
            print(f"Converged at iteration {iteration}")
            break

    # Apply the final station corrections to the station objects
    for idx, station in enumerate(stations):
        station.correction += station_corrections[idx]

    return best_hypocenters
excel_file = 'Antonovskaya_joint_test.xlsx'
stations_file = 'Antonovskaya_gauges.txt'
edl = sc.create_list_event_date_from_exel(excel_file)
real_cords = sc.create_real_cords_from_event_date_list(edl)
observed_times, num_events = sc.create_observed_times_list_and_num_events(edl)
norm_times = jhd4.normalize_observed_times(observed_times)

stations, num_sensors = sc.create_stations_and_num_stations(stations_file)
velocity = 3000
tol = 0.001

initial_hypocenters = jhd4.generate_initial_hypocenters(num_events, stations)
max_iterations = 50
step = 500

# Запуск алгоритма
final_hypocenters = joint_hypocenter_determination(num_events, real_cords,num_sensors, initial_hypocenters, stations, velocity, norm_times, max_iterations, tol)

# Вывод результатов
print("Final Hypocenters:")
print(final_hypocenters)
h_coords = extract_coordinates(final_hypocenters)
rmse = compute_rmse(h_coords, real_cords)
print("RMSE between computed and real hypocenters:")
print(rmse)