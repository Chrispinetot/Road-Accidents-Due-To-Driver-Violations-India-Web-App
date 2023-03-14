# import libraries
import numpy as np
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import json
import pandas as pd
import plotly.express as px
from main_app import app

# -- Import and clean data (importing csv into pandas)
data = pd.read_csv("response.csv")
print(data[:5])

# Preprocessing the data
data = data.rename(columns={"alcintake2014": "alcohol_2014", "overspeed2014": "overspeed_2014",
                            "overtaking2014": "overtake_2014", "lanejumping2014": "lanejump_2014",
                            "wrongside2014": "wrongside_2014", "signalavoid2014": "signalavoid_2014",
                            "asleep2014": "asleep_2014", "othercause2014": "others_2014",
                            "alcintake2016": "alcohol_2016", "overspeed2016": "overspeed_2016",
                            "overtaking2016": "overtake_2016", "lanejumping2016": "lanejump_2016",
                            "wrongside2016": "wrongside_2016", "signalavoid2016": "signalavoid_2016",
                            "asleep2016": "asleep_2016", "othercause2016": "others_2016"})
data = data.replace({"Arunachal Pradesh": "Arunanchal Pradesh", "Orissa": "Odisha",
                     "A & N Islands": "Andaman & Nicobar Island", "D & N Haveli": "Dadara & Nagar Havelli",
                     "Delhi": "NCT of Delhi"})
df = data.drop(["index", "sno", "region", "regionid", "stateut"], axis=1)
india_states = json.load(open("india.geojson", "r"))
state_id_map = {}
for feature in india_states["features"]:
    feature["id"] = feature["properties"]["state_code"]
    state_id_map[feature["properties"]["st_nm"]] = feature["id"]
data["stateid"] = data["stateut"].apply(lambda x: state_id_map[x])

choropleth_dropdown = html.Div([
    dcc.Dropdown(df.columns,
                 id="select_year",
                 multi=False,
                 clearable=False,
                 placeholder="click or dropdown or search",
                 value="alcohol_2014",
                 style={"width": "40%", "color": "black", "font_color": "black"}
                 ),
    html.Label("", htmlFor="state-dropdown", style={"font-family": "Georgia"})
])

graph_1 = dbc.Card(dcc.Graph(id='india_map', config={'displayModeBar': False}, figure={}))

# define the page layout
layout = dbc.Container([
    dbc.Row([
        html.Center(html.H3("Road Accident Causes Per State")),
        html.Br(),
        dbc.Row(choropleth_dropdown),
        html.Br(),
        dbc.Row(graph_1),
    ])
])


# page 1 callback
@app.callback(
    Output(component_id='india_map', component_property='figure'),
    [Input(component_id='select_year', component_property='value')]
)
def update_graph(option_slctd):
    # container = "The accident cause chosen by user is: {}".format(option_slctd)
    data["Cause_Scale"] = np.log10(data[option_slctd], where=(data[option_slctd] != 0))

    fig = px.choropleth(data,
                        locations="stateid",
                        geojson=india_states,
                        color="Cause_Scale",
                        hover_name="stateut",
                        hover_data=[option_slctd],
                        color_continuous_scale=px.colors.diverging.Portland,
                        template=None)
    fig.update_layout(title_text="2014/16 Road Accident Causes Per State", title_x=0.5,
                      font_family="Times New Roman", title_font_family="Times New Roman",
                      title_font_color="black", legend_title_font_color="green",
                      margin=dict(t=0, b=0, l=0, r=0))
    fig.update_geos(fitbounds="locations", visible=False)

    return fig
