import numpy as np
import square_compute
import json
import zipfile
import io
import struct
import event_file_reader as er
import square_compute as sc

# Пример использования


def load_file_as_byte_array(file_path):
    with open(file_path, "rb") as file:
        byte_array = file.read()
    return byte_array
f = load_file_as_byte_array("test.event")
ev = er.try_read(f)
stations=[]
dt=ev.header.datchiki
observed_times=[]
initional=[0,0,0,0]
ngates=0
ev.header.printMe()

for d in dt:
     print(d.Introduction)
     if d.Introduction:#range(5):
        stations.append((d.x,d.y,d.z))
        observed_times.append(d.introInX)
        initional[0]+=d.x
        initional[1]+= d.y
        initional[2] += d.z
        initional[3] += d.introInX
        ngates+=1
# for  i in range(3)       :
#     a=initional[i]/ngates
#     initional[i]=a
# initional.append(3)
#
print(stations,observed_times,initional,ngates)
#
#
#     # stations.append(dt.x,dt.y,dt.z)
# # print("Gauge coords and intro timings")
# # # ev.header.printMe()
# # # print("Saved catalog info:")
# # # ev.catInfo.printMe()
# observed_times = (445.49390077, 189.00395223, 141.73896415, 398.67314872 ) # Наблюдаемые времена прихода
# initial_guess = ( 140, 77107.3, 26832, -150, 3)  # Начальное предположение (t0, x0, y0, z0, v)
# stations = [(77107.3, 26832.9, -151), (78958.7, 26681.8, -216), (78012.5, 26405.8, -233), (79566.5, 26242, -91)]
#
# hypocenter =sc.geiger_method(observed_times, initial_guess, stations)
# print("Определенные параметры гипоцентра:", hypocenter)
# print(sc.compute_travel_times( 78411.250,26540.625,-172.750,3,stations))
#
# hypocenter =sc.geiger_method(observed_times, initional, stations)
#
# print("Определенные параметры гипоцентра:", hypocenter)
# print(sc.compute_travel_times(hypocenter[0],hypocenter[1],hypocenter[2],hypocenter[3],stations))
# # print(sc.compute_travel_times(hypocenter,stations))
# ev.catInfo.printMe()