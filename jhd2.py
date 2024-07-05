import numpy as np
import pandas as pd


class EventDate:
    def __init__(self, date, real_coordinates, speed, number_of_sensors, arrival_times):
        self.date = date
        self.real_coordinates = real_coordinates
        self.speed = speed
        self.number_of_sensors = number_of_sensors
        self.arrival_times = arrival_times

    def __repr__(self):
        return (f"EventDate(date={self.date}, real_coordinates={self.real_coordinates}, "
                f"speed={self.speed} "
                f"arrival_times={self.arrival_times})")


def create_location(filepath):
    data = np.loadtxt(filepath, dtype=str, encoding='utf-8-sig')
    data[:, 1:4] = np.char.replace(data[:, 1:4], ',', '.')
    coordinates = data[:, 1:4].astype(float)
    return coordinates


def create_list_event_date_from_exel(filepath):
    events_data = pd.read_excel(filepath, skiprows=4, engine='openpyxl')
    list_of_events = [
        EventDate(
            date=row['Дата и время UTC+7'],
            real_coordinates=[row['X'], row['Y'], row['Z']],
            speed=row['V'],
            number_of_sensors=row['N датчиков'],
            arrival_times=row[['intro_1', 'intro_2', 'intro_3', 'intro_4', 'intro_5', 'intro_6', 'intro_7']].tolist()
        )
        for index, row in events_data.iterrows()
    ]
    return list_of_events


def prepare_data(events, num_stations):
    data = []
    for event_id, event in enumerate(events):
        for station_id in range(num_stations):
            arrival_time = event.arrival_times[station_id]
            if arrival_time != -1:
                data.append([event_id, station_id, arrival_time, 1.0])
            else:
                data.append([event_id, station_id, 0.0, 0.0])  # Время 0.0, вес 0.0
    return np.array(data)


def jhd_iterative(data, num_events, num_stations, station_positions, velocity, learning_rate=0.01, max_iterations=1000,
                  tolerance=1e-6):
    hypocenters, station_corrections = initialize_parameters(num_events, num_stations)

    for iteration in range(max_iterations):
        residuals = compute_residuals(hypocenters, station_corrections, data, station_positions, velocity)
        J = compute_jacobian(hypocenters, station_corrections, data, station_positions, velocity)

        delta_params = np.linalg.lstsq(J, residuals, rcond=None)[0]

        hypocenters += delta_params[:num_events * 4].reshape((num_events, 4)) * learning_rate
        station_corrections += delta_params[num_events * 4:] * learning_rate

        if np.linalg.norm(delta_params) < tolerance:
            print(f"Сошлось на итерации {iteration}")
            break

    return hypocenters, station_corrections


def initialize_parameters(num_events, num_stations):
    hypocenters = np.random.rand(num_events, 4)
    station_corrections = np.zeros(num_stations)
    return hypocenters, station_corrections


def compute_travel_time(hypocenter, station_position, velocity):
    return np.linalg.norm(hypocenter[:3] - station_position) / velocity


def compute_residuals(hypocenters, station_corrections, data, station_positions, velocity):
    residuals = []
    for event in data:
        event_id = int(event[0])
        station_id = int(event[1])
        observed_time = event[2]
        weight = event[3]
        if weight > 0:
            travel_time = compute_travel_time(hypocenters[event_id], station_positions[station_id], velocity)
            residual = weight * (
                        observed_time - (travel_time + hypocenters[event_id][3] + station_corrections[station_id]))
        else:
            residual = 0.0
        residuals.append(residual)
    return np.array(residuals)


def compute_jacobian(hypocenters, station_corrections, data, station_positions, velocity):
    num_events = hypocenters.shape[0]
    num_stations = station_corrections.shape[0]
    num_params = num_events * 4 + num_stations
    J = np.zeros((len(data), num_params))

    for idx, event in enumerate(data):
        event_id = int(event[0])
        station_id = int(event[1])
        observed_time = event[2]
        weight = event[3]

        if weight > 0:
            hypocenter = hypocenters[event_id]
            station_position = station_positions[station_id]

            travel_time = compute_travel_time(hypocenter, station_position, velocity)
            distance = np.linalg.norm(hypocenter[:3] - station_position)

            J[idx, event_id * 4] = weight * (hypocenter[0] - station_position[0]) / (distance * velocity)
            J[idx, event_id * 4 + 1] = weight * (hypocenter[1] - station_position[1]) / (distance * velocity)
            J[idx, event_id * 4 + 2] = weight * (hypocenter[2] - station_position[2]) / (distance * velocity)
            J[idx, event_id * 4 + 3] = weight
            J[idx, num_events * 4 + station_id] = weight
        else:
            J[idx, event_id * 4] = 0
            J[idx, event_id * 4 + 1] = 0
            J[idx, event_id * 4 + 2] = 0
            J[idx, event_id * 4 + 3] = 0
            J[idx, num_events * 4 + station_id] = 0

    return J


# filepath='Antonovskaya_joint_test.xlsx'
# filepath2='Antonovskaya_gauges.txt'
station_filepath = 'Antonovskaya_gauges.txt'
events_filepath = 'Antonovskaya_joint_test.xlsx'

station_positions = create_location(station_filepath)
events = create_list_event_date_from_exel(events_filepath)

num_events = len(events)
num_stations = len(station_positions)

data = prepare_data(events, num_stations)
velocity = 3000

final_hypocenters, final_station_corrections = jhd_iterative(data, num_events, num_stations, station_positions,
                                                                 velocity)

print("Final Hypocenters:\n", final_hypocenters)
print("Final Station Corrections:\n", final_station_corrections)
