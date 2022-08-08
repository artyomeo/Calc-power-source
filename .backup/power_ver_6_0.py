import re
import sys
import os
import numpy as np
import pandas as pd
from scipy import integrate as integrate
from datetime import datetime as time
import re

def calculation (data=pd.DataFrame(), num=1):
    var_x = data[data.columns[0]]
    var_yv = data[data.columns[num]]
    var_yi = data[data.columns[num+3]]
    dt = var_x[var_x.size-1]-var_x[0]
    Vrms=(integrate.trapz((var_yv**2), var_x)/dt)**(0.5)
    Irms=(integrate.trapz((var_yi**2), var_x)/dt)**(0.5)
    Prms=(integrate.trapz((var_yv*var_yi), var_x)/dt)
    Srms=Vrms*Irms
    Xrms=Prms/Srms

    #return [Vrms, Irms, Prms,Prms/(Vrms*Irms)]
    return {'Vrms': Vrms, 'Irms': Irms, 'Prms': Prms, 'Srms' : Srms, 'Xrms' : Xrms}

def open_file ():
    file_csv = ''

    for file in sorted(os.listdir(os.getcwd())):
        if file.endswith(".csv"):
            point = open(file, 'r')
            line = point.readline()
            line = line.lower()
            point.close()
            if (line.startswith("time") & (line.find("v(") > 0) & (line.find("i(") > 0)):
                file_csv = file
        elif file.endswith(".txt"):
            point = open(file, 'r')
            line = point.readline()
            line = line.lower()
            point.close()
            if (line.startswith("time") & (line.find("v(") > 0) & (line.find("i(") > 0)):
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

start_time = time.now()

file = open_file()
data = pd.read_csv (file, sep=';')
print("Data analysis from file: %s"%(file))

# https://overcoder.net/q/3455/добавить-одну-строку-в-панды-dataframe
#V2_per = pd.DataFrame(columns=[data.columns[0], data.columns[1]])
#V2_per.loc[0] = data.iloc[0]

#logic = pd.concat([pd.Series([True]), (data[data.columns[1][0:data.shape[0]-1]] < 0.0)], ignore_index=True) #! в принципе можно и так вместо concat+drop, но так медленнее

logic = pd.concat([pd.Series([True]), (data[data.columns[1]] < 0.0)], ignore_index=True)    #! добавление к массиву (data[data.columns[1]] < 0.0) элемента в начало
logic = logic.drop(labels=[logic.shape[0]-1])                            #! удаление последнего элемента для сохранения исходной размерности
zero_V1 = data.loc[((data[data.columns[1]] < 1.0) & ((data[data.columns[1]] > -1.0))) & logic]

var = np.int_(zero_V1.shape[0]-1)
# https://pythonworld.ru/obrabotka-dannyx/pandas-cookbook-2.html
Num_of_period = 10
V1_per = data[zero_V1.index[var-Num_of_period]:zero_V1.index[var]+1]
del V1_per[data.columns[4]]
# https://pynative.com/pandas-reset-index/#:~:text=df.drop_duplicates()-,Use%20DataFrame.reset_index()%20function,of%20numbers%20starting%20at%200.
V1_per = V1_per.reset_index(drop=True)

# https://docs.python.org/3/tutorial/inputoutput.html
print("\n----------------------------------------------------------------------------------------------")
for i in range(1, 4):
    source = calculation(V1_per, i)
    #print(f' V{i:1}rms: {source[0]:.4f} V | I{i:1}rms: {source[1]:.4f} A | P{i:1}rms: {source[2]:.4f} W | X{i:1}rms: {source[3]:.4f} ')
    print("| V{:1}rms: {:.3f} V | I{:1}rms: {:.3f} A | P{:1}rms: {:.3f} W | S{:1}rms: {:.3f} VA | X{:1}rms: {:.3f} |".format(i, source['Vrms'], i, source['Irms'], i, source['Prms'], i, source['Srms'], i, source['Xrms']))
print("----------------------------------------------------------------------------------------------\n")

print(f'Total time of program: {time.now()-start_time}\n')