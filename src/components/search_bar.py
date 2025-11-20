# components/search_bar.py
from dash import html, dcc

def search_bar():
    return html.Div(
        id="search-mode-container",
        children=[
            html.H3("Search mode"),
            dcc.Input(
                id="search-query",
                type="text",
                placeholder="e.g. 'Brooklyn 2022 pedestrian crashes'",
                style={"width": "60%"},
            ),
            html.Button(
                "Apply Search",
                id="search-apply-button",
                n_clicks=0,
            ),
            html.Div(
                id="search-status",
                style={"marginTop": "0.5rem", "fontStyle": "italic"},
            ),
        ],
        style={"marginBottom": "1.5rem"},
    )
