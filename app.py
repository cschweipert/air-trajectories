import requests
from dash import Dash, html
import dash_leaflet as dl


app = Dash(__name__)

r = requests.get(f'https://api.energyandcleanair.org/v1/trajectories?location_id=kuala lumpur_mys.4_1_my&date=2022-01-05')

data = r.json().get('data')

trajectories = data[0].get('features')

polylines = []

for trajectory in trajectories:
    coordinates = trajectory.get('geometry').get('coordinates')

    polyline = [[location[1], location[0]] for location in coordinates]
    polylines.append(polyline)

dash_polylines = [dl.Polyline(positions=poly, color='blue') for poly in polylines]

feature_group = dl.FeatureGroup(
    children=dash_polylines
)

app.layout = html.Div([  
    dl.Map([dl.TileLayer(), feature_group], 
           center=(polylines[0][0][0], 
           polylines[0][0][1]), 
           zoom=6, 
           style={'height': '50vh'}),  
])


if __name__ == '__main__':
    app.run_server(debug=True)
