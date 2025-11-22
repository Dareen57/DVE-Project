# app.py
from dash import Dash
from utils.data_loader import load_cleaned_data
from layouts.dashboard import create_dashboard_layout  # <--- Import the layout
from callbacks.update_charts import register_update_callbacks

# Load Data
df = load_cleaned_data("data/NYC_crashes_persons_cleaned.parquet")

# Init App
app = Dash(__name__, external_stylesheets=['/assets/styles.css'])
app.title = "NYC Crash Dashboard"

# Assign Layout
app.layout = create_dashboard_layout(df)  # <--- Use the function

# Register Callbacks
register_update_callbacks(app, df)

if __name__ == "__main__":
    app.run(debug=True)


app = Dash(__name__)
server = app.server 