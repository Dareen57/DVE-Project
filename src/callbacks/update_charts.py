from dash import Input, Output, State
# Import the figure factory functions we are about to write
from utils.figure_factory import (
    create_hourly_borough_trend,
    create_monthly_fatality_trend,
    create_severity_by_hour_weekday,
    create_pedestrian_injury_heatmap,
    create_cyclist_fatality_trend,
    create_motorist_fatality_trend,
    create_multi_fatality_boroughs,
    create_severe_pedestrian_distribution,
    create_fatality_injury_correlation,
    create_long_term_trends
)
from utils.query_parser import parse_search_query

def register_update_callbacks(app, df):


    @app.callback(
        [Output("borough-dropdown", "value"),
         Output("year-dropdown", "value"),
         Output("month-dropdown", "value"),
         Output("weekday-dropdown", "value"),
         Output("hour-dropdown", "value"),
         Output("metric-dropdown", "value")],
        Input("search-btn", "n_clicks"),
        State("search-input", "value"),
        prevent_initial_call=True
    )
    def apply_search(n_clicks, query):
        if not query:
            return None, None, None, None, None, None
        parsed = parse_search_query(query)
        # Returns the values to auto-populate the dropdowns
        return (parsed.get("borough"), parsed.get("year"), 
                parsed.get("month"), parsed.get("weekday"), 
                parsed.get("hour"), parsed.get("metric"))


    @app.callback(
        # LIST ALL 10 OUTPUTS HERE
        [Output("chart-1", "figure"),
         Output("chart-2", "figure"),
         Output("chart-3", "figure"),
         Output("chart-4", "figure"),
         Output("chart-5", "figure"),
         Output("chart-6", "figure"),
         Output("chart-7", "figure"),
         Output("chart-8", "figure"),
         Output("chart-9", "figure"),
         Output("chart-10", "figure")],
        
        # Trigger: The "Generate Report" button
        Input("generate-report-btn", "n_clicks"),
        
        # State: The values of all filters
        [State("borough-dropdown", "value"),
         State("year-dropdown", "value"),
         State("month-dropdown", "value"),
         State("weekday-dropdown", "value"),
         State("hour-dropdown", "value")]
    )
    def update_all_charts(n_clicks, borough, year, month, weekday, hour):
        # 1. Filter the DataFrame (Your existing logic)
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

        # 2. Generate the 10 Figures using the Factory
        
        fig1 = create_hourly_borough_trend(filtered)
        fig2 = create_monthly_fatality_trend(filtered)
        fig3 = create_severity_by_hour_weekday(filtered)
        fig4 = create_pedestrian_injury_heatmap(filtered)
        fig5 = create_cyclist_fatality_trend(filtered)
        fig6 = create_motorist_fatality_trend(filtered)
        fig7 = create_multi_fatality_boroughs(filtered)
        fig8 = create_severe_pedestrian_distribution(filtered)
        fig9 = create_fatality_injury_correlation(filtered)
        fig10 = create_long_term_trends(filtered)

        # 3. Return them in the exact order of the Outputs
        return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10
