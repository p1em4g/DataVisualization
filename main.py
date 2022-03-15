import dash
from dash import html
from dash import dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import datetime
import maths_F
import mySQL_query
from maths_F import approximation
from sensors import sensors

import dash_bootstrap_components as dbc

from config import address_and_nodes, list_of_nodes
from graph_tab import  graph_tab
from cont_tab import cont_tab

from plexus.utils.console_client_api import PlexusUserApi
from plexus.nodes.message import Message

from stend_control_command_creator import StendControlCommandCreator



###############################


# stend_control = None
# addr_decoded_ = None
# decoded_resp_ = None

list_of_nodes1 = [
        {"name": "node2", "address": "tcp://10.9.0.12:5567"}
        ]
client_addr = "tcp://10.9.0.7:5555"         # мой адресс
# stend_control = PlexusUserApi(endpoint=client_addr, name="client2223", list_of_nodes=list_of_nodes1)
# message = Message(addr="node2", device ='node2', command='info')
# addr_decoded_, decoded_resp_ = Message.parse_zmq_msg(stend_control.send_msg(message))

sccc = StendControlCommandCreator(client_addr, list_of_nodes1, "node2")
#############################

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Tabs([
        dbc.Tab(graph_tab, label='Graph'),
        dbc.Tab(cont_tab, label='ControlPanel')
    ])
])



# Graph Page Callbacks 11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
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
#######################################################################3

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
        #############################################approx
        if ('approxVisible' in approxtrue) and (approxFunct != None):
            approxData = mySQL_query.getSensorData(sensor, approxStartTime, approxEndTime)
            fig.add_trace(go.Scatter(x = approxData[0], y = approximation(approxData,approxFunct), name = 'approximation'))
        fig.update_layout(legend_orientation="h",
                          margin=dict(l=0, r=0, t=0, b=0),
                          xaxis_title='Time',
                          yaxis_title=sensors[int(sensor)-1][1])
        Figures.append(fig)
        ############################################# approximation
    children = [
        dcc.Graph(                                                                      #строим график и кладем в чилдрен
            figure = Figures[i]
        ) for i in range(0,len(selectedSensors))]                                           #циклим по кл-ву выбранных сенсоров
    return children

# # Control Page 2222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222
# @app.callback(
#     Input("connect_button", "n_clicks"),
#     State("connect_input","value")
# )
# def create_stend_control(client_addr):
#     client_name = "client{0}".format(client_addr)
#     stend_control = PlexusUserApi(endpoint=client_addr, name=client_name, list_of_nodes=list_of_nodes)
#     message = Message(addr="node2", device ='node2', command='info')
#     addr_decoded_, decoded_resp_ = Message.parse_zmq_msg(stend_control.send_msg(message))

@app.callback(
    Output("node_dropdown",'options'),
    Input('address_dropdown', "value")
)
def get_nodes(address):
    if address != None:
        options = [
            {"label": x, "value": x} for x in address_and_nodes[address]
        ]
        return options

@app.callback(
    Output('device_dropdown','options'),
    Input("connect_button", "n_clicks"),
)
def get_device(n_clicks):
    options = [
        {'label': x, 'value': x} for x in sccc.get_devices_names()
    ]
    return options


@app.callback(
    Output('command_dropdown','options'),
    Input("device_dropdown", "value"),
)
def get_commands(device_dropdown_value):
    if device_dropdown_value != None:
        options = [
            {'label': x, 'value': x} for x in sccc.get_commands(device_dropdown_value)
        ]
        return options

@app.callback(
    Output('command_arguments_input','value'),
    Input("command_dropdown", "value"),
    State("device_dropdown", "value"),
)
def get_device(command,device_dropdown_value, ):
    if device_dropdown_value != None and command != None:
        return sccc.get_arguments_str(device_dropdown_value, command)

@app.callback(
    Output('output_textarea','value'),
    Input("send_button", "n_clicks"),
    State('device_dropdown','value'),
    State("command_dropdown", "value"),
    State('command_arguments_input', "value")
)
def send_message(n_clicks, device, command, arguments: str):
    return sccc.send_message(device, command, arguments)


if __name__ == '__main__':
    try:
        if __name__ == '__main__':
            app.run_server(debug=False)
    finally:
        mySQL_query.connectionClose()
