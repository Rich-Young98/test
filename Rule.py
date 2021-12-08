# -!- coding: utf-8 -!-
import numpy as np
import pandas as pd
import datetime

df = pd.read_csv("original.csv",encoding='gbk')
df['time'] = pd.to_datetime(df['time'])
df = df[df['time']>'2021-08-01']
df = df[df['time']<'2021-09-01']
df = df[::5]
df.index = range(len(df))

result = df.values
levels = [0,1.779,1.456,1.369,1.205]
for i in range(0,result.shape[0]):
    result[i][4] = levels[int(result[i][6])]*result[i][5]*1000000

for i in range (0,result.shape[0]):
    today = result[i][0]
    start = today.strftime("%Y-%m-%d")
    day = int(str(today).split('-')[2].split(' ')[0])
    if day > 7:
        weekago = (today + datetime.timedelta(days=-7)).strftime("%Y-%m-%d")
        # 前n个自然日所在位置
        keys = df[(df['time'] > weekago) & (df['time'] < start)].index.values
        week = result[(keys[0]):keys[-1], 4]
        threshold = np.max(week, axis=0)
        if (result[i - 2][4] < 0.7 * threshold):
            if (result[i - 1][6] != 1):
                result[i][6] = result[i - 1][6] - 1
                result[i][2] = levels[int(result[i][6])]
                result[i][4] = result[i][2] * result[i][5] * 1000000
            else:
                result[i][6] = 1
                result[i][2] = levels[int(result[i][6])]
                result[i][4] = result[i][2] * result[i][5] * 1000000

        elif (result[i - 1][4] > 0.85 * threshold):
            if (result[i - 1][6] != 4):
                result[i][6] = result[i - 1][6] + 1
                result[i][2] = levels[int(result[i][6])]
                result[i][4] = result[i][2] * result[i][5] * 1000000
            else:
                result[i][6] = 4
                result[i][2] = levels[int(result[i][6])]
                result[i][4] = result[i][2] * result[i][5] * 1000000
        else:
            result[i][6] = result[i-1][6]
            result[i][2] = levels[int(result[i][6])]
            result[i][4] = result[i][2] * result[i][5] * 1000000

result = result.T
df = pd.DataFrame({'time':result[0], '推流数':result[1], '码率众数':result[2] ,'CDN在线人':result[3],'bandwith':result[4],'Mass在线人数':result[5],'level':result[6]})
#df.to_csv('./compare/8_Rule.csv',index=False)
df['tiyan'] = df['Mass在线人数'] * df['码率众数']
df = df.set_index('time').between_time("01:00", "19:00")
malv = df['tiyan'].sum()
renshu = df['Mass在线人数'].sum()
print(malv/renshu)

#df['bandwith'] = df['Mass在线人数']*df['码率众数']*1000000
df = df.sort_values(by="bandwith",ascending=False)
len = int(df.shape[0]*0.05)
top5 = df[len:(len+1)]['bandwith'].values[0]
print(top5)


