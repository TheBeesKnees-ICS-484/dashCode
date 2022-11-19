import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import pathlib
import json
from urllib.request import urlopen

filepath = str(pathlib.Path(__file__).parent.resolve())



with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

df = pd.read_csv(filepath+"\data\\bee_colony_census_data_by_county - Copy.csv")
#df=df[['year','period','state','state_ansi', 'ag_district_code', 'county', 'county_ansi', 'value']]

stateAnsi = []

count_State = 0
for i in df.state_ansi:
    df.loc[count_State,"state_ansi"] = str(i).zfill(2)
    stateAnsi.append(str(str(i).zfill(2)))
    count_State=count_State+1

count_County = 0
for i in df.county_ansi:
    df.loc[count_County,"county_ansi"] = str(stateAnsi[count_County])+str(i).zfill(3)
    count_County=count_County+1

#print(df.county_ansi)
#print(counties)

df=df.sort_values("year") # Make sure you sort the time horizon column in ascending order because this column is in random order in the raw dataset

fig = px.choropleth(df, geojson=counties, locations='county_ansi', color='value',
                           color_continuous_scale="Viridis",
                           #mapbox_style="carto-positron",
                           #range_color=(0, 129731),
                           scope="usa",
                           #zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           #opacity=0.5,
                           labels={'value':'Beez'},
                          animation_frame='year')
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(figure=fig,),
])

if __name__ == '__main__':
    app.run_server(debug=True)
