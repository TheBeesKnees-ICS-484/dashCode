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

map_padding = "24px"
map1_size = 400
graph_size = 375
map3_size = 400


############# Maps ################
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

df3 = pd.read_csv("Plotly Tests/neonic State/data/Lowest.csv")
count = 0
for i in df3.State:
    for j in abbrev_to_us_state:
        if abbrev_to_us_state[j].lower()==i.lower():
            df3.loc[count,"State"] = j
    count=count+1
df3=df3.sort_values("Year")
max_Values_Neonic = [260376.4,87192.27355,23148.2,51351.3,137070.6,6937.4,100550,248.6,10.40597214,14349.7,269365.3366]
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


# Combined data (normalized)
bee_state_neonic_df = bee_state_df.copy()
bee_state_neonic_df_normal = bee_state_df_normal.copy()

bee_state_neonic_df['Total Neonicotinoid Amount'] = neonic_df['Total Neonicotinoid Amount'].copy()
bee_state_neonic_df_normal['Total Neonicotinoid Amount'] = neonic_df_normal['Total Neonicotinoid Amount'].copy()

# Create graphs
WTI_fig = px.bar(WTI_df, x='genus', y='relative WTI', 
title="Relative Resistance to Neonicotinoids by Bee Species")

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
                            html.H2("Pesticides and the Neonicotinoid Crisis", className="alert-heading", style={"text-decoration": "underline"},),
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
                        color="primary",
                    ),
                    width=6,
                )
            ],
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(
                     dbc.Alert(
                        [
                            html.H2("Relative Resistance", className="alert-heading", style={"text-decoration": "underline"},),
                            html.P(
                                "Neonicotinoids are toxic to bees, but they also cause a variety of detrimental side effects at sublethal levels depending on the species. These negative effects include problems with flight and navigation, reduced taste sensitivity, altered metabolism, slower learning ability (affects foraging), reduced olfactory response, and hindered reproduction.",
                            ),
                            html.Br(),
                            html.P(
                                "Resistance is represented by the weighted tolerance index (WTI). WTI is the relative degree of tolerance to the side effects of neonicotinoid intoxication. A higher WTI value indicates a greater tolerance.",
                            ),
                        ],
                        color="primary",
                    ),
                    width=6,
                ),
                dbc.Col(
                    dcc.Graph(figure=WTI_fig),
                    width=6,
                ),
            ],style={"padding-bottom": map_padding},
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="graph-with-slider"),#dcc.Graph(figure=fig1,),
                    width = 6
            ),
                dbc.Col(
                [
                    dcc.RadioItems(
                        id='selection_state',
                        options={"Regular_s": "Regular", "Normalized_s": "Normalized"},
                        value='Regular_s'
                    ),
                    dcc.Graph(id="state_graph")],
                    width = 6
                ),
                ],style={"padding-bottom": map_padding},
        ),
        dbc.Row([
            dbc.Col([
            html.Button("Reset", id="reset"),
            dcc.Interval(id="animate", max_intervals=23, interval=3000, disabled=True),
            dcc.Slider(
                1994,
                2017,
                step=None,
                value=1994,
                marks={str(year): str(year) for year in df1['year'].unique()},
                id='year-slider'
            ),
            html.Button("Play", id="play"),])
    ]),
        dbc.Row(
            [
            dbc.Col([
                dcc.Graph(id='NeonicState'), 
            ],width = 6
            ),
            dbc.Col([
                dcc.RadioItems(
                    options=[
                        {'label': 'Corn', 'value':'Corn'},
                        {'label': 'Soybeans',  'value':'Soybeans'},
                        {'label': 'Wheat',  'value':'Wheat'},
                        {'label': 'Cotton',  'value':'Cotton'},
                        {'label': 'Vegetables & fruit',  'value':'Vegetables_and_fruit'},
                        {'label': 'Rice',  'value':'Rice'},
                        {'label': 'Orchards & grapes',  'value':'Orchards_and_grapes'},
                        {'label': 'Alfalfa',  'value':'Alfalfa'},
                        {'label': 'Pasture & Hay',  'value':'Pasture_and_hay'},
                        {'label': 'Other Crops',  'value':'Other_crops'},
                        {'label': 'All Crops',  'value':'All_Crops'}, 
                    ],
                    value='All_Crops',
                    id='NStateDrop',
                    labelStyle={'display': 'block'},
                    style={'font-size': 40}
                ), 
            ])
        ]
        )
    ],
    fluid = True
)

