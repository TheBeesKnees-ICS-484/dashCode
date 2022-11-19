import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import pathlib
from urllib.request import urlopen

filepath = str(pathlib.Path(__file__).parent.resolve())



df = pd.read_csv(filepath+"\data\honeyproduction.csv")
df=df[['state','numcol','yieldpercol','totalprod','stocks', 'priceperlb', 'prodvalue', 'year']]
df.rename({'yieldpercol':'Yield per Colony'},axis=1, inplace=True)
df=df.sort_values("year") # Make sure you sort the time horizon column in ascending order because this column is in random order in the raw dataset

fig = px.choropleth(df,
                    locations='state', 
                    locationmode="USA-states", 
                    color='Yield per Colony',
                    color_continuous_scale="Viridis_r", 
                    scope="usa",
                    animation_frame='year') #make sure 'period_begin' is string type and sorted in ascending order

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(figure=fig,),
])

if __name__ == '__main__':
    app.run_server(debug=True)
