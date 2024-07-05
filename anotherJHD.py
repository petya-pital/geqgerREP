import numpy as np
import solve_hypocentr as sc

def generate_synthetic_data(num_earthquakes, num_stations, true_hypocenters, stations, velocity_model):
    times = np.zeros((num_earthquakes, num_stations))
    for i in range(num_earthquakes):
        for j in range(num_stations):
            distance = np.linalg.norm(true_hypocenters[i, :3] - stations[j])
            travel_time = distance / velocity_model
            times[i, j] = travel_time + true_hypocenters[i, 3]
    return times


def jhd(num_earthquakes, num_stations, initial_hypocenters, observed_times, stations, velocity_model, iterations=10):
    hypocenters = np.array(initial_hypocenters, dtype=float)  # Преобразование к массиву NumPy
    observed_times = np.array(observed_times, dtype=float)    # Преобразование к массиву NumPy
    for iteration in range(iterations):
        A = []
        b = []
        for i in range(num_earthquakes):
            for j in range(num_stations):
                distance = np.linalg.norm(hypocenters[i, :3] - stations[j])
                if distance == 0:
                    continue
                theoretical_time = distance / velocity_model + hypocenters[i, 3]
                residual = observed_times[i, j] - theoretical_time
                partial_derivatives = (hypocenters[i, :3] - stations[j]) / (distance * velocity_model)
                A.append(np.hstack((partial_derivatives, 1)))
                b.append(residual)

        A = np.array(A)
        b = np.array(b)

        # Вывод количества строк в A и b
        print(f"Iteration {iteration}: Number of rows in A: {A.shape[0]}, Number of rows in b: {b.shape[0]}")

        # Решение системы уравнений
        delta_hypocenters, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

        # Вывод информации о размере delta_hypocenters
        print(f"Iteration {iteration}: delta_hypocenters size: {delta_hypocenters.size}, expected: {4 * num_earthquakes}")

        if delta_hypocenters.size == 4 * num_earthquakes:
            for i in range(num_earthquakes):
                hypocenters[i, :3] += delta_hypocenters[4 * i:4 * i + 3]
                hypocenters[i, 3] += delta_hypocenters[4 * i + 3]
        else:
            print("Mismatch in the size of delta_hypocenters.")
            break

    return hypocenters

# Загрузка данных
stations = np.array(sc.create_location('Antonovskaya_gauges.txt'))
print(stations)
num_stations = len(stations)
velocity_model = 3000

events_date_list = sc.create_list_event_date_from_exel('Antonovskaya_joint_test.xlsx')
observed_times, num_events = sc.create_observed_times_list_and_num_events(events_date_list)
true_hypocenters = np.array(sc.create_real_cords_from_event_date_list(events_date_list))
print(observed_times)
initial_hypocenters = np.array(sc.create_initial_estimates(num_events))
print(initial_hypocenters)
# Выполнение JHD
estimated_hypocenters = jhd(num_events, num_stations, initial_hypocenters, observed_times, stations, velocity_model)

# Вывод результатов
print("True hypocenters:")
print(true_hypocenters)
print("Estimated hypocenters:")
print(estimated_hypocenters)
