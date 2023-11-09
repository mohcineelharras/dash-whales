import os
import pandas as pd
import dash
from dash import dcc,html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Load the data from the CSV files
dataframes = []
for filename in os.listdir('output'):
    if filename.endswith('.csv'):
        df = pd.read_csv(os.path.join('output', filename), sep=';')
        dataframes.append(df)
df = pd.concat(dataframes)


# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the app layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('Token Analysis'),
            dcc.Dropdown(
                id='token-dropdown',
                options=[{'label': i, 'value': i} for i in df['tokenSymbol'].unique()],
                value='MANA'
            ),
            # Add more filters here
        ], width=5),
        dbc.Col([
            dcc.Graph(id='token-graph')
        ], width=7)
    ])
])

# Define the callback to update the graph
@app.callback(
    Output('token-graph', 'figure'),
    [Input('token-dropdown', 'value')]
)
def update_graph(selected_token):
    filtered_df = df[df['tokenSymbol'] == selected_token]
    # filtered_df['timeStamp'] = pd.to_datetime(filtered_df['timeStamp'], unit='s')
    # filtered_df['value'] = filtered_df['value'].astype(float) / 1e18
    figure = go.Figure(
        data=[
            go.Scatter(
                x=filtered_df['timeStamp'],
                y=filtered_df['value'],
                mode='lines',
                name='Value over time'
            )
        ],
        layout=go.Layout(
            title='Token Value Over Time',
            yaxis=dict(
                title='Value ('+selected_token+')',  # Change this to 'Value (USD)' if the values are in USD
            ),
            showlegend=True,
            legend=go.layout.Legend(
                x=0,
                y=1.0
            ),
            margin=go.layout.Margin(l=40, r=0, t=40, b=30)
        )
    )
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
