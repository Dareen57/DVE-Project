from dash import Input, Output
import plotly.express as px

def register_update_callbacks(app, df):

    @app.callback(
        Output("main-chart", "figure"),
        Input("generate-report-btn", "n_clicks"),   # BUTTON triggers update
        [
            Input("borough-dropdown", "value"),
            Input("year-dropdown", "value"),
            Input("vehicle-dropdown", "value"),
            Input("factor-dropdown", "value"),
            Input("injury-dropdown", "value"),
        ],
        prevent_initial_call=True
    )
    def update_main_chart(n_clicks, borough, year, vehicle, factor, injury):

        filtered = df.copy()

        # Apply dropdown filters
        if borough:
            filtered = filtered[filtered["BOROUGH"] == borough]

        if year:
            filtered = filtered[filtered["CRASH_YEAR"] == year]

        if vehicle:
            filtered = filtered[filtered["VEHICLE_TYPE"].str.contains(vehicle, na=False)]

        if factor:
            filtered = filtered[filtered["CONTRIBUTING_FACTOR"].str.contains(factor, na=False)]

        if injury == "Injured":
            filtered = filtered[filtered["NUMBER OF PERSONS INJURED"] > 0]

        if injury == "Killed":
            filtered = filtered[filtered["NUMBER OF PERSONS KILLED"] > 0]

        # Create simple chart
        fig = px.histogram(
            filtered,
            x="CRASH_YEAR",
            title="Crashes per Year (Filtered)"
        )

        return fig
