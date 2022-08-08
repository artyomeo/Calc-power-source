import sys
import os
import numpy as np
import pandas as pd
from scipy import integrate as integrate
from datetime import datetime as time

def calculation (data=pd.DataFrame(), num=1):
    var_x = data[data.columns[0]]
    T = var_x[var_x.size-1]-var_x[0]
    var_yv = data[data.columns[num]]
    Vrms=(integrate.trapz((var_yv**2), var_x)/T)**(0.5)
    var_yi = data[data.columns[num+3]]
    Irms=(integrate.trapz((var_yi**2), var_x)/T)**(0.5)
    Prms=(integrate.trapz((var_yv*var_yi), var_x)/T)
    Srms=Vrms*Irms
    Xrms=Prms/Srms

    #return [Vrms, Irms, Prms,Prms/(Vrms*Irms)]
    return {'Vrms': Vrms, 'Irms': Irms, 'Prms': Prms, 'Srms' : Srms, 'Xrms' : Xrms}

def open_file ():
    cur_dir = os.getcwd() # Dir from where search starts can be replaced with any path

    name_file=''
    for file in os.listdir(cur_dir):
        if file.endswith(".csv"):
            name_file=file

    if(name_file == ''):
        for file in os.listdir(cur_dir):
            if file.endswith(".txt"):
                name_file=file

    if (name_file == ''):
        sys.exit()
    del cur_dir
    del file

    if(name_file.endswith(".txt")):
        point_file = open(name_file, 'r')
        data = point_file.read()
        data = data.replace('	', ';')
        point_file.close()
        
        name_file = name_file.replace('.txt', '.csv')
        point_file = open(name_file, 'w')
        point_file.write(data)
        point_file.close()

    if (name_file == ''):
        sys.exit()
    else:
        return name_file

start_time = time.now()

data = pd.read_csv (open_file(), sep=';')

# https://overcoder.net/q/3455/добавить-одну-строку-в-панды-dataframe
#V2_per = pd.DataFrame(columns=[data.columns[0], data.columns[1]])
#V2_per.loc[0] = data.iloc[0]

# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop.html
#data.drop(labels = [2],axis = 0)
logic = pd.concat([pd.Series([True]), (data[data.columns[1]] < 0.0)])
logic = logic.reset_index(drop=True)
logic = logic.drop(labels=[logic.shape[0]-1])
zero_V1 = data.loc[(data[data.columns[1]] == 0.0) & logic]

#zero_var = data.loc[data[data.columns[1]] == 0.0]
#zero_V1 = pd.DataFrame(columns=data.columns)
#data.shape[0] - получение размерности таблицы данных в виде (x,y), [0] - получение длины, [1] - ширины

#for i in range(0, zero_var.shape[0]):
#    if(((data.iloc[zero_var.index[i]][data.columns[1]] == 0.0) & (data.iloc[zero_var.index[i]-1][data.columns[1]] < 0.0)) |
#        ((data.iloc[zero_var.index[i]][data.columns[1]] == 0.0) & (i == 0))):
#        zero_V1 = pd.concat([zero_V1, zero_var.iloc[[i]]])
#del zero_var
#print(zero_V1)

var = np.int_(zero_V1.shape[0]-1)
# https://pythonworld.ru/obrabotka-dannyx/pandas-cookbook-2.html
Num_of_period = 10
V1_per = data[zero_V1.index[var-Num_of_period]:zero_V1.index[var]+1]
del V1_per[data.columns[4]]
del var
# https://pynative.com/pandas-reset-index/#:~:text=df.drop_duplicates()-,Use%20DataFrame.reset_index()%20function,of%20numbers%20starting%20at%200.
V1_per = V1_per.reset_index(drop=True)
#print(V1_per)

# https://docs.python.org/3/tutorial/inputoutput.html
print("\n----------------------------------------------------------------------------------------------")
for i in range(1, 4):
    source = calculation(V1_per, i)
    #print(f' V{i:1}rms: {source[0]:.4f} V | I{i:1}rms: {source[1]:.4f} A | P{i:1}rms: {source[2]:.4f} W | X{i:1}rms: {source[3]:.4f} ')
    print("| V{:1}rms: {:.3f} V | I{:1}rms: {:.3f} A | P{:1}rms: {:.3f} W | S{:1}rms: {:.3f} VA | X{:1}rms: {:.3f} |".format(i, source['Vrms'], i, source['Irms'], i, source['Prms'], i, source['Srms'], i, source['Xrms']))
print("----------------------------------------------------------------------------------------------\n")

print('\nTotal time of program: ', end='')
print(time.now()-start_time)