import time

import dash
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objs as go
from dash import Input, Output, dcc, html, State, ctx
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

chart_text_color = "Black" #'rgb(255,223,51)'
chart_background_color = 'rgba(79,121,161,100%)'

map_text_color = "Gold"
map_background_color = 'rgba(35,87,137,20%)'
map_text_size = 18


############# Maps ################
df1 = pd.read_csv("Plotly Tests/State level map/data/Bee_data_market_state.csv")
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

# Adding in so dates for both neonic and bee data overlap
df1 = df1[df1["year"] >= 1994]
df1 = df1[df1["year"] <= 2017]

df3 = pd.read_csv("Plotly Tests/neonic State/data/LowEst_AgPestUse_Yearly_Combined.csv")

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
#print("NEONIC COLS: ", neonic_df.columns)

# Bee colony count data

# State Level
bee_state_df = pd.read_csv("preprocessed_bee_data/bee_colony_data/state_level/bee_state_summary_chart.csv")
#print("BEE STATE COLS: ", bee_state_df.columns)

# Combined data (normalized)
bee_state_neonic_df = bee_state_df.copy()

bee_state_neonic_df['Total Neonicotinoid Amount'] = neonic_df['Total Neonicotinoid Amount'].copy()

# Create graphs
WTI_fig = px.bar(WTI_df, x='genus', y='relative WTI', 
title="Relative Resistance to Neonicotinoids by Bee Species", labels={"genus":"Genus", "relative WTI": "Relative Resistance"})

WTI_fig.update_layout({
    #'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': chart_background_color,
},
font_color=chart_text_color,
font_size = map_text_size,
xaxis=dict(
    tickangle=90
)
)
#########################################

# MAKE LINE GRAPH PRESENTING SUMMARY of NEONIC USAGE AND BEE POPS
# Create figure with secondary y-axis
bee_state_neonic_fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
bee_state_neonic_fig.add_trace(
    go.Scatter(x=bee_state_neonic_df['Year'], y=bee_state_neonic_df['Bee Count'], name="Bee population",
    line = dict(color='rgb(241, 211, 2)', width=4), mode='lines+markers',
    marker = dict(size = 10, 
    line=dict(
            color='black',
            width=1)),
    ),
    secondary_y=False,
)

bee_state_neonic_fig.add_trace(
    go.Scatter(x=neonic_df['Year'], y=neonic_df['Total Neonicotinoid Amount'], name="Neonicotinoid usage",
    line = dict(color='rgb(135, 206, 235)', width=4), mode='lines+markers',
    marker = dict(size = 10,
    line=dict(
            color='black',
            width=1)),
    ),
    secondary_y=True,
)

# Add figure title
bee_state_neonic_fig.update_layout(
        {
    'plot_bgcolor': 'black',
},
    title_text="Comparing Neonicotinoid Usage and Bee Population Over Time (1994-2017)",
    yaxis1_tickvals = list(range(2_300_000, 2_900_000, 100_000)), yaxis2_tickvals = list(range(0, 6_000_000, 1_000_000))
    #xaxis_showgrid=False, yaxis_showgrid=False, xaxis_zeroline=False, yaxis_zeroline=False
)

bee_state_neonic_fig.update_layout({
    'paper_bgcolor': chart_background_color
    },
    font_color=chart_text_color,
    font_size=map_text_size,
    xaxis = dict(
        tickmode = "array",
        tickvals = list(range(1994, 2018)),
        ticktext = list(range(1994, 2018)),
        tickangle=90
    ),
    hoverlabel_align="right",
    hovermode="x unified",
    hoverlabel_namelength=-1 # so neonicotinoid label isn't cut off
)

# Set x-axis title
bee_state_neonic_fig.update_xaxes(title_text="Year")

# Set y-axes titles
bee_state_neonic_fig.update_yaxes(title_text="Bee Population (# colonies)", color="rgb(241, 211, 2)", 
title_font_color="rgb(241, 211, 2)",  showgrid=False, secondary_y=False) #showgrid=False
bee_state_neonic_fig.update_yaxes(title_text="Neonicotinoid Usage (kg)", color="rgb(135, 206, 235)", 
title_font_color="rgb(135, 206, 235)", showgrid=False, secondary_y=True, rangemode="tozero") #showgrid=False

#bee_state_neonic_fig.update_layout(yaxis=dict(range=[2000000, 3000000]))


###########################

