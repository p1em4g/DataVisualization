import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import mySQL_query
from maths_F import approximation
from sensors import sensors
##############################3
experiments = mySQL_query.showDatabases()             # просим список экспериментов, чтобы потом сделать dropdown
##########################33
# data = [[1,2,3],[3,1,2]]
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
            placeholder='Select database',
            options=[
                {'label': x, 'value': x}
                for x in experiments
            ],


        ),


        dcc.Dropdown(                               #dropdown points
            id="point_ID_dropdown",
            placeholder='Select point',
            options=[],
            value=None,
            style={'margin-top':'2%'}
        ),

        dcc.Input(                              #starttime input
            id="startTimeInput",
            placeholder='Start time',
            type='text',
            style = {'width': '97%','margin-top':'2%'}
        ),

        dcc.Input(                          #endtime input
            id="endTimeInput",
            placeholder='End time',
            type='text',
            style = {'width': '97%','margin-top':'2%'}
        ),

        dcc.Dropdown(                                               #sensors dropdown
            id = "graphDropdown",
            placeholder='Select sensor',
            options=[
                {'label': x[1], 'value': x[0]}
                for x in sensors
                # {'label': '1. Temperature (bmp180_temp)', 'value': '1'},  # bmp180_temp - 1
                # {'label': '2. Pressure (bmp180_pressure)', 'value': '2'},  # bmp180_pressure - 2
                # {'label': '3. CO2 (raw_co2)', 'value': '3'},  # raw_co2 - 3
                # {'label': '4. Humidity (si7021_hum)', 'value': '4'},  # si7021_hum - 4
                # {'label': '5. Temperature (si7021_temp)', 'value': '5'},  # si7021_temp - 5
                # {'label': '6. Mass (scales_data)', 'value': '6'},  # scales_data - 6
                # {'label': '7. ds18b20_ab3b (ds18b20_ab3b)', 'value': '7'},  # ds18b20_ab3b - 7
                # {'label': '8. ds18b20_e54f (ds18b20_e54f)', 'value': '8'},  # ds18b20_e54f -8
            ],
            multi=True,
            value=[],
            style={'margin-top':'2%'}
        ),
########################################################################################################approx
        html.Div(children=[
            dcc.Checklist(
                id = "approximateChecklist",
                options=[
                    {'label': 'approximation (kx+b)', 'value': "approxVisible"}
                ],
                value=[]
            ),
            html.Div(children=[
                dcc.Input(                              #approximation starttime input
                    id="approxStartTimeInput",
                    placeholder='Start time (approximation)',
                    type='text',
                    style = {'width': '97%','margin-top':'2%'}
                ),
                dcc.Input(                                                                           # approximation endtime input
                    id="approxEndTimeInput",
                    placeholder='End time (approximation)',
                    type='text',
                    style={'width': '97%', 'margin-top': '2%'}
                ),
                html.Button('Approximation', id ='approxUpdateButton', n_clicks = 0, style = {'width': '100%', 'margin-top':'4%', 'height':'30px'} ),
            ], id = "aproxHiddenDiv", hidden= True)

        ], style = {'background-color': 'white','border':'1px solid gray','border-radius': '2px', 'margin-top':'2%'}),
#############################################################################################################################33

        html.Button('Update', id='updateButton', n_clicks=0, style = {'width': '100%', 'margin-top':'4%', 'height':'30px'}),


##################################################                !!!УДАЛИТЬ!!! (тестовая штука)


#################################################

    ], style={'width': '16%'}),



    html.Div(id = "graphs", style={'width': '83%', 'left':'17%','top':'0%', 'position': 'absolute'}),  # div в который вернуться графики с колбека


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


@app.callback(
    Output("aproxHiddenDiv","hidden"),
    Input("approximateChecklist","value")
)
###########################################33 колбек для меню апроксимации
def showProp(checklistValue):
    if ("approxVisible" in checklistValue):
        return False
    else:
        return True
#########################
@app.callback(                                          # колбек для графиков
    Output('graphs','children'),
    Input("updateButton", "n_clicks"),
    State("graphDropdown", "value"),
    State("startTimeInput", "value"),
    State("endTimeInput", "value"),
    State("approximateChecklist","value")

)
def createGraphs(n_clicks,selectedSensors,startTime,endTime, approxtrue):
    Figures = []
    for sensor in selectedSensors:                                                     #формируем массив из fig (графики по разным сенсорам)
        data = mySQL_query.getSensorData(sensor, startTime, endTime)
        fig = go.Figure(go.Scatter(x = data[0], y = data[1]))
        ##############################################3approx
        if 'approxVisible' in approxtrue:
            fig.add_trace(go.Scatter(x = data[0], y = approximation(data)))
        Figures.append(fig)
        ################################################ approximation
    children = [
        dcc.Graph(                                                                      #строим график и кладем в чилдрен
            figure = Figures[i]
        ) for i in range(0,len(selectedSensors))]                                           #циклим по кл-ву выбранных сенсоров
    return children




try:
    if __name__ == '__main__':
        app.run_server(debug=True)
finally:
    mySQL_query.connectionClose()