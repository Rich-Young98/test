# -!- coding: utf-8 -!-
import numpy as np
import pandas as pd
import datetime

x = []
y = []
for i in range(1,101):
    x.append(i*0.01)
y = x

file = open('6_rules.csv', 'w+')
for a in x:
    for b in y:
        print(a)
        print(b)
        df = pd.read_csv("original.csv", encoding='gbk')
        df['time'] = pd.to_datetime(df['time'])
        df = df[df['time'] > '2021-06-01']
        df = df[df['time'] < '2021-07-01']
        df = df[::5]
        df.index = range(len(df))

        result = df.values
        levels = [0, 1.779, 1.456, 1.369, 1.205]
        for i in range(0, result.shape[0]):
            result[i][4] = levels[int(result[i][6])] * result[i][5] * 1000000

        for i in range(0, result.shape[0]):
            today = result[i][0]
            start = today.strftime("%Y-%m-%d")
            day = int(str(today).split('-')[2].split(' ')[0])
            if day > 7:
                weekago = (today + datetime.timedelta(days=-7)).strftime("%Y-%m-%d")
                # 前n个自然日所在位置
                keys = df[(df['time'] > weekago) & (df['time'] < start)].index.values
                week = result[(keys[0]):keys[-1], 4]
                threshold = np.max(week, axis=0)
                if (result[i - 2][4] < a * threshold):
                    if (result[i - 1][6] != 1):
                        result[i][6] = result[i - 1][6] - 1
                        result[i][2] = levels[int(result[i][6])]
                        result[i][4] = result[i][2] * result[i][5] * 1000000
                    else:
                        result[i][6] = 1
                        result[i][2] = levels[int(result[i][6])]
                        result[i][4] = result[i][2] * result[i][5] * 1000000

                elif (result[i - 1][4] > b * threshold):
                    if (result[i - 1][6] != 4):
                        result[i][6] = result[i - 1][6] + 1
                        result[i][2] = levels[int(result[i][6])]
                        result[i][4] = result[i][2] * result[i][5] * 1000000
                    else:
                        result[i][6] = 4
                        result[i][2] = levels[int(result[i][6])]
                        result[i][4] = result[i][2] * result[i][5] * 1000000
                else:
                    result[i][6] = result[i - 1][6]
                    result[i][2] = levels[int(result[i][6])]
                    result[i][4] = result[i][2] * result[i][5] * 1000000

        result = result.T
        df = pd.DataFrame(
            {'time': result[0], '推流数': result[1], '码率众数': result[2], 'CDN在线人': result[3], 'bandwith': result[4],
             'Mass在线人数': result[5], 'level': result[6]})
        # df.to_csv('./compare/8_Rule.csv',index=False)
        df['tiyan'] = df['Mass在线人数'] * df['码率众数']
        malv = df['tiyan'].sum()
        renshu = df['Mass在线人数'].sum()
        print(malv / renshu)

        # df['bandwith'] = df['Mass在线人数']*df['码率众数']*1000000
        df = df.sort_values(by="bandwith", ascending=False)
        l = int(df.shape[0] * 0.05)
        top5 = df[l:(l + 1)]['bandwith'].values[0]
        print(top5)
        file.write(str(a)+","+str(b)+","+str(malv / renshu)+","+str(top5)+"\n")
file.close()
