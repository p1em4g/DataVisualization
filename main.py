import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import mySQL_query

##############################3
experiments = mySQL_query.showDatabases()             # просим список экспериментов, чтобы потом сделать dropdown
##########################33
# data = [[1,2,3],[1,2,3]]
# experiments = [0, 1, 2]
# points_1 = ["1","11","111"]
# points_2 = ["2","22","222","2222"]
# points_3 = ["3","33"]
# points = [points_1, points_2, points_3]
########################################3

app = dash.Dash(__name__)

app.layout = html.Div([

    html.Div([
        dcc.Dropdown(                                                                   #dropdown из экспериментов
            id="experiments_dropdown",
            options=[
                {'label': x, 'value': x}
                for x in experiments
            ],


        ),


        dcc.Dropdown(                               #dropdown points
            id="point_ID_dropdown",
            options=[],
            value=None,
            style={'margin-top':'2%'}
        ),

        dcc.Input(                              #starttime input
            id="startTimeInput",
            placeholder='start time',
            type='text',
            style = {'width': '97%','margin-top':'2%'}
        ),

        dcc.Input(                          #endtime input
            id="endTimeInput",
            placeholder='end time',
            type='text',
            style = {'width': '97%','margin-top':'2%'}
        ),



        dcc.Dropdown(                                               #sensors dropdown
            id = "graphDropdown",
            options=[
                {'label': '1. Temperature (bmp180_temp)', 'value': '1'},  # bmp180_temp - 1
                {'label': '2. Pressure (bmp180_pressure)', 'value': '2'},  # bmp180_pressure - 2
                {'label': '3. CO2 (raw_co2)', 'value': '3'},  # raw_co2 - 3
                {'label': '4. Humidity (si7021_hum)', 'value': '4'},  # si7021_hum - 4
                {'label': '5. Temperature (si7021_temp)', 'value': '5'},  # si7021_temp - 5
                {'label': '6. Mass (scales_data)', 'value': '6'},  # scales_data - 6
                {'label': '7. ds18b20_ab3b (ds18b20_ab3b)', 'value': '7'},  # ds18b20_ab3b - 7
                {'label': '8. ds18b20_e54f (ds18b20_e54f)', 'value': '8'},  # ds18b20_e54f -8
            ],
            multi=True,
            value=[],
            style={'margin-top':'2%'}
        ),

        html.Button('update', id='updateButton', n_clicks=0, style = {'width': '100%', 'margin-top':'4%', 'height':'30px'}),
    ], style={'width': '16%'}),
                                                                        #далее 8 (по числу сенсоров) "ДИВвов" с графиками.
    html.Div([
        html.Div(id ="divGraph_1", hidden = True ,children = [
            dcc.Graph(
                id="graph1",
            ),
        ]),
        html.Div(id ="divGraph_2", hidden = True, children =[
            dcc.Graph(
                id="graph2",
            )
        ]),
        html.Div(id ="divGraph_3", hidden = True, children =[
            dcc.Graph(
                id="graph3",
            ),
        ]),
        html.Div(id ="divGraph_4", hidden = True, children =[
            dcc.Graph(
                id="graph4",
            ),
        ]),
        html.Div(id ="divGraph_5", hidden = True, children =[
            dcc.Graph(
                id="graph5",
            ),
        ]),
        html.Div(id ="divGraph_6", hidden = True, children =[
            dcc.Graph(
                id="graph6",
            ),
        ]),
        html.Div(id ="divGraph_7", hidden = True, children =[
            dcc.Graph(
                id="graph7",

            ),
        ]),
        html.Div(id ="divGraph_8", hidden = True, children =[
            dcc.Graph(
                id="graph8",
            ),
        ]),
    ], style={'width': '83%', 'left':'17%','top':'0%', 'position': 'absolute'})

],)


@app.callback(                                                  #cаllback которыйый заполняет dropdown с точками по заданной БД (эксперименту)
    Output("point_ID_dropdown","options"),
    Input("experiments_dropdown","value"),
)
def selectPoints(selectedExperiment):
    if (selectedExperiment != None):
        points = mySQL_query.databaseConnecting(selectedExperiment)
        options = [
            {'label': x, 'value': x}
            for x in points
        ]
    else:
        options = []
    return options


@app.callback(                                                    #callback который заполняет поля со временем по выбранной точке из exp_data.
    Output("startTimeInput","value"),
    Output("endTimeInput","value"),
    Input("point_ID_dropdown","value"),
)
def selectPoint(selectedPoint):
    if (selectedPoint != None):
        StartEndTime = mySQL_query.pointStartEnd(selectedPoint)
    else:
        StartEndTime=[None,None]
    return StartEndTime[0],StartEndTime[1]


