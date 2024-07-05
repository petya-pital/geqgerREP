import numpy as np
import jhd as hd
import solve_hypocentr as  sc
def generate_synthetic_data(num_earthquakes, num_stations, true_hypocenters, stations,):
    times = np.zeros((num_earthquakes, num_stations))
    for i in range(num_earthquakes):
        for j in range(num_stations):
            distance = np.linalg.norm(true_hypocenters[i, :3] - stations[j])
            travel_time = distance / 3000
            times[i, j] = travel_time + true_hypocenters[i, 3]
    return times


def jhd(num_earthquakes, num_stations, initial_hypocenters, observed_times, stations, iterations=10):
    hypocenters = initial_hypocenters.copy()
    for _ in range(iterations):
        A = []
        b = []
        for i in range(num_earthquakes):
            for j in range(num_stations):
                distance = np.linalg.norm(hypocenters[i, :3] - stations[j])
                if distance == 0:
                    continue
                theoretical_time = distance /3000 + hypocenters[i, 3]
                residual = observed_times[i, j] - theoretical_time
                partial_derivatives = (hypocenters[i, :3] - stations[j]) / (distance * 3000)
                A.append(np.hstack((partial_derivatives, 1)))
                b.append(residual)

        A = np.array(A)
        b = np.array(b)

        if A.shape[0] < 4 * num_earthquakes:
            print("Insufficient data to solve for all hypocenters. Check your input data and initial hypocenters.")
            break

        delta_hypocenters, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

        # Проверка размерностей перед обновлением гипоцентров
        if delta_hypocenters.size == 4 * num_earthquakes:
            for i in range(num_earthquakes):
                hypocenters[i, :3] += delta_hypocenters[4 * i:4 * i + 3]
                hypocenters[i, 3] += delta_hypocenters[4 * i + 3]
        else:
            print("Mismatch in the size of delta_hypocenters.")
            break

    return hypocenters
#
# # Заданные координаты гипоцентров землетрясений (x, y, z, t)
true_hypocenters = np.array([
    [10, 20, 30, 0],
    [40, 50, 60, 1],
    [70, 80, 90, 2],
    [25, 35, 45, 1.5],
    [55, 65, 75, 2.5]
])
# Заданные координаты станций (x, y, z)
stations = np.array([
    [0, 0, 0],
    [10, 0, 0],
    [20, 0, 0],
    [0, 10, 0],
    [0, 20, 0],
    [10, 10, 0],
    [20, 20, 0],
    [30, 30, 0],
    [40, 40, 0],
    [50, 50, 0]
])
stations=sc.create_location('Antonovskaya_gauges.txt')
print(stations)
num_stations=len(stations)
#
# # Предположим постоянную модель скорости
velocity_model = 3000
#
# # Генерация синтетических данных
observed_times = generate_synthetic_data(len(true_hypocenters), len(stations), true_hypocenters, stations,
                                         velocity_model)
events_date_list=sc.create_list_event_date_from_exel('Antonovskaya_joint_test.xlsx')
observed_times,num_events=sc.create_observed_times_list_and_num_events(events_date_list)
print(observed_times)
print(num_events)
true_hypocenter=sc.create_real_cords_from_event_date_list(events_date_list)
print(true_hypocenter)
# Начальные предположения для гипоцентров (могут быть близки к истине или случайными)
initial_hypocenters = np.array([
    [12, 22, 32, 0.5],
    [38, 48, 58, 1.5],
    [68, 78, 88, 2.5],
    [28, 38, 48, 1.0],
    [53, 63, 73, 3.0]
])
initial_hypocenters=sc.create_initial_estimates(num_events)
# # Выполнение JHD
# estimated_hypocenters = jhd(len(true_hypocenters), len(stations), initial_hypocenters, observed_times, stations,

estimated_hypocenters = jhd(num_events, num_stations, initial_hypocenters, observed_times, stations,
                            velocity_model)
print("True hypocenters:")
print(true_hypocenters)
print("Estimated hypocenters:")
print(estimated_hypocenters)
st=[]
for i in range(len(stations)):
    S=sc.Station(stations[i][0],stations[i][1],stations[i][2])
    st.append(S)
print(st)
num_events=len(true_hypocenters)
num_stations=len(stations)
eq=hd.create_equations_type_3(observed_times,initial_hypocenters,len(true_hypocenters), len(stations),st)
DeltaX,DeltaS=hd.solve_joint_hypocenter(eq,num_events,num_stations)
focal_param=hd.get_focal_parameters(DeltaX,num_events)
hd.print_focal_parameters(focal_param)
calc_cords=hd.get_coordinates_without_time(focal_param)
hd.compare_real_and_computed(true_hypocenters,calc_cords)
hd.plot_comparison_all(true_hypocenters,calc_cords)
#
