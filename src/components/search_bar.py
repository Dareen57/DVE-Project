from dash import html, dcc

def generate_search_bar():
    return html.Div([
        html.Label("Search"),
        dcc.Input(
            id="search-input",
            type="text",
            placeholder="Type query, e.g. 'Brooklyn 2022 Monday 5 killed'",
            style={"width": "100%"}
        ),
        html.Button("Apply Search", id="search-btn", n_clicks=0),
        html.Hr()
    ])
