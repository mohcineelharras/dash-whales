import os
import pandas as pd
import streamlit as st
import plotly.graph_objs as go

# Load the data from the CSV files
dataframes = []
for filename in os.listdir('output'):
    if filename.endswith('.csv'):
        df = pd.read_csv(os.path.join('output', filename), sep=';')
        dataframes.append(df)
df = pd.concat(dataframes)

# Set the title and other page configurations
st.title('Token Analysis')
selected_token = st.selectbox('Select Token', df['tokenSymbol'].unique(), index=0)

# Filter the data based on the selected token
filtered_df = df[df['tokenSymbol'] == selected_token]

# Plot the token value over time
st.plotly_chart(
    go.Figure(
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
                title=f'Value ({selected_token})',
            ),
            showlegend=True,
            legend=go.layout.Legend(x=0, y=1.0),
            margin=go.layout.Margin(l=40, r=0, t=40, b=30)
        )
    )
)
