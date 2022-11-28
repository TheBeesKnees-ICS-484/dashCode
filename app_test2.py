import time

import dash
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objs as go
from dash import Input, Output, dcc, html, State, ctx

import plotly.express as px
import pandas as pd
import pathlib
from urllib.request import urlopen
import json

import base64

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

df1.rename({'value':'Bee Population'},axis=1, inplace=True)
df1=df1.sort_values("year") # Make sure you sort the time horizon column in ascending order because this column is in random order in the raw dataset

fig1 = px.choropleth(df1,
                    locations='state', 
                    locationmode="USA-states", 
                    color='Bee Population',
                    color_continuous_scale="Viridis_r", 
                    scope="usa",
                    range_color=(0,169000),
                    animation_frame='year') #make sure 'period_begin' is string type and sorted in

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

df2 = pd.read_csv("Plotly Tests/County Level map/data/bee_colony_census_data_by_county_clean.csv")
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

title_text2 ='Bee data by County'

fig2 = px.choropleth(df2, geojson=counties, locations='county_ansi', color='value',
                           color_continuous_scale="Viridis_r",
                           #mapbox_style="carto-positron",
                           #range_color=(0, 129731),
                           scope="usa",
                           #zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           #opacity=0.5,
                           title = title_text2,
                           labels={'value':'Bee Population'},
                          animation_frame='year')
#fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


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

# State Level
bee_state_df = pd.read_csv("preprocessed_bee_data/bee_colony_data/state_level/bee_state_summary_chart.csv")
bee_state_df_normal = pd.read_csv("preprocessed_bee_data/bee_colony_data/state_level/bee_state_summary_chart_normalized.csv")
# County Level
bee_county_df = pd.read_csv("preprocessed_bee_data/bee_colony_data/county_level/bee_county_summary_chart.csv")
bee_county_df_normal = pd.read_csv("preprocessed_bee_data/bee_colony_data/county_level/bee_county_summary_chart_normalized.csv")


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

# Grouped bar charts
# State bee data neonic fig
bee_state_neonic_fig = px.bar(bee_state_neonic_df, x="Year", y=['Total Neonicotinoid Amount', 'Bee Count'], barmode="group",
title="State Level: Comparison of Neonicotinoid usage<br>and Bee Populations Over Time (1994-2017)",
color_discrete_sequence=['rgb(35, 87, 137)', 'rgb(241, 211, 2)'])

bee_state_neonic_fig.update_layout(xaxis=dict(
        tickmode = 'linear',
        tick0 = 1994,
        dtick = 1,
        tickangle = 45,
        # rangeslider=dict(
        # visible=True
        # )
    )
    )

# State bee data neonic fig normalized
bee_state_neonic_fig_normal = px.bar(bee_state_neonic_df_normal, x="Year", y=['Total Neonicotinoid Amount', 'Bee Count'], barmode="group",
title="State Level: Normalized comparison of Neonicotinoid usage<br>and Bee Populations Over Time (1994-2017)",
color_discrete_sequence=['rgb(35, 87, 137)', 'rgb(241, 211, 2)'])

bee_state_neonic_fig_normal.update_layout(xaxis=dict(
        tickmode = 'linear',
        tick0 = 1994,
        dtick = 1,
        tickangle = 45,
        # rangeslider=dict(
        # visible=True
        # )
    )
    )

# County bee data neonic fig
bee_county_neonic_fig = px.bar(bee_county_neonic_df[bee_county_neonic_df['Year'].isin([2002, 2007, 2012])], 
x="Year", y=['Total Neonicotinoid Amount', 'Bee Count'], barmode="group",
title="County Level: Comparison of Neonicotinoid usage<br>and Bee Populations Over Time (1994-2017)",
color_discrete_sequence=['rgb(35, 87, 137)', 'rgb(241, 211, 2)'])

bee_county_neonic_fig.update_layout(xaxis=dict(
        tickmode = 'array',
        tickvals = [2002, 2007, 2012],
        tickangle = 90,
        # rangeslider=dict(
        # visible=True
        # )
    )
    )   

# County bee data neonic fig normalized
bee_county_neonic_fig_normal = px.bar(bee_county_neonic_df_normal[bee_county_neonic_df_normal['Year'].isin([2002, 2007, 2012])], 
x="Year", y=['Total Neonicotinoid Amount', 'Bee Count'], barmode="group",
title="County Level: Normalized comparison of Neonicotinoid usage<br>and Bee Populations Over Time (1994-2017)",
color_discrete_sequence=['rgb(35, 87, 137)', 'rgb(241, 211, 2)'])

bee_county_neonic_fig_normal.update_layout(xaxis=dict(
        tickmode = 'array',
        tickvals = [2002, 2007, 2012],
        tickangle = 90,
        # rangeslider=dict(
        # visible=True
        # )
    )
    ) 

#########################################

###########################

