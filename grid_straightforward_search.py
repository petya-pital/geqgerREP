import numpy as np

class HypocenterLocator:
    def __init__(self, sensor_coords, detection_times, velocities, scale_factor=2, num_cells=10):
        self.sensor_coords = sensor_coords
        self.detection_times = np.array([dt if dt is not None else np.nan for dt in detection_times], dtype=float)
        self.velocities = velocities
        self.scale_factor = scale_factor
        self.num_cells = num_cells
        self.grid = None

    def expand_bounding_box(self):
        """Расширяет bounding box исходя из координат датчиков и заданного масштабирующего коэффициента."""
        min_coords = np.min(self.sensor_coords, axis=0)
        max_coords = np.max(self.sensor_coords, axis=0)
        center = (min_coords + max_coords) / 2
        expanded_min = center - (center - min_coords) * self.scale_factor
        expanded_max = center + (max_coords - center) * self.scale_factor
        return expanded_min, expanded_max

    def create_grid(self):
        """Создаёт сетку поиска гипоцентра внутри расширенного bounding box."""
        expanded_min, expanded_max = self.expand_bounding_box()
        x = np.linspace(expanded_min[0], expanded_max[0], self.num_cells)
        y = np.linspace(expanded_min[1], expanded_max[1], self.num_cells)
        z = np.linspace(expanded_min[2], expanded_max[2], self.num_cells)
        self.grid = np.array(np.meshgrid(x, y, z)).T.reshape(-1, 3)

    def theoretical_time(self, hypocenter, sensor, velocity):
        """Вычисляет теоретическое время прихода волны от гипоцентра до датчика."""
        return np.linalg.norm(hypocenter - sensor) / velocity

    def calculate_errors(self):
        """Рассчитывает функцию ошибки для каждой точки сетки."""
        errors = []
        for point in self.grid:
            times = np.array([self.theoretical_time(point, sensor, velocity) for sensor, velocity in zip(self.sensor_coords, self.velocities)])
            valid_indices = ~np.isnan(self.detection_times)
            observed_times = self.detection_times[valid_indices]
            computed_times = times[valid_indices]
            source_time = np.mean(observed_times - computed_times)
            residuals = observed_times - (source_time + computed_times)
            error = np.sqrt(np.sum(residuals**2)) / len(observed_times)
            errors.append(error)
        return errors

    def find_hypocenter(self):
        """Находит наиболее вероятное положение гипоцентра, используя сетку и функцию ошибки."""
        self.create_grid()
        errors = self.calculate_errors()
        best_index = np.argmin(errors)
        return self.grid[best_index], errors[best_index]

# Пример использования класса
sensor_coords = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 1]])
detection_times = [0.5, None, 0.7, 0.2, 1.0]
velocities = np.array([5000, 6000, 5000, 5500, 5300])  # Разные скорости для каждого датчика

locator = HypocenterLocator(sensor_coords, detection_times, velocities)
hypocenter, error = locator.find_hypocenter()
print("Estimated hypocenter:", hypocenter, "with error:", error)