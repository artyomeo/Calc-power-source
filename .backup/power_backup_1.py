from os import sep
import numpy as np
import pandas as pd
from scipy import integrate as intg

data = pd.read_csv ('Draft1.csv', delimiter=';')

#https://overcoder.net/q/3455/добавить-одну-строку-в-панды-dataframe
#V2_per = pd.DataFrame(columns=[data.columns[0], data.columns[1]])
#V2_per.loc[0] = data.iloc[0]

zero_V1 = pd.DataFrame(columns=data.columns)

#data.shape[0] - получение размерности таблицы данных в виде (x,y), [0] - получение длины, [1] - ширины
for i in range(data.shape[0]):
    if (((data.iloc[i][data.columns[1]] == 0.0) & (data.iloc[i-1][data.columns[1]] < 0.0)) |
        ((data.iloc[i][data.columns[1]] == 0.0) & (i == 0))):
        zero_V1 = pd.concat([zero_V1, data.iloc[[i]]])

        #https://ru.stackoverflow.com/questions/641166/Как-обновить-одну-строку-в-терминале
        #print('Completed: {}%'.format(i*100/data.shape[0]), end='\r')
        print('Completed: %.2f %%' % (i*100/data.shape[0]), end='\r')

print('', end='\n\r')
zero_V1.to_csv ('point_of_period1.csv', sep=';')

V1_per = pd.DataFrame(columns=[data.columns[0], data.columns[1]])

var = np.int_(zero_V1.shape[0]/2)
for i in range(zero_V1.index[var],zero_V1.index[var+1]+1, 1):
    #https://overcoder.net/q/3455/добавить-одну-строку-в-панды-dataframe
    V1_per.loc[var_count] = data.iloc[i]
    var_count = var_count+1
    #https://ru.stackoverflow.com/questions/641166/Как-обновить-одну-строку-в-терминале
    print('Completed: %.2f %%' % (var_count*100/(zero_V1.index[var+1]-zero_V1.index[var])), end='\r')

print(V1_per)
V2_per = data[[data.columns[0], data.columns[1]]][zero_V1.index[var]:zero_V1.index[var+1]+1]
#https://pynative.com/pandas-reset-index/#:~:text=df.drop_duplicates()-,Use%20DataFrame.reset_index()%20function,of%20numbers%20starting%20at%200.
V2_per = V2_per.reset_index(drop=True)
print(V2_per)
#for i in range(zero_A.shape[0]):
#    print(zero_A.iloc[i][zero_A.columns[1]])
#    if (zero_A.loc(i)['V(A,N)']):
#        zero_AA.append(zero_A.loc(i))

#print (zero_AA.shape[0])

#print (np.int_(zero_A.size/8))
#print (zero_A.shape[0])
