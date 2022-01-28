import pymysql
import datetime
from userData import host, user, password



connection = pymysql.connect(
    host = host,
    user = user,
    password = password)
print("случилось подключение")
cursor = connection.cursor()


# def query(queryList):
#     cursor = connection.cursor()
#     data = []
#     for x in queryList:
#         cursor.execute(x)
#         if "select" in x or 'show in x':
#             data.append(cursor.fetchall())
#     cursor.close()
#     return data


def showDatabases(): #возвращает список с базами данных, начинающихся как "experiment"
    cursor = connection.cursor()
    cursor.execute("show databases;")
    databases = [item[0] for item in cursor.fetchall()]
    experiments = []
    for i in range(len(databases)-1,-1,-1):
        if "experiment" in databases[i]:
            experiments.append(databases[i])
    cursor.close()
    return experiments

def databaseConnecting(databaseName):           #подключаемся к указанной БД и сразу просим
    cursor = connection.cursor()
    cursor.execute("use {0}".format(databaseName))
    cursor.execute("select count(*) from exp_data;")
    pointsAmount = cursor.fetchall()
    cursor.close()
    points=[]
    for i in range(1,int(pointsAmount[0][0]+1)):
        points.append(i)
    return points

# def databaseConnecting(databaseName):           #подключаемся к указанной БД и сразу просим точки и их время
#     cursor = connection.cursor()
#     cursor.execute("use {0}".format(databaseName))
#     cursor.execute("select point_id, start_time, end_time from exp_data;")
#     pointsAndTime = cursor.fetchall()
#     cursor.close()
#     return pointsAndTime


# def selectData(start_time, end_time):                                   # формирует свой массив за период времени со всеми сенсорами. Данные сортирует по сенсорам
#     Data = [[],[],[],[],[],[],[],[]]
#     cursor.execute("select sensor_id, time, data from raw_data where time > '{0}' and time < '{1}';".format(start_time,end_time))
#     AllData = cursor.fetchall();
#     for i in range(0, len(AllData)-1):
#         Data[(AllData[i][0])-1].append(AllData[i])
#     return Data

def pointStartEnd(point_id : str):                    #возвращает время начала и конца 15-минутного цикла
    cursor= connection.cursor()
    cursor.execute("select start_time from exp_data where point_id = '{0}';".format(point_id))
    # print("select start_time from exp_data where point_id = '{0}';".format(point_id))
    startTime = cursor.fetchall()
    cursor.execute("select end_time from exp_data where point_id = '{0}';".format(point_id))
    # print("select end_time from exp_data where point_id = '{0}';".format(point_id))
    endTime = cursor.fetchall()
    cursor.close()
    return startTime[0][0],endTime[0][0]

def getSensorData(sensor_id : str, startTime, endTime):      #получаем данные за указанный период времени (и само время) с указанного датчика
    cursor = connection.cursor()
    # print("select time, data from raw_data where sensor_id = '{0}' and time > '{1}' and time < '{2}';".format(sensor_id,startTime,endTime))
    cursor.execute("select time, data from raw_data where sensor_id = '{0}' and time > '{1}' and time < '{2}';".format(sensor_id,startTime,endTime))
    time_and_data = cursor.fetchall()
    time = [ item[0] for item in time_and_data]
    sensorData = [ item[1] for item in time_and_data]
    cursor.close()
    return time,sensorData

def connectionClose():
    cursor.close()
    print("курсор всё")
    connection.close()
    print("соединение тоже всё")



# # print(showDatabases())
# #
# a = databaseConnecting("experiment23")
# # print (a)
# #
# # # b = selectData("2021-08-07 03:12:53","2021-08-07 03:15:53")
# # # print(b)
# # # print(b[0][0][2])
# #
# print(getSensorData(3,"2021-08-07 03:12:53", "2021-08-07 03:15:53"))
# #
# # print(pointStartEnd(327))
#
#
# a = query(["show databases;",'use experiment23','select point_id from exp_data'])
# print (a)