image_filename = 'intro_material/honeybee.jpeg' 
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("Bees Knees"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    html.Img(
                        src='data:image/png;base64,{}'.format(encoded_image.decode()), 
                        alt='honeybee',
                        width=700,
                        height=350,
                        className="center",
                    ),
                    width=6, 
                ),
                dbc.Col(
                    dbc.Alert(
                        [
                            html.H4("Pesticides and the Neonicotinoid Crisis", className="alert-heading", style={"text-decoration": "underline"},),
                            html.P(
                                "Pesticides called neonicotinoids (neonics), which have been embraced in recent decades by many commercial farms across the U.S, have led to mass deaths of pollinators. It is one of the major factors that has put one in four of North America’s 4,000 bee species at risk of extinction."
                            ),
                            html.Br(),
                            html.P(
                                "Their loss is our loss, and that’s not an overstatement. One hundred percent of almonds, for example, are pollinated by bees, while 90 percent of apples, blueberries, and avocados are also the fruits of bees’ labor. If bees are taken out of the agricultural system, the cost of fruits and vegetables could multiply tenfold, pricing out vulnerable communities from any access to crucial sources of nutrition."
                            ),
                            html.Hr(),
                            html.P(
                                    "Excerpt from:",
                                    className="mb-0",
                                ),
                            html.A("the Bee Conservancy", href="#", className="alert-link"),
                        ],
                        color="success",
                    ),
                    width=6,
                )
            ],
        ),
        dbc.Row(
            [
                dbc.Col(

                    width=6,
                ),
                dbc.Col(
                    dcc.Graph(figure=WTI_fig),
                    width=6,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col([
                    dcc.Interval(id="animate", disabled=True),
                    dcc.Graph(id="graph-with-slider")],#dcc.Graph(figure=fig1,),
                    width = 6
            ),
                dbc.Col([
                    dcc.Interval(id="animate2", disabled=True),
                    dcc.Graph(id="graph-with-slider2")],#dcc.Graph(figure=fig2,),
                    width = 6
                ),
            ]
        ),

        dbc.Row(
            [
            dbc.Col([
                dcc.RadioItems(
                    id='selection_state',
                    options={"Regular_s": "Regular", "Normalized_s": "Normalized"},
                    value='Regular_s'
                ),
                dcc.Loading(dcc.Graph(id="state_graph"), type="cube")],
                width = 6
            ),
            dbc.Col([
                dcc.RadioItems(
                    id='selection_county',
                    options={"Regular_c": "Regular", "Normalized_c": "Normalized"},
                    value='Regular_c'
                ),
                dcc.Loading(dcc.Graph(id="county_graph"), type="cube")],
                width = 6
            ),
            dbc.Col([
                dcc.Slider(
                    1994,
                    2017,
                    step=None,
                    value=1994,
                    marks={str(year): str(year) for year in df1['year'].unique()},
                    id='year-slider'
                )])
        ]
        )
    ],
    fluid = True
)

# Unified slider callbacks
@app.callback(
    Output('graph-with-slider', 'figure'),
    Output('graph-with-slider2', 'figure'),

    Output("animate", "n_intervals"),
    Output("animate2", "n_intervals"),

    Output("year-slider", "value"),

    Input("animate", "n_intervals"),
    Input("animate2", "n_intervals"),

    Input("year-slider", "value")
)
def update_figure(n, n2, year):
    #print("ctx.triggered_id", ctx.triggered_id)
    print("n", n)
    print("n2", n2)

    Ndf= df1[df1.year == year]
    n_clicks = abs(((df1.year.max())-year)-((df1.year.max())-df1.year.min()))

    Ndf2 = df2[df2.year == 2002]
    if (year >= 2007 and year < 2012):
        Ndf2= df2[df2.year == 2007]
    elif (year >= 2012):
        Ndf2= df2[df2.year == 2012]

    #n_clicks2 = abs(((df2.year.max())-year)-((df2.year.max())-df2.year.min()))

   ######################################################################

    title_text = str(year)+' Bee data by State'

    fig = px.choropleth(Ndf,
                        locations='state', 
                        locationmode="USA-states", 
                        color='Bee Population',
                        color_continuous_scale="Viridis_r", 
                        scope="usa",
                        range_color=(0,169000),
                        title= title_text,
                        animation_frame='year') #make sure 'period_begin' is string type and sorted in
    
    # fig.update_layout(transition = {'duration': 9000})
    # #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    # fig.update_layout(transition_duration=500)

    ######################################################################

    title_text2 ='Bee data by County'

    fig2 = px.choropleth(Ndf2, geojson=counties, locations='county_ansi', color='value',
                           color_continuous_scale="Viridis_r",
                           #mapbox_style="carto-positron",
                           #range_color=(0, 129731),
                           scope="usa",
                           #zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           #opacity=0.5,
                           title = title_text2,
                           labels={'value':'Bee Population'},
                           animation_frame='year')
    
    #fig2.update_layout(transition = {'duration': 9000})
    #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    #fig2.update_layout(transition_duration=500)

    return fig, fig2, n_clicks, n_clicks, year
    #return fig, fig2, n_clicks, n_clicks2, year


# @app.callback(
#     Output('graph-with-slider2', 'figure'),
#     Output("animate2", "n_intervals"),
#     Output("year-slider", "value"),

#     Input("animate2", "n_intervals"),
#     Input("year-slider", "value")
# )
# def update_figure2(n, year):
#     if (ctx.triggered_id == "animate2"):

#         if n == None:
#             n = 0

#         CurYear = df2.year.min()+(n%((df2.year.max()+1)-df2.year.min()))
#         Ndf= df2[df2.year == CurYear]
#         year = CurYear
#         n_clicks = n
#     else:
#         Ndf= df2[df2.year == year]
#         n_clicks = abs(((df2.year.max())-year)-((df1.year.max())-df2.year.min()))

#     title_text = str(year)+' Bee data by County'

#     fig2 = px.choropleth(df2, geojson=counties, locations='county_ansi', color='value',
#                            color_continuous_scale="Viridis_r",
#                            #mapbox_style="carto-positron",
#                            #range_color=(0, 129731),
#                            scope="usa",
#                            #zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
#                            #opacity=0.5,
#                            title = title_text2,
#                            labels={'value':'Bee Population'},
#                           animation_frame='year')
    
#     fig2.update_layout(transition = {'duration': 9000})
#     #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

#     fig2.update_layout(transition_duration=500)

#     return fig2, n_clicks, year


# Bar chart button callbacks
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

if __name__ == "__main__":
    app.run_server(debug=True)


