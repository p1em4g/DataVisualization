
from dash import html
from dash import dcc
import mySQL_query
import styles
from sensors import sensors
##############################3
experiments = mySQL_query.showDatabases()             # просим список экспериментов, чтобы потом сделать dropdown


graph_tab = html.Div([
########################################################################## меню построения графиков
    html.Div([

        dcc.Dropdown(                                   #dropdown из экспериментов
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






# try:
#     if __name__ == '__main__':
#         app.run_server(debug=True)
# finally:
#     mySQL_query.connectionClose()