image_filename = 'intro_material/bee.jpeg' 
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
                            html.H2("Pesticides and the Neonicotinoid Crisis", className="alert-heading", style={"text-decoration": "underline",},),
                            html.P(
                                "Pesticides called neonicotinoids (neonics), which have been embraced in recent decades by many commercial farms across the U.S, have led to mass deaths of pollinators. It is one of the major factors that has put one in four of North America???s 4,000 bee species at risk of extinction.", style={"font-size": 18},
                            ),
                            html.Br(),
                            html.P(
                                "Their loss is our loss, and that???s not an overstatement. One hundred percent of almonds, for example, are pollinated by bees, while 90 percent of apples, blueberries, and avocados are also the fruits of bees??? labor. If bees are taken out of the agricultural system, the cost of fruits and vegetables could multiply tenfold, pricing out vulnerable communities from any access to crucial sources of nutrition.", style={"font-size": 18},
                            ),
                            html.Hr(),
                            html.P(
                                    "Excerpt from:",
                                    className="mb-0",
                                    style={"font-size": 18},
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
                dbc.Col([
                     dbc.Alert(
                        [
                            html.H2("Relative Resistance", className="alert-heading", style={"text-decoration": "underline"},),
                            html.P(
                                "Neonicotinoids are toxic to bees, but they also cause a variety of detrimental side effects at sublethal levels depending on the species. These negative effects include problems with flight and navigation, reduced taste sensitivity, altered metabolism, slower learning ability (affects foraging), reduced olfactory response, and hindered reproduction.", style={"font-size": 18},
                            ),
                            html.Br(),
                            html.P(
                                "Resistance is represented by the weighted tolerance index (WTI). WTI is the relative degree of tolerance to the side effects of neonicotinoid intoxication. A higher WTI value indicates a greater tolerance.", style={"font-size": 18},
                            ),
                        ],
                        color="primary",
                    ),
                    # dbc.Fade(
                    #     dbc.Container([
                    #         dbc.Row([
                    #             dbc.Col(html.H1(id="year-counter", style={"color": "#FFF5EE"}), align="center"),
                    #             dbc.Col([html.H3("Bee Population Loss:", style={"color": "rgb(241, 211, 2)"}), 
                    #                     html.H3("Neonicotinoid Usage:", style={"color": "rgb(135, 206, 235)"})], 
                    #                     style={"white-space": "pre"}, width=4.5),
                    #             dbc.Col([html.H3(id="bee-loss-counter", style={"color": "rgb(241, 211, 2)", "text-align": "right"}),
                    #             html.H3(id="neonic-use-counter", style={"color": "rgb(135, 206, 235)", "text-align": "right"})], width=3,
                    #             #style={"background-color": "rgb(19, 47, 71, 0.7)"}
                    #             ),
                    #             dbc.Col(width=4.5)
                    #         ], className="g-0")
                    #     ], style={"margin-top": "20px"}),
                    #     id="counter-fade",
                    #     is_in=False,
                    #     appear=False,
                    #     # style={"transition": "opacity 100ms ease"},
                    #     # timeout=100,
                    # ),
                    #width=6,
            ]),
                dbc.Col(
                    dcc.Graph(figure=WTI_fig),
                    width=6,
                ),
            ],style={"padding-bottom": map_padding, "padding-left": 0},
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col([
                    dcc.Graph(id="graph-with-slider"),            
                
                                    #dbc.Fade(
                        dbc.Container([
                            dbc.Row([
                                dbc.Col(html.H1(id="year-counter", style={"color": "#FFF5EE"}), align="center"),
                                dbc.Col([html.H3("Bee Population Loss*:", style={"color": "rgb(241, 211, 2)"}), 
                                        html.H3("Neonicotinoid Usage:", style={"color": "rgb(135, 206, 235)"}),
                                        html.H6("*Negative value indicates bee pop. gain", style={"color": "rgb(241, 211, 2)", "font-size": "12px"})], 
                                        style={"white-space": "pre"}),
                                dbc.Col([html.H3(id="bee-loss-counter", style={"color": "rgb(241, 211, 2)", "text-align": "right"}),
                                html.H3(id="neonic-use-counter", style={"color": "rgb(135, 206, 235)", "text-align": "right"})]
                                #style={"background-color": "rgb(19, 47, 71, 0.7)"}
                                ),
                                #dbc.Col(width=4.5)
                            ], className="g-0")
                        ], style={"margin-top": "20px"}),
                    #     id="counter-fade",
                    #     is_in=False,
                    #     appear=False,
                    #     # style={"transition": "opacity 100ms ease"},
                    #     # timeout=100,
                    # ),
                ],
                    width = 6
            ),
            
                dbc.Col(
                [
                    dcc.Graph(id='NeonicState'),
                    dbc.Col([
                        dcc.RadioItems(
                            options=[
                                {'label': 'All Crops',  'value':'All_Crops'},
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
                                 
                            ],
                            value='All_Crops',
                            id='NStateDrop',
                            inline=True,
                            labelStyle={'display': 'block', 'font-size': '15px'},
                            style={'font-size': 40, 'color': 'rgb(135, 206, 235)'},
                            inputStyle={"margin-left": "5px"}
                        ) ,
            ]),
                
                ],
                    width = 6
                ),
                ], style={"padding-bottom": map_padding},
        ),
        dbc.Row(
            dbc.Col([
                html.Button("Reset", id="reset"),
                dcc.Interval(id="animate", max_intervals=23, interval=1000, disabled=True),
                dcc.Slider(
                    1994,
                    2017,
                    step=None,
                    value=1994,
                    marks={str(year): str(year) for year in df1['year'].unique()},
                    id='year-slider',
                    disabled=False
                ),
                html.Button("Play", id="play"),
                #html.Button(id="play"),
            ]),
        ),
        dbc.Row(
            [
            dbc.Col([
                dcc.Graph(figure=bee_state_neonic_fig, style={"padding-top": "20px"}),
            ]#,width = 9
            ),
            # dbc.Col([
            #     dbc.Card([
            #         dbc.CardHeader(html.H3(id="year-counter", style={"color": "red"})),
            #         dbc.CardBody([
            #             html.H4(id="bee-loss-counter", style={"color": "rgb(241, 211, 2)"}),
            #             html.H4(id="neonic-use-counter", style={"color": "rgb(35, 87, 137)"})
            #         ], style={"background-color": "white"})
            #     ])
            # ])
            ],style={"padding-bottom": map_padding},
        ),
        dbc.Row(
            [

            ]
        )
    ],
    fluid = True
)

