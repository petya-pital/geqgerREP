import numpy as np
import seismic_sensors

class EPoint:
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
    def dist(self,other):
        return np.linalg.norm(np.array([self.x,self.y,self.z])-np.array([other.x,other.y,other.z]))
    def get_vector(self):
        return numpy.array([self.x,self.y,self.z])
A=EPoint(1,2,3)
B=EPoint(2,4,444)
(print
(A.dist(B)))
class FPoint(EPoint):
    def __init__(self,x,y,z,t=None):
        self.x=x
        self.y=y
        self.z=z
        self.t=numpy.infty
        self.t=t
    def Tdist(self,other):
        return np.linalg.norm(np.array([self.x,self.y,self.z.self.t])-np.array([other.x,other.y,other.z,other.t]))





def theoretical_time(pointA, pointB, velocity):
    distance = np.linalg.norm(pointA - pointB)
    return distance / velocity


def residual_sum_squares(TestPoint, sensors: seismic_sensors.SeismicSensorArray):
    residuals = 0
    for i in range(sensors.sensor_numbers - 1):
        if sensors.detections[i]:
            time = theoretical_time(TestPoint, sensors.locations[i], sensors.velocities[i])
            residuals += (time - sensors.observed_times[i]) ** 2
    return residuals
def residual_sum_squares_c(TestPoint, sensors,velocities):
    residuals = 0
    for i in range(len(sensors)):
        time = theoretical_time(TestPoint,sensors[i], velocities[i])
        residuals += (time - sensors.observed_times[i]) ** 2
    return residuals

