import numpy as np

import  solve_hypocentr as sc
# class Station:
#     def __init__(self, x, y, z, name=None, correction=0):
#         self.x = x
#         self.y = y
#         self.z = z
#         self.name = name
#         self.correction = correction
#
#     def __repr__(self):
#         return (f"Station(x={self.x}, y={self.y}, z={self.z} ,name={self.name},correction={self.correction})")


def compute_travel_time(hypo, station, velocity):
    distance = np.sqrt((hypo[0] - station.x) ** 2 + (hypo[1] - station.y) ** 2 + (hypo[2] - station.z) ** 2)
    return distance / velocity if distance != 0 else np.inf


def joint_hypocenter_determination(num_events, num_sensors, initial_hypocenters, stations, velocity, observed_times,
                                   max_iterations, tol):
    hypocenters = np.array(initial_hypocenters, dtype=float)
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
                adjustments, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
                hypocenters[event_idx] += adjustments
                total_adjustment += np.sum(np.abs(adjustments))
            except np.linalg.LinAlgError:
                print(f"LinAlgError at iteration {iteration} for event {event_idx}")
                continue

        if total_adjustment < tol:
            print(f"Converged at iteration {iteration}")
            break

    return hypocenters
def generate_synthetic_data(hypocenters, stations, velocity):
    num_events = len(hypocenters)
    num_sensors = len(stations)
    observed_times = []
    for event in hypocenters:
        event_times = []
        for station in stations:
            travel_time = compute_travel_time(event, station, velocity)
            event_times.append(travel_time)
        observed_times.append(event_times)
    return np.array(observed_times)
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
def compute_errors(computed_hypocenters, real_hypocenters):
    computed_coords = extract_coordinates(computed_hypocenters)
    errors = []
    for i, (computed, real) in enumerate(zip(computed_coords, real_hypocenters)):
        differences = computed - np.array(real)
        squared_diff = np.square(differences)
        mse = np.mean(squared_diff)
        rmse = np.sqrt(mse)
        errors.append((i, rmse))
    return errors
def generate_initial_hypocenters(num_events, stations):
    avg_x = np.mean([station.x for station in stations])
    avg_y = np.mean([station.y for station in stations])
    avg_z = np.mean([station.z for station in stations])
    initial_hypocenters = [[avg_x, avg_y, avg_z, 0] for _ in range(num_events)]
    return initial_hypocenters
# Example usage
# num_events = 2
# num_sensors = 7
# initial_hypocenters = [[0, 0, 0, 0], [0, 0, 0, 0]]
# stations = [Station(0, 0, 0), Station(1, 0, 0), Station(0, 1, 0), Station(0, 0, 1), Station(1, 1, 0), Station(1, 0, 1),
#             Station(0, 1, 1)]
edl=sc.create_list_event_date_from_exel('Antonovskaya_joint_test.xlsx')
real_cords=sc.create_real_cords_from_event_date_list(edl)
observed_times, num_events=sc.create_observed_times_list_and_num_events(edl)
norm_times=normalize_observed_times(observed_times)
# print(OTl)
# print(num_events)
# =sc.create_initial_estimates(num_events)

# print(ie)
stations, num_sensors=sc.create_stations_and_num_stations('Antonovskaya_gauges.txt')
velocity = 3000
initial_hypocenters=generate_initial_hypocenters(num_events,stations)
# observed_times = [[0.0, 0.22999999999999998, -1.0, 0.5025, -1.0, 0.12749999999999995, 0.4890000000000003],
#                   [0.0, 0.2665000000000002, -1.0, 0.45150000000000023, -1.0, 0.17200000000000015, 0.5180000000000002]]
max_iterations =4000
tol = 0.001

hypocenters = joint_hypocenter_determination(num_events, num_sensors, initial_hypocenters, stations, velocity,
                                             norm_times, max_iterations, tol)
print(real_cords)
print("Final Hypocenters:")
print(hypocenters)
print(real_cords)
h_coords = extract_coordinates(hypocenters)

rmse=compute_rmse(real_cords,h_coords)
print("RMSE between computed and real hypocenters:")
print(rmse)
errors = compute_errors(h_coords,real_cords)
print("Errors between each pair of computed and real hypocenters:")
for idx, error in errors:
    print(f"Event {idx}: RMSE = {error}")

# Example usage
# num_events = 2
# num_sensors = 7
# stations = [sc.Station(0, 0, 0), sc.Station(1, 0, 0), sc.Station(0, 1, 0), sc.Station(0, 0, 1), sc.Station(1, 1, 0), sc.Station(1, 0, 1), sc.Station(0, 1, 1)]
# velocity = 5.0
# real_hypocenters = [[1, 1, 1, 0.1], [2, 2, 2, 0.2]]

# # Generate synthetic observed times
# observed_times = generate_synthetic_data(real_hypocenters, stations, velocity)
# print("Observed Times (Synthetic Data):")
# print(observed_times)
#
# # Initial guesses for hypocenters
# initial_hypocenters = [[0, 0, 0, 0], [0, 0, 0, 0]]
# max_iterations = 100
# tol = 1e-5
#
# # Compute hypocenters using JHD
# computed_hypocenters = joint_hypocenter_determination(num_events, num_sensors, initial_hypocenters, stations, velocity, observed_times, max_iterations, tol)
# print("Final Computed Hypocenters:")
# print(computed_hypocenters)
#
# # Compute errors
# real_coords = extract_coordinates(real_hypocenters)
# errors = compute_errors(computed_hypocenters, real_coords)
# print("Errors between each pair of computed and real hypocenters:")
# for idx, error in errors:
#     print(f"Event {idx}: RMSE = {error}")