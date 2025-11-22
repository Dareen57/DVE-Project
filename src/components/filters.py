from dash import html, dcc

def generate_filter_dropdowns(df):
    return html.Div([
        # Borough filter
        html.Label("Borough"),
        dcc.Dropdown(
            id="borough-dropdown",
            options=[{"label": b, "value": b} for b in sorted(df["BOROUGH"].dropna().unique())],
            placeholder="Select Borough",
            clearable=True,
            multi=True
        ),

        # Year filter
        html.Label("Year"),
        dcc.Dropdown(
            id="year-dropdown",
            options=[{"label": int(y), "value": int(y)} for y in sorted(df["YEAR"].dropna().unique())],
            placeholder="Select Year",
            clearable=True,
            multi=True

        ),

        # Month filter
        html.Label("Month"),
        dcc.Dropdown(
            id="month-dropdown",
            options=[{"label": int(m), "value": int(m)} for m in sorted(df["MONTH"].dropna().unique())],
            placeholder="Select Month",
            clearable=True,
            multi=True
        ),

        # Weekday filter
        html.Label("Weekday"),
        dcc.Dropdown(
            id="weekday-dropdown",
            options=[{"label": w, "value": w} for w in sorted(df["WEEKDAY"].dropna().unique())],
            placeholder="Select Weekday",
            clearable=True,
            multi=True
        ),

        # Hour filter
        html.Label("Hour"),
        dcc.Dropdown(
            id="hour-dropdown",
            options=[{"label": h, "value": h} for h in sorted(df["HOUR"].dropna().unique())],
            placeholder="Select Hour",
            clearable=True,
            multi=True
        ),

        # Column selector for injury/fatality
        html.Label("Metric"),
        dcc.Dropdown(
            id="metric-dropdown",
            options=[
                {"label": "Persons Killed", "value": "NUMBER_OF_PERSONS_KILLED"},
                {"label": "Pedestrians Injured", "value": "NUMBER_OF_PEDESTRIANS_INJURED"},
                {"label": "Cyclists Killed", "value": "NUMBER_OF_CYCLIST_KILLED"},
                {"label": "Motorists Killed", "value": "NUMBER_OF_MOTORIST_KILLED"}
            ],
            placeholder="Select Metric",
            clearable=False,
        ),

        # Generate Report Button
        html.Button("Generate Report", id="generate-report-btn", n_clicks=0),
    ])
