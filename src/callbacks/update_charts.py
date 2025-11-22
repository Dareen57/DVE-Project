from dash import Input, Output, State
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

    # ---------------------------------------------------------
    # Search Bar Callback
    # ---------------------------------------------------------
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
        
        # Helper to wrap single values in lists (since dropdowns are multi=True)
        def wrap(val):
            return [val] if val and not isinstance(val, list) else val
            
        return (
            wrap(parsed.get("borough")), 
            wrap(parsed.get("year")), 
            wrap(parsed.get("month")), 
            wrap(parsed.get("weekday")), 
            wrap(parsed.get("hour")), 
            parsed.get("metric") # Metric is single select, so no wrap needed
        )

    # ---------------------------------------------------------
    # Main Update Callback
    # ---------------------------------------------------------
    @app.callback(
        [Output(f"chart-{i}", "figure") for i in range(1, 11)],
        Input("generate-report-btn", "n_clicks"),
        [State("borough-dropdown", "value"),
         State("year-dropdown", "value"),
         State("month-dropdown", "value"),
         State("weekday-dropdown", "value"),
         State("hour-dropdown", "value")]
    )
    def update_all_charts(n_clicks, borough, year, month, weekday, hour):
        filtered = df.copy()
        
        # --- FIXED FILTERING LOGIC ---
        # Checks if value is a list (Multi-select) or single value
        
        if borough:
            if isinstance(borough, list):
                filtered = filtered[filtered["BOROUGH"].isin(borough)]
            else:
                filtered = filtered[filtered["BOROUGH"] == borough]
                
        if year:
            if isinstance(year, list):
                filtered = filtered[filtered["YEAR"].isin(year)]
            else:
                filtered = filtered[filtered["YEAR"] == year]
                
        if month:
            if isinstance(month, list):
                filtered = filtered[filtered["MONTH"].isin(month)]
            else:
                filtered = filtered[filtered["MONTH"] == month]
                
        if weekday:
            if isinstance(weekday, list):
                filtered = filtered[filtered["WEEKDAY"].isin(weekday)]
            else:
                filtered = filtered[filtered["WEEKDAY"] == weekday]
                
        if hour is not None: # Hour can be 0, so check for None explicitly
            if isinstance(hour, list):
                filtered = filtered[filtered["HOUR"].isin(hour)]
            else:
                filtered = filtered[filtered["HOUR"] == hour]

        # --- GENERATE CHARTS ---
        return (
            create_hourly_borough_trend(filtered),
            create_monthly_fatality_trend(filtered),
            create_severity_by_hour_weekday(filtered),
            create_pedestrian_injury_heatmap(filtered),
            create_cyclist_fatality_trend(filtered),
            create_motorist_fatality_trend(filtered),
            create_multi_fatality_boroughs(filtered),
            create_severe_pedestrian_distribution(filtered),
            create_fatality_injury_correlation(filtered),
            create_long_term_trends(filtered)
        )
