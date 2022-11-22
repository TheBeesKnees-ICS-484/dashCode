# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Contains the charts used for the visualization

# Load in data

# Weighted tolerance index bar chart
WTI_df = pd.read_csv("../preprocessed_bee_data/WTI_clean.csv")
# print(WTI_df.head)

# Neonicotinoid usage data
neonic_df = pd.read_csv("../preprocessed_bee_data/neonic_summary_chart.csv")
neonic_df_normal = pd.read_csv("../preprocessed_bee_data/neonic_summary_chart_normalized.csv")

# Bee colony count data

# State Level
bee_state_df = pd.read_csv("../preprocessed_bee_data/bee_colony_data/state_level/bee_state_summary_chart.csv")
bee_state_df_normal = pd.read_csv("../preprocessed_bee_data/bee_colony_data/state_level/bee_state_summary_chart_normalized.csv")
# County Level
bee_county_df = pd.read_csv("../preprocessed_bee_data/bee_colony_data/county_level/bee_county_summary_chart.csv")
bee_county_df_normal = pd.read_csv("../preprocessed_bee_data/bee_colony_data/county_level/bee_county_summary_chart_normalized.csv")


# Combined data (normalized)
bee_state_neonic_df = bee_state_df.copy()
bee_state_neonic_df_normal = bee_state_df_normal.copy()

bee_state_neonic_df['Total Neonicotinoid Amount'] = neonic_df['Total Neonicotinoid Amount'].copy()
bee_state_neonic_df_normal['Total Neonicotinoid Amount'] = neonic_df_normal['Total Neonicotinoid Amount'].copy()

bee_county_neonic_df = bee_county_df.copy()
bee_county_neonic_df_normal = bee_county_df_normal.copy()

bee_county_neonic_df['Total Neonicotinoid Amount'] = neonic_df['Total Neonicotinoid Amount'].copy()
bee_county_neonic_df_normal['Total Neonicotinoid Amount'] = neonic_df_normal['Total Neonicotinoid Amount'].copy()

# Create graphs
WTI_fig = px.bar(WTI_df, x='genus', y='relative WTI', 
title="Weighted Tolerance Index (WTI) compared with co-foraging species of bees")

# neonic_state_fig = px.bar(neonic_df, x='Year', y='Total Neonicotinoid Amount',
# title="State Level: Neonicotinoid Usage Over Time (1994-2017)")
# neonic_state_fig.update_layout(xaxis=dict(
#         tickmode = 'linear',
#         tick0 = 1994,
#         dtick = 1,
#         tickangle = 45,
#         rangeslider=dict(
#         visible=True
#         )
#     )
#     )

# neonic_county_fig = px.bar(neonic_df[neonic_df['Year'].isin([2002, 2007, 2012])], x='Year', y='Total Neonicotinoid Amount',
# title="County Level: Neonicotinoid Usage Over Time (1994-2017)")
# neonic_county_fig.update_layout(xaxis=dict(
#         tickmode = 'array',
#         tickvals = [2002, 2007, 2012],
#         tickangle = 45,
#         rangeslider=dict(
#         visible=True
#         )
#     )
#     )    

# bee_state_fig = px.bar(bee_state_df, x='Year', y='Bee Count',
# title="State Level: Bee Colony Population Over Time (1994-2017)") 
# bee_state_fig.update_layout(xaxis=dict(
#         tickmode = 'linear',
#         tick0 = 1994,
#         dtick = 1,
#         tickangle = 45,
#         rangeslider=dict(
#         visible=True
#         )
#     )
#     )

# bee_county_fig = px.bar(bee_county_df, x='Year', y='Bee Count',
# title="County Level: Bee Colony Population Over Time (1994-2017)") 
# bee_county_fig.update_layout(xaxis=dict(
#         tickmode = 'array',
#         tickvals = [2002, 2007, 2012],
#         tickangle = 45,
#         rangeslider=dict(
#         visible=True
#         )
#     )
#     )    

