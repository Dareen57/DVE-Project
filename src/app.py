from dash import Dash, html, dcc
from utils.data_loader import load_cleaned_data
from components.filters import generate_filter_dropdowns
from callbacks.update_charts import register_update_callbacks

# Load cleaned dataset
df = load_cleaned_data("data/NYC_crashes_persons_cleaned.csv")

# Initialize Dash app
app = Dash(__name__)
app.title = "NYC Crash Dashboard"

# Layout
app.layout = html.Div([
    html.H1("NYC Traffic Collision Analysis"),

    # Filters
    generate_filter_dropdowns(df),

    # # Generate Report button
    # html.Button("Generate Report", id="generate-report-btn"),

    # Main Chart
    dcc.Graph(id="main-chart"),
])

# Register callbacks
register_update_callbacks(app, df)

if __name__ == "__main__":
    app.run(debug=True)
