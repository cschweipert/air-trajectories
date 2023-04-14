"""Dash app to fetch and display air trajectories."""
from __future__ import annotations
import requests
import dash_leaflet as dl
from dash import Dash, Output, Input, State, html, dcc
from dash.exceptions import PreventUpdate


app = Dash(__name__)

options = [
    {'label': 'Bangkok', 'value': 'bangkok_tha.3_1_th'},
    {'label': 'Kuala Lumpur', 'value': 'kuala lumpur_mys.4_1_my'}
    ]


def create_layer(date: str, city_id: str) -> list:
    """ Fetches data and creates multipolygin layer.
        Input: date: str, city_id: str
        Ouput: list
    """
    r = requests.get(
        f'https://api.energyandcleanair.org/v1/trajectories?location_id={city_id}&date={date}',
        timeout=10
        )

    data = r.json().get('data')

    trajectories = data[0].get('features')

    polylines = []

    for trajectory in trajectories:
        coordinates = trajectory.get('geometry').get('coordinates')

        polyline = [[location[1], location[0]] for location in coordinates]
        polylines.append(polyline)

    dash_polylines = [dl.Polyline(positions=poly, color='blue') for poly in polylines]
    map_center = [polylines[0][0][0], polylines[0][0][1]]

    return [dl.FeatureGroup(children=dash_polylines), map_center]


feature_group, center = create_layer('2022-01-05', 'bangkok_tha.3_1_th')

app.layout = html.Div(
    [
        html.Header(
            'Global Air Trajectories',
            className='header',
        ),
        dcc.Dropdown(id='city', className='dropdown', options=options),
        dcc.Input(id='date', className='input', placeholder='YYYY-MM-DD'),
        html.Button(
            id='button',
            className='button',
            children=['Get trajectories!']
            ),
        html.Br(),
        html.Div([dl.Map([dl.TileLayer(), feature_group],
                         center=center,
                         zoom=6,
                         style={'height': '50vh'})], id='trajectories')
    ])


@app.callback(
        [Output('trajectories', 'children')],
        [Input('button', 'n_clicks'), Input('date', 'value')],
        [State('city', 'value')])
def update_data(*args: str) -> list[any]:
    """ Fetches new data after user input and updates figure.
        Input: date: str, city: str
        Output: list[plotly figure]
    """
    n_clicks, date, city_id = args
    if n_clicks is None:
        raise PreventUpdate
    new_feature_group, new_center = create_layer(date, city_id)
    return [dl.Map([dl.TileLayer(), new_feature_group],
                   center=new_center,
                   zoom=6,
                   style={'height': '50vh'})]


if __name__ == '__main__':
    app.run_server(debug=True)