@app.callback(                                                  #callback отвечающий за отображение "ДИВов" с графиками и заполнение графиков данными.
    Output("divGraph_1","hidden"),
    Output("divGraph_2","hidden"),
    Output("divGraph_3","hidden"),
    Output("divGraph_4","hidden"),
    Output("divGraph_5","hidden"),
    Output("divGraph_6","hidden"),
    Output("divGraph_7","hidden"),
    Output("divGraph_8","hidden"),

    Output("graph1","figure"),
    Output("graph2","figure"),
    Output("graph3","figure"),
    Output("graph4","figure"),
    Output("graph5","figure"),
    Output("graph6","figure"),
    Output("graph7","figure"),
    Output("graph8","figure"),

    Input("updateButton","n_clicks"),
    State("graphDropdown","value"),
    State("startTimeInput","value"),
    State("endTimeInput","value")
)
def showGraph(n_clicks,GraphDropdownValue, startTime, endTime):
    #visibility = [False,False,False,False,False,False,False,False]
    visibility = [True,True,True,True,True,True,True,True]                  # массив отвечающий за отображение графиков. Его элементы по порядку возвращаем соответствующим графикам
    for i in GraphDropdownValue:
        visibility[int(i)-1] = False
    # data = [[1,2,3],[1,2,3]]
    # startTime = "2021-08-04 07:12:53"
    # endTime = "2021-08-04 07:15:53"
    # print("endStartTime: ",startTime," | ",endTime)
    if (visibility[0] == False):                                            #если график отображается, то можно и данные запросить. Далее делаем проверку по каждому графику
        data = mySQL_query.getSensorData("1", startTime, endTime)
        # print ("data: ", data)
        figure1 = dict(
            data=[
                dict(
                    x=data[0],
                    y=data[1],
                )
            ],
            layout = {'title':'1. Temperature (bmp180_temp)'}
        )
    else:
        figure1 = dict(
            data=[
            ]
        )

    if (visibility[1] == False):
        data = mySQL_query.getSensorData("2", startTime, endTime)
        figure2 = dict(
            data=[
                dict(
                    x=data[0],
                    y=data[1]
                )
            ],
            layout = {'title':'2. Pressure (bmp180_pressure)'}
        )
    else:
        figure2 = dict(
            data=[ ]
        )

    if (visibility[2] == False):
        data = mySQL_query.getSensorData("3", startTime, endTime)
        figure3 = dict(
            data=[
                dict(
                    x=data[0],
                    y=data[1]
                )
            ],
            layout={'title': '3. CO2 (raw_co2)'}
        )
    else:
        figure3 = dict(
            data=[]
         )

    if (visibility[3] == False):
        data = mySQL_query.getSensorData("4", startTime, endTime)
        figure4 = dict(
            data=[
                dict(
                    x=data[0],
                    y=data[1]
                )
            ],
            layout={'title': '4. Humidity (si7021_hum)'}
        )
    else:
        figure4 = dict(
            data=[
                ]
        )

    if (visibility[4] == False):
        data = mySQL_query.getSensorData("5", startTime, endTime)
        figure5= dict(
            data=[
                dict(
                    x=data[0],
                    y=data[1]
                )
            ],
            layout={'title': '5. Temperature (si7021_temp)'}
        )
    else:
        figure5= dict(
            data=[
            ]
        )

    if (visibility[5] == False):
        data = mySQL_query.getSensorData("6", startTime, endTime)
        figure6 = dict(
            data=[
                dict(
                    x=data[0],
                    y=data[1]
                )
            ],
            layout={'title': '6. Mass (scales_data)'}
        )
    else:
        figure6 = dict(
            data=[
                ]
            )

    if (visibility[6] == False):
        data = mySQL_query.getSensorData("7", startTime, endTime)
        figure7 = dict(
            data=[
                dict(
                    x=data[0],
                    y=data[1]
                )
            ],
            layout={'title': '7. ds18b20_ab3b (ds18b20_ab3b)'}
        )
    else:
        figure7 = dict(
            data=[]
            )

    if (visibility[7] == False):
        data = mySQL_query.getSensorData("8", startTime, endTime)
        figure8 = dict(
            data=[
                dict(
                    x=data[0],
                    y=data[1]
                )
            ],
            layout={'title': '8. ds18b20_e54f (ds18b20_e54f)'}
        )
    else:
        figure8= dict(
            data=[]
        )

    return visibility[0], visibility[1],visibility[2],visibility[3],visibility[4],visibility[5],visibility[6],visibility[7],\
           figure1,figure2,figure3,figure4,figure5,figure6,figure7,figure8



try:
    if __name__ == '__main__':
        app.run_server(debug=True)
finally:
    mySQL_query.connectionClose()