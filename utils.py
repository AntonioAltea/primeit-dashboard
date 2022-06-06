from typing import List, Union

import numpy as np
from dash import html


def get_total_bikes(data: dict) -> str:
    total = 0
    for features in data['features']:
        total = total + features['properties']['count']
    return str(total)


def get_max_time_stopped(data: dict) -> int:
    max_time_stopped = 0
    for features in data['features']:
        time_stopped = features['properties']['time_stopped']
        if time_stopped > max_time_stopped:
            max_time_stopped = time_stopped
    return time_stopped


def get_max_time_stopped_grid(data: dict) -> int:
    max_polygon = 0
    max_polygon_id = 0
    for features in data['features']:
        polygon = features['properties']['polygon']
        if polygon > max_polygon:
            max_polygon = polygon
            max_polygon_id = features['id']
    return max_polygon_id


def get_mean_time_stopped_grid(data: dict) -> int:
    polygon_list = []
    for features in data['features']:
        polygon_list.append(features['properties']['polygon'])
    return np.mean(polygon_list)


def count_frequency(data: dict) -> Union[List[int], List[int]]:
    # count, number of grids
    count_list = []
    for features in data['features']:
        count = features['properties']['count']
        if count in [values[0] for values in count_list]:
            index = [values[0] for values in count_list].index(count)
            count_list[index][1] = count_list[index][1] + 1
        else:
            count_list.append([count, 1])

    return [count_tuple[0] for count_tuple in count_list], [count_tuple[1] for count_tuple in count_list]

def get_info(feature=None):
    header = [html.H4("Grid info")]
    if not feature:
        return header + [html.P("Hoover over a grid")]
    return header + ['id: ', html.B(feature["id"]), html.Br(),
                     'count: ', feature["properties"]["count"], html.Br(),
                     'time stopped: ', feature['properties']['time_stopped']]
