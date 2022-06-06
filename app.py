import dash
import dash_leaflet as dl
import dash_leaflet.express as dlx
import geojson
import numpy as np
import pandas as pd
import plotly.express as px
from dash import dash_table, dcc, html, Output, Input
from dash_extensions.javascript import arrow_function, assign

from utils import (count_frequency, get_max_time_stopped,
                   get_max_time_stopped_grid, get_mean_time_stopped_grid,
                   get_total_bikes, get_info)


app = dash.Dash()

# load geojson
with open('dataset_motos.geojson') as f:
    data = geojson.load(f)

# creation of the style and colorbar
classes = [0, 10, 20, 30, 50]
style = dict(weight=2, opacity=1, color='white',
             dashArray='3', fillOpacity=0.7)

colorscale = ['#FED976', '#FD8D3C',
              '#FC4E2A', '#E31A1C', '#BD0026']

ctg = ["{}+".format(cls, classes[i + 1])
       for i, cls in enumerate(classes[:-1])] + ["{}+".format(classes[-1])]
colorbar = dlx.categorical_colorbar(
    categories=ctg, colorscale=colorscale, width=300, height=30, position="bottomleft")
style_handle = assign("""function(feature, context){
    const {classes, colorscale, style, colorProp} = context.props.hideout;  // get props from hideout
    const value = feature.properties[colorProp];  // get value the determines the color
    for (let i = 0; i < classes.length; ++i) {
        if (value > classes[i]) {
            style.fillColor = colorscale[i];  // set the fill color according to the class
        }
    }
    return style;
}""")

# info widget
info = html.Div(children=get_info(), id="info", className="info",
                style={"position": "absolute", "top": "10px", "right": "10px", "z-index": "1000"})

geojson_widget = dl.GeoJSON(
    id='geojson',
    data=data,
    options=dict(style=style_handle),
    zoomToBounds=True,
    zoomToBoundsOnClick=True,
    hoverStyle=arrow_function(
        dict(weight=5, color='#666', dashArray='')),
    hideout=dict(colorscale=colorscale,
                 classes=classes,
                 style=style,
                 colorProp="count"
                 )
)
map_dl = dl.Map(children=[dl.TileLayer(),
                          geojson_widget,
                          colorbar,
                          dl.GestureHandling(),
                          info
                          ],
                center=(40.45, -3.7),
                zoom=11,
                style={'height': '50vh'})

# metrics table table creation
df = pd.DataFrame({'Métrica': ['Cantidad total de motos disponibles',
                               'Máximo tiempo parada de un grid',
                               'Grid id con máximo tiempo de parada',
                               'Media total de tiempo de parada de todos los grids'],
                   'Valor': [get_total_bikes(data),
                             get_max_time_stopped(data),
                             get_max_time_stopped_grid(data),
                             get_mean_time_stopped_grid(data)]})
table = dash_table.DataTable(
    id='table',
    data=df.to_dict('records'),
    columns=[{"name": i, "id": i} for i in df.columns],
    style_cell={'textAlign': 'left'},)

# histogram
count, frequency = count_frequency(data)
fig = px.bar(x=count, y=frequency)

app.layout = html.Div(
    [dash.html.H1("Mapa"), map_dl,
     dash.html.H1("Métricas"), table,
     dash.html.H1("Histograma"), dcc.Graph(figure=fig)]
)


@app.callback(Output("info", "children"), [Input("geojson", "hover_feature")])
def info_hover(feature):
    return get_info(feature)


if __name__ == '__main__':
    app.run_server()
