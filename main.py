import numpy as np
import pandas as pd
import event_file_reader as er
import square_compute as sc
import gird_searh as gs
import solve_hypocentr as sh
import  writer
import seismic_sensors as ss
import  visual
import test_calcs as tc

filepath='Antonovskaya_joint_test.xlsx'
filepath2='Antonovskaya_gauges.txt'
filepath3='newAntonovskaya_joint_test.xlsx'
tc.gss_massive_calculation_from_file_path(filepath,filepath2,4,200)
# tc.geiger_massive_calculation_from_file_path(filepath,filepath2,99,0.000001)
visual.plot_coordinates_from_excel(filepath3)
