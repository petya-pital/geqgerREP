import numpy as np


class Station:
    def __init__(self, x, y, z, name=None, correction=0):
        self.x = x
        self.y = y
        self.z = z
        self.name = name
        self.correction = correction

    def __repr__(self):
        return (f"Station(x={self.x}, y={self.y}, z={self.z} ,name={self.name},correction={self.correction})")


def compute_residuals(arrival_time, predicted_time):
    return arrival_time - predicted_time


def compute_weighted_residuals(weights, residuals):
    return weights * residuals


def compute_partial_derivatives(hypocenter, station, wave_speed):
    distance = np.sqrt((hypocenter[0] - station.x) ** 2 +
                       (hypocenter[1] - station.y) ** 2 +
                       (hypocenter[2] - station.z) ** 2)
    if distance == 0:
        return np.zeros(4)
    partials = np.array([(hypocenter[0] - station.x) / (wave_speed * distance),
                         (hypocenter[1] - station.y) / (wave_speed * distance),
                         (hypocenter[2] - station.z) / (wave_speed * distance),
                         1])
    return partials


def update_estimates(estimates, adjustments):
    return estimates + adjustments


def predict_arrival_time(hypocenter, station, wave_speed):
    distance = np.sqrt((hypocenter[0] - station.x) ** 2 +
                       (hypocenter[1] - station.y) ** 2 +
                       (hypocenter[2] - station.z) ** 2)
    travel_time = distance / wave_speed
    return travel_time + station.correction


def jhd_algorithm(arrival_times, initial_hypocenters, stations, weights, wave_speed=3000, max_iterations=100,
                  tolerance=1e-5):
    num_events = initial_hypocenters.shape[0]
    num_stations = len(stations)

    hypocenters = initial_hypocenters.copy()
    station_corrections = np.array([station.correction for station in stations])

    for iteration in range(max_iterations):
        residuals = []
        partial_derivatives = []
        weights_list = []

        # Шаг 1: Вычисляем остатки времени прибытия
        for event_idx in range(num_events):
            for station_idx in range(num_stations):
                if arrival_times[event_idx, station_idx] != -1:
                    predicted_time = predict_arrival_time(hypocenters[event_idx], stations[station_idx], wave_speed)
                    residual = compute_residuals(arrival_times[event_idx, station_idx], predicted_time)
                    residuals.append(residual)

                    # Шаг 2: Вычисляем частные производные
                    partial_derivative = compute_partial_derivatives(hypocenters[event_idx], stations[station_idx],
                                                                     wave_speed)
                    partial_derivatives.append(partial_derivative)
                    weights_list.append(weights[event_idx, station_idx])

        residuals = np.array(residuals)
        partial_derivatives = np.array(partial_derivatives)
        weights_list = np.array(weights_list)

        # Шаг 3: Решаем систему уравнений для поправок
        W = np.diag(weights_list)
        G = np.dot(W, partial_derivatives)
        y = np.dot(W, residuals)

        # Решение нормальных уравнений методом наименьших квадратов
        adjustments, _, _, _ = np.linalg.lstsq(G, y, rcond=None)

        # Шаг 4: Обновляем оценки
        hypocenter_adjustments = adjustments[:num_events * 3].reshape((num_events, 3))
        station_correction_adjustments = adjustments[num_events * 3:]

        hypocenters = update_estimates(hypocenters, hypocenter_adjustments)
        station_corrections = update_estimates(station_corrections, station_correction_adjustments)

        # Обновляем станционные поправки
        for i, station in enumerate(stations):
            station.correction = station_corrections[i]

        # Проверяем сходимость
        if np.all(np.abs(hypocenter_adjustments) < tolerance) and np.all(
                np.abs(station_correction_adjustments) < tolerance):
            break

    return hypocenters, stations


# Пример входных данных
arrival_times = np.array([[0.0, 0.22999999999999998, -1.0, 0.5025, -1.0, 0.12749999999999995, 0.4890000000000003],
                          [0.0, 0.24099999999999966, -1.0, 0.2469999999999999, -1.0, 0.1419999999999999,
                           0.5179999999999998]])

stations = [Station(x=77107.3, y=26832.9, z=-151.0),
            Station(x=78958.7, y=26681.8, z=-216.0),
            Station(x=77339.5, y=26663.3, z=-167.0),
            Station(x=78936.6, y=26014.3, z=-130.8),
            Station(x=77476.3, y=27577.8, z=-206.0),
            Station(x=78012.5, y=26405.8, z=-233.0),
            Station(x=79566.5, y=26242.0, z=-91.0)]

initial_hypocenters = np.array([np.mean([[station.x, station.y, station.z] for station in stations], axis=0)])

weights = np.where(arrival_times != -1, 1, 0)

# Запуск алгоритма
hypocenters, updated_stations = jhd_algorithm(arrival_times, initial_hypocenters, stations, weights)

print("Гипоцентры землетрясений:", hypocenters)
print("Станционные поправки:")
for station in updated_stations:
    print(station)
