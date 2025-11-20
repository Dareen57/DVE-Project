from dash import Input, Output, State
import plotly.express as px

def register_update_callbacks(app, df):

    @app.callback(
        Output("main-chart", "figure"),

        # ONLY the button is Input (trigger)
        Input("generate-report-btn", "n_clicks"),

        # Dropdowns are State (read-only, not triggers)
        [
            State("borough-dropdown", "value"),
            State("year-dropdown", "value"),
            State("vehicle-dropdown", "value"),
            State("factor-dropdown", "value"),
            State("injury-dropdown", "value"),
        ],
        prevent_initial_call=True
    )
    def update_main_chart(n_clicks, borough, year, vehicle, factor, injury):

        filtered = df.copy()

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

        fig = px.histogram(
            filtered,
            x="CRASH_YEAR",
            title="Crashes per Year (Filtered)"
        )
        return fig
