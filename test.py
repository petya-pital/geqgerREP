import numpy as np


class Station:
    def __init__(self,x,y,z,name=None,correction=0):
        self.x = x
        self.y = y
        self.z = z
        self.name=name
        self.correction=correction

class EventInModel:
    def __init__(self, times, true_coordinates):
        self.times = np.array(times)
        self.weights = np.where(self.times == -1, 0, 1)
        self.true_coordinates = np.array(true_coordinates)

    def __str__(self):
        return f"Times: {self.times}\nWeights: {self.weights}\nTrue Coordinates: {self.true_coordinates}"


class Model:
    def __init__(self, locations, sensor_names=None):
        self.N = len(locations)
        self.locations = np.array(locations)
        self.sensor_names = sensor_names if sensor_names is not None else [f"Sensor_{i + 1}" for i in range(self.N)]

    def __str__(self):
        sensor_info = "\n".join([f"{name}: {loc}" for name, loc in zip(self.sensor_names, self.locations)])
        return f"Number of sensors (N): {self.N}\nLocations:\n{sensor_info}"


class EventsDate:
    def __init__(self, model, events):
        if not isinstance(model, Model):
            raise ValueError("model must be an instance of the Model class")
        self.model = model
        self.N = model.N
        self.events = events if all(isinstance(event, EventInModel) for event in events) else []

    def __str__(self):
        events_info = "\n".join([str(event) for event in self.events])
        return f"Model: \n{self.model}\n\nNumber of sensors (N): {self.N}\n\nEvents:\n{events_info}"


def calculate_partial_derivatives():
    # Здесь нужно определить конкретные частные производные в зависимости от задачи
    return np.array([1, 1, 1])


# Функция для создания матрицы весов (пример)
def create_weight_matrix(times):
    weights = np.where(times == -1, 0, 1)
    return np.diag(weights)

# Функция для создания уравнений типа 3
def create_equations_type_3(observed_times, initial_estimates,  num_events, num_stations, stations):
    equations = []

    for j in range(num_events):
        W_j = create_weight_matrix(num_stations)
        A_j = np.zeros((num_stations, 4))
        r_j = np.zeros(num_stations)

        for i in range(num_stations):
            partials = calculate_partial_derivatives()
            A_j[i, :] = [1, partials[0], partials[1], partials[2]]
            r_j[i] = observed_times[j, i] - (initial_estimates[j, 0] + station_corrections[i])

        equations.append((W_j, A_j, r_j))

    return equations
# Пример использования:
locations = [
    [0.0, 1.0, 2.0],
    [3.0, 4.0, 5.0],
    [6.0, 7.0, 8.0]
]
sensor_names = ["Sensor_A", "Sensor_B", "Sensor_C"]
model = Model(locations, sensor_names)

event1 = EventInModel([0, -1, 5], [1.0, 2.0, 3.0])
event2 = EventInModel([3, 2, -1], [4.0, 5.0, 6.0])
events = [event1, event2]

events_date = EventsDate(model, events)
print(events_date)
