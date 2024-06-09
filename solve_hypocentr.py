import numpy as np
from scipy.optimize import minimize
import event_file_reader as er
import square_compute as sc
import gird_searh
import seismic_sensors
import points
def calculate_travel_time(x, y, z, x0, y0, z0, v):
    """Рассчитывает время прохождения волны от гипоцентра до станции."""
    return np.sqrt((x - x0)**2 + (y - y0)**2 + (z - z0)**2) / v

def objective_function(params, x, y, z, t, v):
    """Функция потерь, которую мы минимизируем: сумма квадратов временных остатков."""
    if t.all !=np.inf:
        t0, x0, y0, z0 = params
        residuals = t - (t0 + calculate_travel_time(x, y, z, x0, y0, z0, v))
        return np.sum(residuals**2)
    else:
        return 0

def find_hypocenter(x, y, z, t, v, initial_guess):
    """Находит гипоцентр, минимизируя функцию потерь."""
    result = minimize(objective_function, initial_guess, args=(x, y, z, t, v),
                      method='BFGS', options={'disp': True})
    return result.x
ev=er.load_event_from_path("test.event")
ssa=seismic_sensors.SeismicSensorArray.from_header(ev.header)
# Пример данных: координаты станций, времена прихода и скорости распространения

stations=np.array(ssa.locations)
v=ssa.velocities
t=ssa.observed_times
# Начальное предположение о времени и местоположении гипоцентра
initial_guess = [0, 0,0,0]  # t0, x0, y0, z0

# Вызов функции для поиска гипоцентра
hypocenter = find_hypocenter(stations[:, 0], stations[:, 1], stations[:, 2], t, v, initial_guess)
print(f"Оценка гипоцентра: время {hypocenter[0]}, координаты ({hypocenter[1]}, {hypocenter[2]}, {hypocenter[3]})")