# Unified slider callbacks
@app.callback(
    Output('graph-with-slider', 'figure'),
    Output("animate", "n_intervals"),
    #Output("animate2", "n_intervals"),

    Output('state_graph', 'figure'),

    Output("year-slider", "value"),

    Output('NeonicState', 'figure'),

    # For reset button
    Output("reset", "disabled"),   

    Output("animate", "disabled"), ######

    Input("animate", "n_intervals"),
    #Input("animate2", "n_intervals"),

    Input("year-slider", "value"),

    # For switching between normalized and regular bar charts
    Input("selection_state", "value"),

    # For neonic data
    Input('NStateDrop', 'value'),

    # For reset button
    Input("reset", "n_clicks"),
    State("reset", "disabled"),

    Input("play", "n_clicks"), ######
    State("animate", "disabled"), #####
)
# n2 commented out
def update_figure(n, year, selection1, value, n3, playing, n4, playing2):
    #print("ctx.triggered_id", ctx.triggered_id)
    #print("n", n)
    #print("n2", n2)
    print("ctx.triggered_id", ctx.triggered_id)
    print("n", n)
    #print("n2", n2)
    print("n3", n3)
    print("n4", n4)

    print("playing2 is", playing2)
    if (ctx.triggered_id == "play" or ctx.triggered_id == "animate"):
        playing2 = False
        print("ANIMATE")
        if n == None:
            n = 0

        CurYear = 1994+((n)%((df1.year.max()+1)-1994))
        print("Current year is", CurYear)
        #Ndf= df1[df1.year == CurYear]
        year = CurYear
        n_clicks = n
    else:
        #Ndf= df1[df1.year == year]
        n_clicks = n
        #n_clicks = abs(((df1.year.max())-year)-((df1.year.max())-df1.year.min()))

    Ndf= df1[df1.year == year]
    #n_clicks = abs(((df1.year.max())-year)-((df1.year.max())-df1.year.min()))

    print("The year is", year)

    Ndf3 = bee_state_neonic_df[bee_state_neonic_df['Year'] == year]
    Ndf3_norm = bee_state_neonic_df_normal[bee_state_neonic_df_normal['Year'] == year]

    #Ndf5 = df3[df3['Year'] == year]

    title_fig1 = str(year)+' Bee population by State'

    title_fig3="State Level: Comparison of Neonicotinoid usage<br>and Bee Populations in " + str(year)
    title_fig3norm = "State Level: Normalized Comparison of Neonicotinoid usage<br>and Bee Populations in " + str(year)

    title_fig5 = str(year) + ' Neonicotinoid use by State & Crop'

    if ((n3 != None and n3 % 2 != 0) or ctx.triggered_id == None):
        Ndf = df1
        Ndf3 = bee_state_neonic_df
        Ndf3_norm = bee_state_neonic_df_normal
        Ndf5 = df3

        title_fig1 = ' Bee Population by State (1994-2017)'

        title_fig3 = "State Level: Comparison of Neonicotinoid usage<br>and Bee Populations (1994-2017)"
        title_fig3norm =  "State Level: Normalized Comparison of Neonicotinoid usage<br>and Bee Populations (1994-2017)"

        title_fig5 = 'Neonicotinoid use by State & Crop (1994-2017)'

        # Want slider to move back to the beginning
        year = 1994


    #n_clicks2 = abs(((df2.year.max())-year)-((df2.year.max())-df2.year.min()))

   ######################################################################

    fig = px.choropleth(Ndf,
                        locations='state', 
                        locationmode="USA-states", 
                        color='Bee Population',
                        color_continuous_scale="Viridis", 
                        scope="usa",
                        range_color=(0,169000),
                        title= title_fig1,
                        animation_frame='year',
                        height = map1_size
                        ) #make sure 'period_begin' is string type and sorted in

    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(35,87,137,20%)'
    },
    font_color="Gold",
    geo=dict(bgcolor= 'rgba(0,0,0,0)')
    )
    ######################################################################

    # State bee data neonic fig
    fig3 = px.bar(Ndf3, x="Year", y=['Total Neonicotinoid Amount', 'Bee Count'], barmode="group",
    title=title_fig3,
    height = graph_size,
    color_discrete_sequence=['rgb(35, 87, 137)', 'rgb(241, 211, 2)'])

    fig3.update_layout(xaxis=dict(
            tickmode = 'linear',
            tick0 = 1994,
            dtick = 1,
            tickangle = 90,
            # rangeslider=dict(
            # visible=True
            # )
        )
    )

    fig3_normal = px.bar(Ndf3_norm, x="Year", y=['Total Neonicotinoid Amount', 'Bee Count'], barmode="group",
    title=title_fig3norm,
    color_discrete_sequence=['rgb(35, 87, 137)', 'rgb(241, 211, 2)'])

    fig3_normal.update_layout(xaxis=dict(
            tickmode = 'linear',
            tick0 = 1994,
            dtick = 1,
            tickangle = 90,
            # rangeslider=dict(
            # visible=True
            # )
        )
    )

    ######################################################################
    # Update to normal / regular bar chart

    animations = {}

    if (selection1 == "Regular_s"):
        animations['selection1'] = fig3
    else:
        animations['selection1'] = fig3_normal

    ######################################################################

    if value == 'Corn':
        rColor = max_Values_Neonic[0]
    elif value == 'Soybeans':
        rColor = max_Values_Neonic[1]
    elif value == 'Wheat':
        rColor = max_Values_Neonic[2]
    elif value == 'Cotton':
        rColor = max_Values_Neonic[3]
    elif value == 'Vegetables_and_fruit':
        value = 'Vegetables & fruit'
        df3.rename({'Vegetables_and_fruit':'Vegetables & fruit'},axis=1, inplace=True)
        rColor = max_Values_Neonic[4]
    elif value == 'Rice':
        rColor = max_Values_Neonic[5]
    elif value == 'Orchards_and_grapes':
        value = 'Orchards & grapes'
        df3.rename({'Orchards_and_grapes':'Orchards & grapes'},axis=1, inplace=True)
        rColor = max_Values_Neonic[6]
    elif value == 'Alfalfa':
        rColor = max_Values_Neonic[7]
    elif value == 'Pasture_and_hay':
        value = 'Pasture & Hay'
        df3.rename({'Pasture_and_hay':'Pasture & Hay'},axis=1, inplace=True)
        rColor = max_Values_Neonic[8]
    elif value == 'Other_crops':
        value = 'Other Crops'
        df3.rename({'Other_crops':'Other Crops'},axis=1, inplace=True)
        rColor = max_Values_Neonic[9]
    elif value == 'All_Crops':
        value = 'All Crops'
        df3.rename({'All_Crops':'All Crops'},axis=1, inplace=True)
        rColor = max_Values_Neonic[10]
    
    Ndf5 = df3[df3['Year'] == year]
    
    fig5 = px.choropleth(Ndf5,
                    locations='State', 
                    locationmode="USA-states", 
                    color=value,
                    color_continuous_scale="Viridis", 
                    scope="usa",
                    title = title_fig5,
                    range_color=(0,rColor),
                    animation_frame='Year',
                    height = map3_size
                    ) #make sure 'period_begin' is string type and sorted in ascending order

    fig5.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(35,87,137,20%)'
    },
    font_color="Gold",
    geo=dict(bgcolor= 'rgba(0,0,0,0)')
    )

    if (n != None and n >= 23):
        #print("n value is", n)
        print("playing2 again", playing2)
        playing2 = not playing2

        # reset n_clicks
        n_clicks = 0

    print("n_clicks is", n_clicks)
    # second n_clicks commented out
    return fig, n_clicks, animations["selection1"], year, fig5, playing, playing2

if __name__ == "__main__":
    app.run_server(debug=True)


