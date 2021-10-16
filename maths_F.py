import numpy as np
# import mySQL_query
# import plotly.graph_objects as go


# mySQL_query.databaseConnecting('experiment23')
#
# data = mySQL_query.getSensorData('3', '2021-08-03 23:27:22', '2021-08-03 23:30:22')
# print(data)



def approximation(data):
    y = np.array(data[1])
    startTime = data[0][0]
    x = []
    for i in range(0, len(data[0])):
        x.append((data[0][i] - startTime).total_seconds())
    x = np.array(x)
    approxCoef = np.polyfit(x, y, 1)
    Approx_Y = []
    for x1 in x:
        Approx_Y.append(approxCoef[0]*x1+approxCoef[1])
    return Approx_Y

# y1 = approximation(data)
#
# fig = go.Figure()
# fig.add_trace(go.Scatter(x = data[0], y = data[1]))
# fig.add_trace(go.Scatter(x=data[0], y=y1))
# fig.show()


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