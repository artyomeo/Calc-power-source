import sys
import os
import numpy as np
import pandas as pd
from scipy import integrate as integrate

cur_dir = os.getcwd() # Dir from where search starts can be replaced with any path

var=''
for file in os.listdir(cur_dir):
    if file.endswith(".csv"):
        var=file

if(var == ''):
    for file in os.listdir(cur_dir):
        if file.endswith(".txt"):
            var=file

if (var == ''):
    sys.exit()
del cur_dir
del file

if(var.endswith(".txt")):
    point_file = open(var, 'r')
    data = point_file.read()
    data = data.replace('	', ';')
    point_file.close()
    
    var = var.replace('.txt', '.csv')
    point_file = open(var, 'w')
    point_file.write(data)
    point_file.close()
#print(var)

data = pd.read_csv (var, sep=';')
#print(data)
del var

# https://overcoder.net/q/3455/добавить-одну-строку-в-панды-dataframe
#V2_per = pd.DataFrame(columns=[data.columns[0], data.columns[1]])
#V2_per.loc[0] = data.iloc[0]

# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop.html
#data.drop(labels = [2],axis = 0)
zero_var = data.loc[data[data.columns[1]] == 0.0]
zero_V1 = pd.DataFrame(columns=data.columns)
#data.shape[0] - получение размерности таблицы данных в виде (x,y), [0] - получение длины, [1] - ширины
for i in range(0, zero_var.shape[0]):
    if(((data.iloc[zero_var.index[i]][data.columns[1]] == 0.0) & (data.iloc[zero_var.index[i]-1][data.columns[1]] < 0.0)) |
        ((data.iloc[zero_var.index[i]][data.columns[1]] == 0.0) & (i == 0))):
        zero_V1 = pd.concat([zero_V1, zero_var.iloc[[i]]])
del zero_var
#print(zero_V1)
#zero_V1.to_csv ('point_of_period1.csv', sep=';')

V1_per = pd.DataFrame(columns=[data.columns[0], data.columns[1]])
var = np.int_(zero_V1.shape[0]/2)       #просто где-то из середины вытаскиваем период
# https://pythonworld.ru/obrabotka-dannyx/pandas-cookbook-2.html
Num_of_period = 10
V1_per = data[[data.columns[0], data.columns[1], data.columns[2], data.columns[5]]][zero_V1.index[var]:zero_V1.index[var+Num_of_period]+1]
# https://pynative.com/pandas-reset-index/#:~:text=df.drop_duplicates()-,Use%20DataFrame.reset_index()%20function,of%20numbers%20starting%20at%200.
V1_per = V1_per.reset_index(drop=True)
#V1_per.to_csv ('V1_per.csv', sep=';')
del var
#print(V1_per)

var_x = V1_per[V1_per.columns[0]]
T = var_x[var_x.size-1]-var_x[0]
var_yv = V1_per[V1_per.columns[1]]
V1rms=(integrate.trapz((var_yv**2), var_x)/T)**(0.5)
var_yi = V1_per[V1_per.columns[2]]
I1rms=(integrate.trapz((var_yi**2), var_x)/T)**(0.5)
P1rms=(integrate.trapz((var_yv*var_yi), var_x)/T)

print(V1rms)
print(I1rms)
print(P1rms)
print(P1rms/(V1rms*I1rms))