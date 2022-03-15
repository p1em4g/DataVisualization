import dash_bootstrap_components as dbc
from dash import html
from dash import dcc

from config import address_and_nodes



cont_tab = html.Div([
    html.Div(children = [

        dbc.Row([
            dbc.Col(html.Div([
                dbc.InputGroup([dbc.InputGroupText("ip"), dbc.Input(id = "connect_input",placeholder="address")])
            ]),width=3),
            dbc.Col(html.Div([dbc.Button("CONNECT",id = 'connect_button', color="success", className="me-1")]),width=1),
            dbc.Col(html.Div([dbc.Button("DISCONNECT", color="danger", className="me-1")]), width=1),
            dbc.Col(html.Div([dbc.Textarea(className="mb-3", placeholder="A Textarea",disabled = True),]))
            ]),

    ],style = {"border-bottom":"1px solid black"}),

    html.Div(children = [
        dbc.Row([
            dbc.Col(html.Div([
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Address"),
                        dbc.Select(
                            id = 'address_dropdown',
                            options=[
                                {"label": x, "value": x} for x in address_and_nodes
                            ]
                        ),
                    ]
                ),
            ]),width=2),

            dbc.Col(html.Div([
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Node"),
                        dbc.Select(
                            id = "node_dropdown",
                            # options=[{"label": "Option 1", "value": 1},{"label": "Option 2", "value": 2},]
                        ),
                    ]
                ),
            ]),width=2),

            dbc.Col(html.Div([
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Device"),
                        dbc.Select(
                            id = 'device_dropdown',

                        ),

                    ]
                ),
            ]),width=2),

            dbc.Col(html.Div([
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Command"),
                        dbc.Select(
                            id = 'command_dropdown',

                        ),

                    ]
                ),
            ]),width=2),

            dbc.Col(html.Div([dbc.InputGroup([dbc.InputGroupText("Arguments"), dbc.Input(id = 'command_arguments_input',placeholder="")])])),
            dbc.Col(html.Div([dbc.Button("SEND",id = 'send_button', color="primary", className="me-1")]),width=1),

        ])
    ],style = {"border-bottom":"1px solid black"}),

    html.Div(children=[
        dcc.Textarea(
            id='output_textarea',
            value='Textarea',
            style={'width': '100%', 'height': 500},
        ),
    ],style = {"margin-top":"1%"}),
])