# Unified slider callbacks
@app.callback(
    Output('graph-with-slider', 'figure'),
    Output("animate", "n_intervals"),

    Output("year-slider", "value"),

    Output('NeonicState', 'figure'),

    # For reset button
    Output("reset", "disabled"),   

    Output("animate", "disabled"), ######

    Output("play", "children"), # Change title of button if play is paused

    Output("year-slider", "disabled"), # Disable slider if playing animation

    Output("bee-loss-counter", "children"), #$$$$$$$$$$$
    Output("neonic-use-counter", "children"), #$$$$$$$$$$$
    Output("year-counter", "children"), #$$$$$$$$$$$

    #Output("counter-fade", "is_in"),

    Input("animate", "n_intervals"),
    #Input("animate2", "n_intervals"),

    Input("year-slider", "value"),

    # For neonic data
    Input('NStateDrop', 'value'),

    # For reset button
    Input("reset", "n_clicks"),
    State("reset", "disabled"),

    Input("play", "n_clicks"), ######
    State("animate", "disabled"), #####

    Input("year-slider", "disabled")
)
# n2 commented out
def update_figure(n, year, value, n3, playing, n4, playing2, year_slider):
    #print("ctx.triggered_id", ctx.triggered_id)
    #print("n", n)
    #print("n2", n2)
    #print("ctx.triggered_id", ctx.triggered_id)
    #print("n", n)
    #print("n2", n2)
    #print("n3", n3)
    #print("n4", n4)

    #print("playing2 is", playing2)

    show_counter = True
    if (ctx.triggered_id == "play" or ctx.triggered_id == "animate"):
        year_slider = True
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
        playing2 = True
        year_slider = False
        n_clicks = n
        #n_clicks = abs(((df1.year.max())-year)-((df1.year.max())-df1.year.min()))

    Ndf= df1[df1.year == year]
    # Checking Bee Population matches as expected
    print("Ndf year value sum for " + str(year) + " is:", Ndf['Bee Population'].sum())

    #n_clicks = abs(((df1.year.max())-year)-((df1.year.max())-df1.year.min()))

    print("The year is", year)

    Ndf5 = df3[df3['Year'] == year]
    title_fig1 = 'Bee Population by State in ' + str(year)

    title_fig5 = 'Neonicotinoid Usage by State & Crop in ' +  str(year)

    # First loading page or reset button was clicked
    if (ctx.triggered_id == "reset" or ctx.triggered_id == None):
        show_counter = False
        # Stop animation
        playing2 = True

        year = 1994

        Ndf= df1[df1.year == year]
        Ndf5 = df3[df3['Year'] == year]

        #Ndf = df1
        # Ndf3 = bee_state_neonic_df
        # Ndf3_norm = bee_state_neonic_df_normal
        # Ndf4 = bee_county_neonic_df
        # Ndf4_norm = bee_county_neonic_df_normal
        #Ndf5 = df3

        title_fig1 = 'Bee Population by State in 1994'

        title_fig5 = 'Neonicotinoid Usage by State & Crop in 1994'

        # Want slider to move back to the beginning
        #year = 1994

        n_clicks = 0

    #n_clicks2 = abs(((df2.year.max())-year)-((df2.year.max())-df2.year.min()))

    #bee_max = 510000
    #bee_max = 300000
    bee_max = 269365.3366

   ######################################################################

    print("The bee population for NDF is --->", (Ndf[['state']].count()), "<---")
    fig = px.choropleth(Ndf,
                        locations='state', 
                        locationmode="USA-states", 
                        color='Bee Population',
                        color_continuous_scale="Viridis", 
                        scope="usa",
                        range_color=(0,bee_max),
                        title= title_fig1,
                        #animation_frame='year',
                        height = map1_size
                        ) #make sure 'period_begin' is string type and sorted in

    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': map_background_color
    },
    font_color=map_text_color,
    font_size = map_text_size,
    geo=dict(bgcolor= 'rgba(0,0,0,0)')
    )

    fig.add_annotation(x=1.1, y=-0.25,
                text="measured in number of colonies",
                font=dict(size=10)
                )
    ######################################################################


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
        Ndf5 = Ndf5.rename({'Vegetables_and_fruit':'Vegetables & fruit'},axis=1)
        rColor = max_Values_Neonic[4]
    elif value == 'Rice':
        rColor = max_Values_Neonic[5]
    elif value == 'Orchards_and_grapes':
        value = 'Orchards & grapes'
        Ndf5 = Ndf5.rename({'Orchards_and_grapes':'Orchards & grapes'},axis=1)
        rColor = max_Values_Neonic[6]
    elif value == 'Alfalfa':
        rColor = max_Values_Neonic[7]
    elif value == 'Pasture_and_hay':
        value = 'Pasture & Hay'
        Ndf5 = Ndf5.rename({'Pasture_and_hay':'Pasture & Hay'},axis=1)
        rColor = max_Values_Neonic[8]
    elif value == 'Other_crops':
        value = 'Other Crops'
        Ndf5 = Ndf5.rename({'Other_crops':'Other Crops'},axis=1)
        rColor = max_Values_Neonic[9]
    elif value == 'All_Crops':
        value = 'All Crops'
        Ndf5 = Ndf5.rename({'All_Crops':'All Crops'},axis=1)
        rColor = max_Values_Neonic[10]
    
    fig5 = px.choropleth(Ndf5,
                    locations='State', 
                    locationmode="USA-states", 
                    color=value,
                    color_continuous_scale="Viridis", 
                    scope="usa",
                    title = title_fig5,
                    range_color=(0,rColor),
                    #animation_frame='Year',
                    height = map3_size
                    ) #make sure 'period_begin' is string type and sorted in ascending order

    fig5.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': map_background_color
    },
    font_color='rgb(135, 206, 235)',
    font_size = map_text_size,
    geo=dict(bgcolor= 'rgba(0,0,0,0)')
    )

    fig5.add_annotation(x=1.1, y=-0.25,
                text="amount in kilograms (kg)",
                font=dict(size=10)
                )

    play_text = "Play"
    # Stopping the slider at end
    print("n before end is", n)
    if (n != None and n >= 23):
        #print("n value is", n)
        print("playing2 again", playing2)
        play_text = "Restart"
        playing2 = True
    # if (year == 2017):
    #     "STOP HERE"
    #     playing2 = False

        # reset n_clicks
        n_clicks = 0
    elif ((n4 != None) and (n4 % 2 != 0)):
        play_text = "Pause"
    # Stopping player when they pause
    elif ((n4 != None) and (n4 % 2 == 0)):
        playing2 = True
        play_text = "Play"
    

    print("n_clicks is", n_clicks)
    print("playing2 at the end is", playing2)
    
    # FOR COUNTERS:
    # calculate current bee pop
    bee_data_year = bee_state_df[bee_state_df['Year'] == year]
    bee_count = np.array(bee_data_year['Bee Count'])[0].astype('int64')
    # bee_count_str = "Bee Population: " + "{:,}".format(bee_count)

    # To get bee loss
    bee_loss_count = 0
    if (year > 1994):
        bee_data_year_prior = bee_state_df[bee_state_df['Year'] == year - 1]
        bee_count_prior = np.array(bee_data_year_prior['Bee Count'])[0].astype('int64')
        bee_loss_count += bee_count_prior - bee_count
    # bee_loss_str = "Bee Population Loss: " + "{:,}".format(bee_loss_count)

    bee_loss_str = "{:,}".format(bee_loss_count)

    # calculate neonic usage
    neonic_data_year = neonic_df[neonic_df['Year'] == year]
    neonic_count = np.array(neonic_data_year['Total Neonicotinoid Amount'])[0].astype('int64')
    # neonic_count_str = "Neonicotinoid Usage: " + "{:,}".format(neonic_count)
    neonic_count_str = "{:,}".format(neonic_count)

    # Get year count
    year_count_str = str(year) + " Counts"

    return fig, n_clicks, year, fig5, playing, playing2, play_text, year_slider, bee_loss_str, neonic_count_str,  year_count_str, #show_counter

if __name__ == "__main__":
    app.run_server(debug=True)


