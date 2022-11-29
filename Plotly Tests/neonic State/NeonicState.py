import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import pathlib
from urllib.request import urlopen
from dash import Dash, dcc, html, Input, Output

filepath = str(pathlib.Path(__file__).parent.resolve())

df = pd.read_csv(filepath+"\data\\Lowest.csv")
#df=df['','State_FIPS_code','State','Compound','Year','Corn','Soybeans', 'Wheat', 'Cotton', 'Vegetables_and_fruit', 'Rice', 'Orchards_and_grapes', 'Alfalfa','Pasture_and_hay', 'Other_crops']
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
for i in df.State:
    for j in abbrev_to_us_state:
        if abbrev_to_us_state[j].lower()==i.lower():
            df.loc[count,"State"] = j
    count=count+1

#df.rename({'Other_crops':'Beez'},axis=1, inplace=True)
df=df.sort_values("Year") # Make sure you sort the time horizon column in ascending order because this column is in random order in the raw dataset

max_Values = [260376.4,87192.27355,23148.2,51351.3,137070.6,6937.4,100550,248.6,10.40597214,14349.7,269365.3366]

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='NeonicState'),
    dcc.Dropdown(
        options=[
            {'label': 'Corn',  'value':'Corn'},
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
        clearable=False,
        id='NStateDrop'
    )
])

@app.callback(
    Output('NeonicState', 'figure'),
    Input('NStateDrop', 'value')
)
def update_output(value):
    
    if value == 'Corn':
        rColor = max_Values[0]
    elif value == 'Soybeans':
        rColor = max_Values[1]
    elif value == 'Wheat':
        rColor = max_Values[2]
    elif value == 'Cotton':
        rColor = max_Values[3]
    elif value == 'Vegetables_and_fruit':
        value = 'Vegetables & fruit'
        df.rename({'Vegetables_and_fruit':'Vegetables & fruit'},axis=1, inplace=True)
        rColor = max_Values[4]
    elif value == 'Rice':
        rColor = max_Values[5]
    elif value == 'Orchards_and_grapes':
        value = 'Orchards & grapes'
        df.rename({'Orchards_and_grapes':'Orchards & grapes'},axis=1, inplace=True)
        rColor = max_Values[6]
    elif value == 'Alfalfa':
        rColor = max_Values[7]
    elif value == 'Pasture_and_hay':
        value = 'Pasture & Hay'
        df.rename({'Pasture_and_hay':'Pasture & Hay'},axis=1, inplace=True)
        rColor = max_Values[8]
    elif value == 'Other_crops':
        value = 'Other Crops'
        df.rename({'Other_crops':'Other Crops'},axis=1, inplace=True)
        rColor = max_Values[9]
    elif value == 'All_Crops':
        value = 'All Crops'
        df.rename({'All_Crops':'All Crops'},axis=1, inplace=True)
        rColor = max_Values[10]
    
    fig3 = px.choropleth(df3,
                    locations='State', 
                    locationmode="USA-states", 
                    color=value,
                    color_continuous_scale="Viridis_r", 
                    scope="usa",
                    range_color=(0,rColor),
                    animation_frame='Year') #make sure 'period_begin' is string type and sorted in ascending order
    fig3.update_layout(transition = {'duration': 9000})
    fig3.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return(fig3)

if __name__ == '__main__':
    app.run_server(debug=True)