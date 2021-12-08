# -!- coding: utf-8 -!-
import pandas as pd
import numpy as np
import datetime

if __name__ == "__main__":
    df = pd.read_csv("original.csv", encoding='gbk')
    df['time'] = pd.to_datetime(df['time'])
    df = df[df['time'] > '2021-06-01']
    df = df[df['time'] < '2021-07-01']
    df = df[::5]
    df.index = range(len(df))
    result = df.values
    levels = [0, 1.779, 1.456, 1.369, 1.205]
    for i in range(0, result.shape[0]):
        result[i][2] = levels[int(result[i][6])]
        result[i][4] = levels[int(result[i][6])] * result[i][5] * 1000000

    for i in range(0, result.shape[0]-2):
        today = result[i][0]
        start = today.strftime("%Y-%m-%d")
        day = int(str(today).split('-')[2].split(' ')[0])
        if day>7:
            ago = (today + datetime.timedelta(days=-(day - 1))).strftime("%Y-%m-%d")
            # 前面所有自然日的九五峰值
            keys = df[(df['time'] > ago) & (df['time'] < start)].index.values
            week = result[(keys[0]):keys[-1], 4]
            week = np.sort(week)
            l = int(len(keys) * 0.95)
            threshold = week[l:(l+1)]

            levelbefore = result[i-1][6]
            codebefore = levels[int(levelbefore)]

            if (result[i+2][5]*codebefore*1000000 < 0.7 * threshold):
                if (levelbefore != 1):
                    result[i][6] = levelbefore - 1
                else:
                    result[i][6] ==1
                result[i][2] = levels[int(result[i][6])]
                result[i][4] = result[i][2] * result[i][5] * 1000000

            elif (result[i+1][5]*codebefore*1000000 > 0.85 * threshold):
                if (levelbefore != 4):
                    result[i][6] = levelbefore + 1
                else:
                    result[i][6] = 4
                result[i][2] = levels[int(result[i][6])]
                result[i][4] = result[i][2] * result[i][5] * 1000000
            else:
                result[i][6] = levelbefore
                result[i][2] = levels[int(result[i][6])]
                result[i][4] = result[i][2] * result[i][5] * 1000000

    result = result.T
    df = pd.DataFrame(
        {'time': result[0], '推流数': result[1], '码率众数': result[2], 'CDN在线人': result[3], 'bandwith': result[4],
         'Mass在线人数': result[5], 'level': result[6]})
    df['tiyan'] = df['Mass在线人数'] * df['码率众数']
    malv = df['tiyan'].sum()
    renshu = df['Mass在线人数'].sum()
    print(malv / renshu)

    #df['bandwith'] = df['Mass在线人数'] * df['码率众数'] * 1000000
    df = df.sort_values(by="bandwith", ascending=False)
    len = int(df.shape[0] * 0.05)
    top5 = df[len:(len + 1)]['bandwith'].values[0]
    print(top5)


