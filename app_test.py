import time

import dash
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objs as go
from dash import Input, Output, dcc, html

import plotly.express as px
import pandas as pd
import pathlib
from urllib.request import urlopen
import json

app = dash.Dash(external_stylesheets=[dbc.themes.SUPERHERO])


############# Maps ################

filepath = str(pathlib.Path(__file__).parent.resolve())

df1 = pd.read_csv("Plotly Tests/State level map/data/bee_colony_survey_data_by_state.csv")
df1=df1[['year','period','week_ending','state','state_ansi', 'watershed', 'data_item', 'value']]
us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))
#for state in df.state:
count = 0
for i in df1.state:
    for j in abbrev_to_us_state:
        if abbrev_to_us_state[j].lower()==i.lower():
            df1.loc[count,"state"] = j
    count=count+1

df1.rename({'value':'Beez'},axis=1, inplace=True)
df1=df1.sort_values("year") # Make sure you sort the time horizon column in ascending order because this column is in random order in the raw dataset

fig1 = px.choropleth(df1,
                    locations='state', 
                    locationmode="USA-states", 
                    color='Beez',
                    color_continuous_scale="Viridis_r", 
                    scope="usa",
                    range_color=(0,169000),
                    animation_frame='year') #make sure 'period_begin' is string type and sorted in ascending order

fig1.update_layout(transition = {'duration': 9000})
fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

df2 = pd.read_csv("Plotly Tests/County Level map/data/bee_colony_census_data_by_county.csv")
#df=df[['year','period','state','state_ansi', 'ag_district_code', 'county', 'county_ansi', 'value']]

stateAnsi = []

count_State = 0
for i in df2.state_ansi:
    df2.loc[count_State,"state_ansi"] = str(i).zfill(2)
    stateAnsi.append(str(str(i).zfill(2)))
    count_State=count_State+1

count_County = 0
for i in df2.county_ansi:
    df2.loc[count_County,"county_ansi"] = str(stateAnsi[count_County])+str(i).zfill(3)
    count_County=count_County+1

#print(df.county_ansi)
#print(counties)

df2=df2.sort_values("year") # Make sure you sort the time horizon column in ascending order because this column is in random order in the raw dataset

fig2 = px.choropleth(df2, geojson=counties, locations='county_ansi', color='value',
                           color_continuous_scale="Viridis",
                           #mapbox_style="carto-positron",
                           #range_color=(0, 129731),
                           scope="usa",
                           #zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           #opacity=0.5,
                           labels={'value':'Beez'},
                          animation_frame='year')
fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


#############################

############ Bar Chart Summary ##########

# Load in data

# Weighted tolerance index bar chart
WTI_df = pd.read_csv("preprocessed_bee_data/WTI_clean.csv")
# print(WTI_df.head)

# Neonicotinoid usage data
neonic_df = pd.read_csv("preprocessed_bee_data/neonic_summary_chart.csv")
neonic_df_normal = pd.read_csv("preprocessed_bee_data/neonic_summary_chart_normalized.csv")

# Bee colony count data
bee_df = pd.read_csv("preprocessed_bee_data/bee_summary_chart.csv")
bee_df_normal = pd.read_csv("preprocessed_bee_data/bee_summary_chart_normalized.csv")

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

#########################################

@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"), Input("store", "data")],
)
def render_tab_content(active_tab, data):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab and data is not None:
        if active_tab == "scatter":
            return dcc.Graph(figure=data["scatter"])
        elif active_tab == "histogram":
            return dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=data["hist_1"]), width=6),
                    dbc.Col(dcc.Graph(figure=data["hist_2"]), width=6),
                ]
            )
    return "No tab selected"


@app.callback(Output("store", "data"), [Input("button", "n_clicks")])
def generate_graphs(n):
    """
    This callback generates three simple graphs from random data.
    """
    if not n:
        # generate empty graphs when app loads
        return {k: go.Figure(data=[]) for k in ["scatter", "hist_1", "hist_2"]}

    # simulate expensive graph generation process
    time.sleep(2)

    # generate 100 multivariate normal samples
    data = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], 100)

    scatter = go.Figure(
        data=[go.Scatter(x=data[:, 0], y=data[:, 1], mode="markers")]
    )
    hist_1 = go.Figure(data=[go.Histogram(x=data[:, 0])])
    hist_2 = go.Figure(data=[go.Histogram(x=data[:, 1])])

    # save figures in a dictionary for sending to the dcc.Store
    return {"scatter": scatter, "hist_1": hist_1, "hist_2": hist_2}

###########################

app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("Bees Knees"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=fig1,)),
                dbc.Col(dcc.Graph(figure=fig2,)),
            ]
        ),

        dbc.Row(
            dbc.Col(
                dcc.Graph(figure = bee_neonic_fig),
                width = 12
            )
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)


