import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H2("Input Values for Diagram"),
    
    # 5 input fields
    html.Div([
        html.Div([
            html.Label("Price Threshold"),
            dcc.Input(id='input-1', type='number', placeholder='Enter Threshold'),
        ]),
        html.Div([
            html.Label("Capacity"),
            dcc.Input(id='input-2', type='number', placeholder='Enter Capacity'),
        ]),
        html.Div([
            html.Label("charge power"),
            dcc.Input(id='input-3', type='number', placeholder='Enter Charge Power'),
        ]),
        html.Div([
            html.Label("discharge power"),
            dcc.Input(id='input-4', type='number', placeholder='Enter Discharge Power'),
        ]),
        html.Div([
            html.Label("Start Date"),
            dcc.DatePickerSingle(
                id='date-picker-start',
                date=None,
                placeholder='Select a date'
            ),
        ]),
        html.Div([
            html.Label("End Date"),
            dcc.DatePickerSingle(
                id='date-picker-end',
                date=None,
                placeholder='Select a date'
            ),
        ]),
    ], style={'display': 'flex', 'gap': '20px', 'flexWrap': 'wrap'}),
    
    # Submit button
    html.Button('Show Diagram', id='submit-button', n_clicks=0),
    
    # Output chart
    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='bar-chart-2')
])

# Callback to update the bar chart
@app.callback(
    Output('bar-chart', 'figure'),
    Output('bar-chart-2', 'figure'),
    Input('submit-button', 'n_clicks'),
    State('input-1', 'value'),
    State('input-2', 'value'),
    State('input-3', 'value'),
    State('input-4', 'value')
)
def update_chart(n_clicks, val1, val2, val3, val4):
    if n_clicks == 0:
        return go.Figure()  # Empty chart at start
    
    # Handle None values
    values = [v if v is not None else 0 for v in [val1, val2, val3, val4]]
    labels = [f"Value {i+1}" for i in range(5)]

    fig = go.Figure(data=[
        go.Bar(x=labels, y=values)
    ])
    fig.update_layout(title="Input Values", yaxis_title="Value", xaxis_title="Label")
    return fig, fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8080)
