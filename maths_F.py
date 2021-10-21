import datetime

import numpy as np
# import mySQL_query
# import plotly.graph_objects as go


# mySQL_query.databaseConnecting('experiment23')
#
# data = mySQL_query.getSensorData('3', '2021-08-03 23:27:22', '2021-08-03 23:30:22')
# print(data)

def strToDatetime(datetimeStr): #переводит строку формата "2021-08-04T04:12:30" в datetime
    try:
        year =''
        for i in range(0,4):
            year = year + datetimeStr[i]

        month =''
        for i in range(5,7):
            month=month+datetimeStr[i]

        day =''
        for i in range(8,10):
            day = day + datetimeStr[i]

        hour =''
        for i in range(11,13):
            hour = hour + datetimeStr[i]

        minute = ""
        for i in range(14,16):
            minute=minute+datetimeStr[i]

        second = ''
        for i in range(17,19):
            second = second + datetimeStr[i]

        DT = datetime.datetime(year = int(year),month = int(month), day = int(day), hour = int(hour), minute = int(minute), second = int(second))
        return DT
    except:
        return None


def approximation(data,polyDegree):#работает при степени полинома <=3
    if data[1] != []:
        y = np.array(data[1])
        startTime = data[0][0]
        x = []
        for i in range(0, len(data[0])):
            x.append((data[0][i] - startTime).total_seconds())
        x = np.array(x)
        approxCoef = np.polyfit(x, y, polyDegree)

        coef_2 = []                           # coef_2 сделан чтобы добавить вначало нули, для случае, когда степень полинома не равна 3. чтобы унифицировать составление Approx_Y
        for i in range(0,(4-len(approxCoef))):
            coef_2.append(0)
        for i in range(0,len(approxCoef)): #добавляем коэффициенты после нулей
            coef_2.append(approxCoef[i])

        Approx_Y = []
        for x1 in x:
            Approx_Y.append(coef_2[0]*(x1**3) + coef_2[1]*(x1**2) + coef_2[2]*x1+coef_2[3])
        return Approx_Y
    else:
        return data[1]


# y1 = approximation(data,1)
# fig = go.Figure()
# fig.add_trace(go.Scatter(x = data[0], y = data[1]))
# fig.add_trace(go.Scatter(x=data[0], y=y1))
# fig.show()
#
#
# mySQL_query.connectionClose()







# x=[]
# # x = np.array([2.863301071014881134e+06,2.460245261639075354e+06,2.093026012088939082e+06,1.760246916946319165e+06,1.459359399934661807e+06,1.186759278075916693e+06,9.379136078178760363e+05,7.075090289232722716e+05,4.896215309857819229e+05,2.779015818236746127e+05,6.577018238002381986e+04,-1.533787985483088996e+05,-3.859754316150106606e+05,-6.380747491954336874e+05,-9.151669400838417932e+05,-1.222001861839911900e+06,-1.562432032544140937e+06,-1.939277663402933627e+06,-2.354219490472638980e+06,-2.807717568478100933e+06,-3.298964879534429871e+06], dtype= float)
# y = np.array([2.863301071014881134e+06,2.460245261639075354e+06,2.093026012088939082e+06,1.760246916946319165e+06,1.459359399934661807e+06,1.186759278075916693e+06,9.379136078178760363e+05,7.075090289232722716e+05,4.896215309857819229e+05,2.779015818236746127e+05,6.577018238002381986e+04,-1.533787985483088996e+05,-3.859754316150106606e+05,-6.380747491954336874e+05,-9.151669400838417932e+05,-1.222001861839911900e+06,-1.562432032544140937e+06,-1.939277663402933627e+06,-2.354219490472638980e+06,-2.807717568478100933e+06,-3.298964879534429871e+06])
# for i in range(0,len(y)):
#     x.append(i)
# x = np.array(x)
# z = np.polyfit(x, y, 1)
# print(z)
# x1 = np.array([1,2,3,4,5,6,7])
# y1 = np.array([5,5,4,3,2,1,2])
#
#
#
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=x, y=y,
#                     # mode='lines',
#                     name='lines'))
# fig.add_trace(go.Scatter(x=x, y=((z[0]*x)+z[1]),
#                     # mode='lines',
#                     name='111111'))
# # fig.update_layout(
# #     xaxis = dict(
# #         tickmode = 'linear',
# #     )
# # )
# fig.show()