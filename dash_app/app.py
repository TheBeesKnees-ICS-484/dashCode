# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


# Load in data

# Weighted tolerance index bar chart
WTI_df = pd.read_csv("../preprocessed_bee_data/WTI_clean.csv")
# print(WTI_df.head)

# Neonicotinoid usage data
neonic_df = pd.read_csv("../preprocessed_bee_data/neonic_summary_chart.csv")
neonic_df_normal = pd.read_csv("../preprocessed_bee_data/neonic_summary_chart_normalized.csv")

# Bee colony count data
bee_df = pd.read_csv("../preprocessed_bee_data/bee_summary_chart.csv")
bee_df_normal = pd.read_csv("../preprocessed_bee_data/bee_summary_chart_normalized.csv")

# Combined data (normalized)
bee_neonic_df_normal = bee_df_normal.copy()

bee_neonic_df_normal['Total Neonicotinoid Amount'] = neonic_df_normal['Total Neonicotinoid Amount'].copy()

# Create graphs
WTI_fig = px.bar(WTI_df, x='genus', y='relative WTI', 
title="Weighted Tolerance Index (WTI) compared with co-foraging species of bees")

neonic_fig = px.bar(neonic_df, x='Year', y='Total Neonicotinoid Amount',
title="Neonicotinoid Usage Over Time (1994-2017)")

bee_fig = px.bar(bee_df, x='Year', y='Bee Count',
title="Bee Colony Population Over Time (1994-2017)") 

# Grouped bar chart
bee_neonic_fig = px.bar(bee_neonic_df_normal, x="Year", y=['Total Neonicotinoid Amount', 'Bee Count'], barmode="group",
title="Comparison of Neonicotinoid usage and Bee Populations Over Time (1994-2014)")

bee_neonic_fig.update_layout(xaxis=dict(
        tickmode = 'linear',
        tick0 = 1994,
        dtick = 1,
        tickangle = 45,
        rangeslider=dict(
        visible=True
        )
    )
    )

app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

app.title = "The Effects of Neonicotinoids on Bees"

app.layout = dbc.Container([
        dbc.Row(
            dbc.Col(
                dcc.Graph(figure = WTI_fig),
                width = 12
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(figure = neonic_fig),
                width = 12
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(figure = bee_fig),
                width = 12
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(figure = bee_neonic_fig),
                width = 12
            )
        )
    ], fluid = True)

if __name__ == '__main__':
    app.run_server(debug=True)