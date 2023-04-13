from dash import Dash, html
import dash_leaflet as dl

app = Dash(__name__)

app.layout = html.Div([  
    dl.Map(dl.TileLayer()),
])

if __name__ == '__main__':
    app.run_server(debug=True)
