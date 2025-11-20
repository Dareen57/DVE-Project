from dash import html, dcc

def generate_filter_dropdowns(df):
    return html.Div([
        
        # Borough filter
        html.Label("Borough"),
        dcc.Dropdown(
            id="borough-dropdown",
            options=[{"label": b, "value": b} for b in sorted(df["BOROUGH"].dropna().unique())],
            placeholder="Select Borough",
            clearable=True
        ),

        # Year filter
        html.Label("Year"),
        dcc.Dropdown(
            id="year-dropdown",
            options=[{"label": int(y), "value": int(y)} for y in sorted(df["CRASH_YEAR"].dropna().unique())],
            placeholder="Select Year",
            clearable=True
        ),

        # Vehicle type filter
        html.Label("Vehicle Type"),
        dcc.Dropdown(
            id="vehicle-dropdown",
            options=[{"label": v, "value": v} for v in sorted(df["VEHICLE_TYPE"].dropna().unique())],
            placeholder="Select Vehicle Type",
            clearable=True
        ),

        # Contributing factor filter
        html.Label("Contributing Factor"),
        dcc.Dropdown(
            id="factor-dropdown",
            options=[{"label": f, "value": f} for f in sorted(df["CONTRIBUTING_FACTOR"].dropna().unique())],
            placeholder="Select Factor",
            clearable=True
        ),

        # Injury type filter
        html.Label("Injury Type"),
        dcc.Dropdown(
            id="injury-dropdown",
            options=[
                {"label": "Injured", "value": "Injured"},
                {"label": "Killed", "value": "Killed"},
            ],
            placeholder="Select Injury Type",
            clearable=True
        ),

        # Generate Report Button
        html.Button("Generate Report", id="generate-report-btn", n_clicks=0),
    ])
