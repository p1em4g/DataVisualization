import dash
from dash import html
from dash import dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import datetime
import maths_F
import mySQL_query
import styles
from maths_F import approximation
from sensors import sensors
##############################3
experiments = mySQL_query.showDatabases()             # просим список экспериментов, чтобы потом сделать dropdown



app = dash.Dash(__name__)

app.layout = html.Div([
########################################################################## меню построения графиков
    html.Div([
        dcc.Dropdown(                                                                   #dropdown из экспериментов
            id="experiments_dropdown",
            placeholder='Select database',
            options=[
                {'label': x, 'value': x}
                for x in experiments
            ],
            style = {**styles.meinMenuElement}

        ),


        dcc.Dropdown(                               #dropdown points
            id="point_ID_dropdown",
            placeholder='Select point',
            options=[],
            value=None,
            style = {**styles.meinMenuElement}


        ),

        dcc.Input(                              #starttime input
            id="startTimeInput",
            placeholder='Start time',
            type='text',
            style ={**styles.meinMenuElement,**styles.meinMenuInput}
        ),

        dcc.Input(                          #endtime input
            id="endTimeInput",
            placeholder='End time',
            type='text',
            style ={**styles.meinMenuElement,**styles.meinMenuInput}

         ),

        html.Button('Update', id='updateButton', n_clicks=0, style = {'width':'250px', 'height':'35px','margin':'4px','margin-top':"8px",'float':'left' } ),

        dcc.Checklist(
                id="approximateChecklist",
                options=[
                    {'label': 'approximation', 'value': "approxVisible"}
                ],
                value=[],
                style = {'margin-top':'15px',}
            ),

        dcc.Dropdown(                                               #sensors dropdown
            id = "graphDropdown",
            placeholder='Select sensor',
            options=[
                {'label': x[1], 'value': x[0]}
                for x in sensors
            ],
            multi=True,
            value=[],
            style = {'width':'99.5%','height':'30px','margin':'4px', 'float':'right'  }

        ),

    ],style = {'height':'100px', "border":"1px solid black"}),

####################################################################### далее меню апроксимации

    html.Div(children = [
        html.Div(children=[

            dcc.Dropdown(
                id = "ApproxFunctDropdown",
                options=[
                    {'label': 'kx+b', 'value': 1},
                    {'label': 'ax^2+bx+c', 'value': 2},
                    {'label': 'ax^3+bx^2+cx+d', 'value': 3}
                ],
                value = None,
                style = styles.approxMenuElement
            ),
            html.Div(children=[
                dcc.Input(  # approximation starttime input
                    id="approxStartTimeInput",
                    placeholder='Start time (approximation)',
                    type='text',
                    style = {**styles.approxMenuElement,**styles.approxMenuInput}

                ),
                dcc.Input(  # approximation endtime input
                    id="approxEndTimeInput",
                    placeholder='End time (approximation)',
                    type='text',
                    style = {**styles.approxMenuElement,**styles.approxMenuInput}

                ),
            ], )
        ])
    ],id="aproxHiddenDiv", hidden=True, style = {"height":'50px',"margin-top":"5px","border":"1px solid black"}),

    html.Div([
        html.Div([
            dcc.RangeSlider(
                id = 'approxRangeSlider',
                min=0,
                max=10,
                step=1,
                value =[0,10]
            )
        ],style = {"margin-top":"7px","margin-left":"30px", 'width':'99.7%'})
    ],id='approxRangeSliderDiv',style = {"height":'20px',"margin-top":"5px","border-bottom":"1px solid black", }),
########################################################################


    html.Div(id = "graphs"),  # div в который вернуться графики с колбека


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

###########################################33 колбек для меню апроксимации
@app.callback(                                  #передает время из слайдера в инпуты для апроксимации

    Output("approxStartTimeInput", 'value'),
    Output("approxEndTimeInput", 'value'),
    Input("approxRangeSlider","value"),
    State("startTimeInput", "value"),
    # State("endTimeInput", "value"),
)

def updAproxTime(sliderValue,strStartTimeInput):
    startTimeInput = maths_F.strToDatetime(strStartTimeInput)
    if startTimeInput != None:
        approxStartTimeInput = startTimeInput+datetime.timedelta(seconds=sliderValue[0])
        approxEndTimeInput = startTimeInput+datetime.timedelta(seconds=sliderValue[1])

    else:
        approxStartTimeInput = "0000-00-00T00:00:00"
        approxEndTimeInput = "0000-00-00T00:00:00"
    return approxStartTimeInput, approxEndTimeInput


@app.callback(                             #передает время из инпутов для времени построения графиеов в слайдер
    Output("approxRangeSlider",'max'),
    Output("approxRangeSlider",'value'),
    Input("startTimeInput","value"),
    Input("endTimeInput","value"),

)
def approxTime(strStartTime,strEndTime):
    startTime = maths_F.strToDatetime(strStartTime)
    endTime = maths_F.strToDatetime(strEndTime)
    if ((endTime != None) and(startTime != None) ):
        rSliderMax = (endTime-startTime).total_seconds()

        approxSliderValue = [0, rSliderMax]
    else:
        rSliderMax = 10
        approxSliderValue = [0, 10]
    return rSliderMax,approxSliderValue


@app.callback(                                         #делает меню апрксимации видимым/скрытым
    Output("aproxHiddenDiv","hidden"),
    Output('approxRangeSliderDiv','hidden'),
    Input("approximateChecklist","value")
)

def showProp(checklistValue):
    if ("approxVisible" in checklistValue):
        return False, False
    else:
        return True,True
#########################
@app.callback(                                          # колбек для графиков
    Output('graphs','children'),
    Input("updateButton", "n_clicks"),
    State("graphDropdown", "value"),
    State("startTimeInput", "value"),
    State("endTimeInput", "value"),
    State("approximateChecklist","value"),
    State("approxStartTimeInput", 'value'),
    State("approxEndTimeInput", 'value'),
    State("ApproxFunctDropdown","value")
)
def createGraphs(n_clicks,selectedSensors,startTime,endTime, approxtrue, approxStartTime,approxEndTime,approxFunct):
    Figures = []
    for sensor in selectedSensors:                                                     #формируем массив из fig (графики по разным сенсорам)
        data = mySQL_query.getSensorData(sensor, startTime, endTime)
        fig = go.Figure(go.Scatter(x = data[0], y = data[1], name = sensors[int(sensor)-1][1]))
        ##############################################3approx
        if ('approxVisible' in approxtrue) and (approxFunct != None):
            approxData = mySQL_query.getSensorData(sensor, approxStartTime, approxEndTime)
            fig.add_trace(go.Scatter(x = approxData[0], y = approximation(approxData,approxFunct), name = 'approximation'))
        fig.update_layout(legend_orientation="h",
                          margin=dict(l=0, r=0, t=0, b=0),
                          xaxis_title='Time',
                          yaxis_title=sensors[int(sensor)-1][1])
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