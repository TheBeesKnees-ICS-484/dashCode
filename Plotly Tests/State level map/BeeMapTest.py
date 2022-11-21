import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import pathlib
from urllib.request import urlopen
from dash.dependencies import Input, Output, State
from dash import ctx
filepath = str(pathlib.Path(__file__).parent.resolve())

df = pd.read_csv(filepath+"\data\\bee_colony_survey_data_by_state.csv")
df=df[['year','period','week_ending','state','state_ansi', 'watershed', 'data_item', 'value']]
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
for i in df.state:
    for j in abbrev_to_us_state:
        if abbrev_to_us_state[j].lower()==i.lower():
            df.loc[count,"state"] = j
    count=count+1

df.rename({'value':'Beez'},axis=1, inplace=True)
df=df.sort_values("year") # Make sure you sort the time horizon column in ascending order because this column is in random order in the raw dataset

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Interval(id="animate", disabled=True),
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        df.year.min(),
        df.year.max(),
        step=None,
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        id='year-slider'
    ),
    html.Button("Play", id="play"),
])

@app.callback(
    Output('graph-with-slider', 'figure'),
    Output("animate", "n_intervals"),
    Output("year-slider", "value"),
    Input("animate", "n_intervals"),
    Input("year-slider", "value")
)
def update_figure(n, year):
    if (ctx.triggered_id == "animate"):

        if n == None:
            n = 0

        CurYear = df.year.min()+(n%((df.year.max()+1)-df.year.min()))
        Ndf= df[df.year == CurYear]
        year = CurYear
        n_clicks = n
    else:
        Ndf= df[df.year == year]
        n_clicks = abs(((df.year.max())-year)-((df.year.max())-df.year.min()))

    title_text = str(year)+' Bee data by State'

    fig = px.choropleth(Ndf,
                        locations='state', 
                        locationmode="USA-states", 
                        color='Beez',
                        color_continuous_scale="Viridis_r", 
                        scope="usa",
                        range_color=(0,169000),
                        title= title_text
    )
    fig.update_layout(transition = {'duration': 9000})
    #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    fig.update_layout(transition_duration=500)

    return fig, n_clicks, year

@app.callback(
    Output("animate", "disabled"),
    Input("play", "n_clicks"),
    State("animate", "disabled"),
)
def toggle(n, playing):
    print(playing)
    if n:
        return not playing
    return playing

if __name__ == '__main__':
    app.run_server(debug=True)

