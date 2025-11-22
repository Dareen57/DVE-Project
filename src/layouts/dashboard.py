# layouts/dashboard.py
from dash import html, dcc
from components.filters import generate_filter_dropdowns
from components.search_bar import generate_search_bar

def create_dashboard_layout(df):
    return html.Div([
        html.H1("NYC Traffic Collision Analysis", className="text-center mb-4"),

        # Search Bar
        generate_search_bar(),

        # Filters (Imported from components)
        generate_filter_dropdowns(df),

        html.Hr(),

        # --- THE 10 CHART GRID ---
        html.Div([
            # Row 1: Charts 1 & 2
            html.Div([
                html.Div([dcc.Graph(id="chart-1")], className="six columns"),
                html.Div([dcc.Graph(id="chart-2")], className="six columns"),
            ], className="row"),

            # Row 2: Charts 3 & 4
            html.Div([
                html.Div([dcc.Graph(id="chart-3")], className="six columns"),
                html.Div([dcc.Graph(id="chart-4")], className="six columns"),
            ], className="row"),

            # Row 3: Charts 5 & 6
            html.Div([
                html.Div([dcc.Graph(id="chart-5")], className="six columns"),
                html.Div([dcc.Graph(id="chart-6")], className="six columns"),
            ], className="row"),

            # Row 4: Charts 7 & 8
            html.Div([
                html.Div([dcc.Graph(id="chart-7")], className="six columns"),
                html.Div([dcc.Graph(id="chart-8")], className="six columns"),
            ], className="row"),

            # Row 5: Charts 9 & 10
            html.Div([
                html.Div([dcc.Graph(id="chart-9")], className="six columns"),
                html.Div([dcc.Graph(id="chart-10")], className="six columns"),
            ], className="row"),

        ], className="container")
    ])
