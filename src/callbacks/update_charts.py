from dash import Input, Output, State
import plotly.express as px
from utils.query_parser import parse_search_query

def register_update_callbacks(app, df):

    # Generate button callback
    @app.callback(
        Output("main-chart", "figure"),
        Input("generate-report-btn", "n_clicks"),
        [
            State("borough-dropdown", "value"),
            State("year-dropdown", "value"),
            State("month-dropdown", "value"),
            State("weekday-dropdown", "value"),
            State("hour-dropdown", "value"),
            State("metric-dropdown", "value")
        ],
        prevent_initial_call=True
    )
    def update_main_chart(n_clicks, borough, year, month, weekday, hour, metric):
        filtered = df.copy()
        if borough:
            filtered = filtered[filtered["BOROUGH"] == borough]
        if year:
            filtered = filtered[filtered["YEAR"] == year]
        if month:
            filtered = filtered[filtered["MONTH"] == month]
        if weekday:
            filtered = filtered[filtered["WEEKDAY"] == weekday]
        if hour is not None:
            filtered = filtered[filtered["HOUR"] == hour]


        # Create simple chart
        fig = px.histogram(
            filtered,
            x="YEAR",
            y=metric if metric else None,
            title=f"{metric.replace('_', ' ').title() if metric else 'Crashes'} per Year (Filtered)",
            labels={metric: metric.replace('_', ' ').title() if metric else "Count", "YEAR": "Year"}
        )
        return fig

    # Search input callback to set dropdowns
    @app.callback(
        Output("borough-dropdown", "value"),
        Output("year-dropdown", "value"),
        Output("month-dropdown", "value"),
        Output("weekday-dropdown", "value"),
        Output("hour-dropdown", "value"),
        Output("metric-dropdown", "value"),
        Input("search-btn", "n_clicks"),
        State("search-input", "value"),
        prevent_initial_call=True
    )
    def apply_search(n_clicks, query):
        if not query:
            return None, None, None, None, None, None
        parsed = parse_search_query(query)
        return parsed["borough"], parsed["year"], parsed["month"], parsed["weekday"], parsed["hour"], parsed["metric"]
