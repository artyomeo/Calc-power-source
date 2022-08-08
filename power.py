import re
import sys
import os
import numpy as np
import pandas as pd
from scipy import integrate as integrate
from datetime import datetime as time
import re

def search_file ():
    file_csv = ''

    for file in sorted(os.listdir(os.getcwd())):
        if file.endswith(".csv"):
            point = open(file, 'r')
            line = point.readline()
            point.close()
            if (line.startswith("time") & (line.find("V(") > 0) & (line.find("I(") > 0)):
                file_csv = file
        elif file.endswith(".txt"):
            point = open(file, 'r')
            line = point.readline()
            point.close()
            if (line.startswith("time") & (line.find("V(") > 0) & (line.find("I(") > 0)):
                point = open(file, 'r')
                data = point.read()
                data = data.replace('	', ';')
                point.close()
        
                file_csv = file.replace('.txt', '.csv')
                point = open(file_csv, 'w')
                point.write(data)
                point.close()

    if (file_csv == ''):
        sys.exit("\nNot found file for analysis!\n")
    else:
        return file_csv

def min_amount(name_file=''):
    point = open(name_file, 'r')
    line = point.readline()
    point.close()

    return min(len(re.findall(r'V\(', line)), len(re.findall(r'I\(', line)))

def find_VI (data=pd.DataFrame(), num=1):
    bias_V=num
    bias_I=num
    for i in (range(1, data.shape[1])):
        if(data.columns[i].startswith('V(') | data.columns[i].startswith('-V(')):
            if (bias_V == 1):
                save_v=i
                bias_V = 0
            else:
                bias_V = bias_V-1

        if(data.columns[i].startswith('I(') | data.columns[i].startswith('-I(')):
            if (bias_I == 1):
                save_i=i
                bias_I = 0
            else:
                bias_I = bias_I-1
    
    return [save_v, save_i]

def calculation (data=pd.DataFrame(), num=1):

    position_VI = find_VI(data, num)

    var_x = data[data.columns[0]]
    var_yv = data[data.columns[position_VI[0]]]
    var_yi = data[data.columns[position_VI[1]]]
    dt = var_x[var_x.size-1]-var_x[0]
    Vrms=(integrate.trapz((var_yv**2), var_x)/dt)**(0.5)
    Irms=(integrate.trapz((var_yi**2), var_x)/dt)**(0.5)
    Prms=(integrate.trapz((var_yv*var_yi), var_x)/dt)
    Srms=Vrms*Irms
    Xrms=Prms/Srms

    return {'Vrms': Vrms, 'Irms': Irms, 'Prms': Prms, 'Srms' : Srms, 'Xrms' : Xrms}

def mean_signal (data=pd.DataFrame()):
    var_x = data[data.columns[0]]
    var_yv = data[data.columns[1]]
    dt = var_x[var_x.size-1]-var_x[0]
    
    return integrate.trapz(var_yv, var_x)/dt

start_time = time.now()

file = search_file()
data_csv = pd.read_csv (file, sep=';')
print("Data analysis from file: %s"%(file))

# находим первый массив напряжений, на который будем ориентироваться: поиск точек периода
first_VI=find_VI(data_csv)
# расчитываем среднее значение, чтобы заждать линию, через которую будем искать период
mean_first_V=mean_signal(data_csv[[data_csv.columns[0],data_csv.columns[first_VI[0]]]])
# не всегда точки будут ровно пересекать определенную точку, нужно задать диапазон, 
# в пределах которого точка будет считаться пересечением среднего значения
step_V=np.abs((mean_first_V-data_csv[data_csv.columns[1]].max())*0.005)

#logic = pd.concat([pd.Series([True]), (data_csv[data_csv.columns[1][0:data_csv.shape[0]-1]] < 0.0)], ignore_index=True) #! в принципе можно и так вместо concat+drop, но так медленнее

logic = pd.concat([pd.Series([True]), (data_csv[data_csv.columns[1]] < mean_first_V)], ignore_index=True)    #! добавление к массиву (data[data.columns[1]] < 0.0) элемента в начало
logic = logic.drop(labels=[logic.shape[0]-1])                            #! удаление последнего элемента для сохранения исходной размерности
zero_V1 = data_csv.loc[(data_csv[data_csv.columns[1]] < (mean_first_V+step_V)) & (data_csv[data_csv.columns[1]] > (mean_first_V-step_V)) & logic]

var = np.int_(zero_V1.shape[0]-1)
Num_of_period = 10
# https://pythonworld.ru/obrabotka-dannyx/pandas-cookbook-2.html
VI_data = data_csv[zero_V1.index[var-Num_of_period]:zero_V1.index[var]+1]
# https://pynative.com/pandas-reset-index/#:~:text=df.drop_duplicates()-,Use%20DataFrame.reset_index()%20function,of%20numbers%20starting%20at%200.
VI_data = VI_data.reset_index(drop=True)

# https://docs.python.org/3/tutorial/inputoutput.html
print("\n----------------------------------------------------------------------------------------------")
for i in range(1, min_amount(file)+1):
    source = calculation(VI_data, i)
    print(f"| V{i:1}rms: {source['Vrms']:.3f} V | I{i:1}rms: {source['Irms']:.3f} A | P{i:1}rms: {source['Prms']:.3f} W | S{i:1}rms: {source['Srms']:.3f} VA | X{i:1}rms: {source['Xrms']:.3f} |")
print("----------------------------------------------------------------------------------------------\n")

print(f'Total time of program: {time.now()-start_time}\n')