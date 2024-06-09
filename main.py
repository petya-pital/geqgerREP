import numpy as np
import event_file_reader as er
import square_compute as sc
import gird_searh as gs
import seismic_sensors as ss
#file_path='Осинниковская 22_10_2021 05_51_12.event'
# sc.geiger_from_file_path('test.event',90000,0.001,True,initial_guess=[0,0, 25248.0, 6.0])
# gs.gird_serch_from_file_path('test.event',0.0001,True,True,[22608.0, 25248.0, 6.0 ] )
# sc.geiger_from_file_path(file_path,45000,0.00001,True,initial_guess=[0,47859.0, 30610.0, -17.0])
file_path='Антоновская 29_05_2024 22_44_43.event'
# gs.gird_serch_from_file_path(file_path,0.0001,True,True,istep=500000)
sc.geiger_from_file_path(file_path,70500,0.000001,True,initial_guess=[0,47859.0, 30610.0, -17.0])