# Grouped bar charts
# State bee data neonic fig
bee_state_neonic_fig = px.bar(bee_state_neonic_df, x="Year", y=['Total Neonicotinoid Amount', 'Bee Count'], barmode="group",
title="State Level: Comparison of Neonicotinoid usage and Bee Populations Over Time (1994-2014)")

bee_state_neonic_fig.update_layout(xaxis=dict(
        tickmode = 'linear',
        tick0 = 1994,
        dtick = 1,
        tickangle = 45,
        rangeslider=dict(
        visible=True
        )
    )
    )

# State bee data neonic fig normalized
bee_state_neonic_fig_normal = px.bar(bee_state_neonic_df_normal, x="Year", y=['Total Neonicotinoid Amount', 'Bee Count'], barmode="group",
title="State Level: Normalized comparison of Neonicotinoid usage and Bee Populations Over Time (1994-2014)")

bee_state_neonic_fig_normal.update_layout(xaxis=dict(
        tickmode = 'linear',
        tick0 = 1994,
        dtick = 1,
        tickangle = 45,
        rangeslider=dict(
        visible=True
        )
    )
    )

# County bee data neonic fig
bee_county_neonic_fig = px.bar(bee_county_neonic_df[bee_county_neonic_df['Year'].isin([2002, 2007, 2012])], 
x="Year", y=['Total Neonicotinoid Amount', 'Bee Count'], barmode="group",
title="County Level: Comparison of Neonicotinoid usage and Bee Populations Over Time (1994-2014)")

bee_county_neonic_fig.update_layout(xaxis=dict(
        tickmode = 'array',
        tickvals = [2002, 2007, 2012],
        tickangle = 45,
        rangeslider=dict(
        visible=True
        )
    )
    )   

# County bee data neonic fig normalized
bee_county_neonic_fig_normal = px.bar(bee_county_neonic_df_normal[bee_county_neonic_df_normal['Year'].isin([2002, 2007, 2012])], 
x="Year", y=['Total Neonicotinoid Amount', 'Bee Count'], barmode="group",
title="County Level: Normalized comparison of Neonicotinoid usage and Bee Populations Over Time (1994-2014)")

bee_county_neonic_fig_normal.update_layout(xaxis=dict(
        tickmode = 'array',
        tickvals = [2002, 2007, 2012],
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
            dbc.Col([
                dcc.RadioItems(
                    id='selection_state',
                    options=["Regular_s", "Normalized_s"],
                    value='Regular_s',
                ),
                dcc.Loading(dcc.Graph(id="state_graph"), type="cube")],
                width = 12
            )
        ),
        dbc.Row(
            dbc.Col([
                dcc.RadioItems(
                    id='selection_county',
                    options=["Regular_c", "Normalized_c"],
                    value='Regular_c',
                ),
                dcc.Loading(dcc.Graph(id="county_graph"), type="cube")],
                width = 12
            )
        )
        # dbc.Row(
        #     dbc.Col(
        #         dcc.Graph(figure = bee_state_neonic_fig),
        #         width = 12
        #     )
        # ),
        # dbc.Row(
        #     dbc.Col(
        #         dcc.Graph(figure = bee_state_neonic_fig_normal),
        #         width = 12
        #     )
        # ),
        # dbc.Row(
        #     dbc.Col(
        #         dcc.Graph(figure = bee_county_neonic_fig),
        #         width = 12
        #     )
        # ),
        # dbc.Row(
        #     dbc.Col(
        #         dcc.Graph(figure = bee_county_neonic_fig_normal),
        #         width = 12
        #     )
        # )
    ], fluid = True)

@app.callback(
Output("state_graph", "figure"), 
Output("county_graph", "figure"), 
Input("selection_state", "value"),
Input("selection_county", "value"))

def display_animated_graph(selection1, selection2):
    animations = {}

    if (selection1 == "Regular_s"):
        animations['selection1'] = bee_state_neonic_fig
    else:
        animations['selection1'] = bee_state_neonic_fig_normal
    if (selection2 == "Regular_c"):
        animations['selection2'] = bee_county_neonic_fig
    else:
        animations['selection2'] = bee_county_neonic_fig_normal
    return animations["selection1"], animations["selection2"]

if __name__ == '__main__':
    app.run_server(debug=True)