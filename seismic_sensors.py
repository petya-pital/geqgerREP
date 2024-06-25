import numpy as np
import event_file_reader as er

class SeismicSensorArray:
    def __init__(self, locations, velocities, observed_times, detections,sensor_names=None):
        """
        Инициализирует массив сейсмических датчиков.

        :param locations: Массив местоположений датчиков (N x 3).
        :param velocities: Массив скоростей распространения P-волн для каждого датчика (N).
        :param sensor_names: Опциональный массив с типами датчиков (N).
        """
        self.locations = locations
        self.velocities = np.array(velocities)
        self.observed_times=np.array(observed_times)
        self.detections=detections
        self.sensor_names = sensor_names if sensor_names is not None else ['default'] * len(locations)
        self.sensor_numbers=len(locations)

    @classmethod

    def from_header(cls, header,d=False): #true => add all data without nondetected gauge
        locations = []

        velocities = []
        sensor_names = []
        detections=[]
        observed_times=[]
        for datchik in header.datchiki:
            if datchik.Introduction or d:
                detections.append(datchik.Introduction)
                A = [datchik.x, datchik.y, datchik.z]
                locations.append(A)
                velocities.append(datchik.v)
                sensor_names.append(datchik.Name)
                observed_times.append(datchik.introInX)
                #print(observed_times)
            #print(datchik.Name,[np.round(datchik.x,6), np.round(datchik.y,6), np.round(datchik.z,6)])

            # sensor_names.append(datchik.Name)
            # if datchik.Introduction:
            #     observed_times.append(np.round(datchik.introInX))
            # else:
            #     observed_times.append(np.inf)
        return cls(locations, velocities, observed_times, detections, sensor_names)
    def from_event_header(ev:er.Event):
        hd=ev.header
        return hd.from_header()
    def from_file_path(file_path):
        ev=er.load_event_from_path()
        hd=ev.header
        return hd.from_header()
    def __str__(self):
        return f"Seismic Sensor Array with {len(self.locations)} sensors"
    def printMe(self):
        print( f"Seismic Sensor Array with {len(self.locations)} sensors ")
        for index in range(len(self.locations)):
            print(self.get_sensor_info(index))
    def get_sensor_info(self, index):
        """
        Возвращает информацию о датчике по указанному индексу.

        :param index: Индекс датчика в массиве.
        :return: Информация о датчике.
        """
        location = self.locations[index]
        velocity = self.velocities[index]
        sensor_name = self.sensor_names[index]
        detection=self.detections[index]
        observed_time=self.observed_times[index]
        return f"Type: {sensor_name}, Location: {location}, Velocity: {velocity},Detection: {detection}, Observed_time= {observed_time} "
    # def getDetectedData(self):
    #
    #     for i in range(self.sensor_numbers):
    #         if self.detections[i]:
    #             self.locations
    #         if i self.lo

# class SeismicSensor:
#     def __init__(self, location, velocitie, observed_time, detection, sensor_name=None):
#         self.velocitie=velocitie
#         self.detection=detection
#         self.location=location
#         self.observed_time=observed_time
#         self.name=sensor_name
# def ArrayfromSensors(SensorsArray):
#     for i in SensorsArray:

