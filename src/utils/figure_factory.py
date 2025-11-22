import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def _create_empty_figure(title, message="No Data Available"):
    """Helper to create a placeholder figure when data is empty."""
    fig = go.Figure()
    fig.update_layout(
        title=title,
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[{
            "text": message,
            "xref": "paper", "yref": "paper",
            "showarrow": False,
            "font": {"size": 20}
        }]
    )
    return fig

# ---------------------------------------------------------------------
# CHART 1: Hourly Collision Trends by Borough
# ---------------------------------------------------------------------
def create_hourly_borough_trend(df):
    if df.empty: return _create_empty_figure("Collision Frequency by Hour & Borough")
    
    # Group by Weekday too!
    grouped = df.groupby(['WEEKDAY', 'BOROUGH', 'HOUR'])['COLLISION_ID'].count().reset_index(name='Collision Count')
    
    # Use facet_col='WEEKDAY' to show side-by-side charts
    fig = px.line(
        grouped, 
        x='HOUR', 
        y='Collision Count', 
        color='BOROUGH',
        facet_col='WEEKDAY', 
        facet_col_wrap=4, # Wraps to new row after 4 days
        title='1. Hourly Collision Trends by Borough (Split by Weekday)',
        markers=False, # Turn off markers to reduce clutter
        template='plotly_dark'
    )
    fig.update_xaxes(dtick=4) # Show every 4th hour to save space
    return fig



# ---------------------------------------------------------------------
# CHART 4: Pedestrian Injuries (Borough vs Hour)
# ---------------------------------------------------------------------
def create_pedestrian_injury_heatmap(df):
    if df.empty: return _create_empty_figure("Pedestrian Injuries Heatmap")

    grouped = df.groupby(['BOROUGH', 'HOUR'])['NUMBER_OF_PEDESTRIANS_INJURED'].sum().reset_index()
    pivot = grouped.pivot(index='BOROUGH', columns='HOUR', values='NUMBER_OF_PEDESTRIANS_INJURED').fillna(0)

    fig = px.imshow(
        pivot,
        labels=dict(x="Hour", y="Borough", color="Injuries"),
        title="4. Pedestrian Injuries: Borough vs. Hour",
        template='plotly_dark',
        aspect="auto"  # Keeps cells square-ish
    )
    fig.update_xaxes(dtick=1)
    return fig

# ---------------------------------------------------------------------
# CHART 5: Cyclist Fatalities Trend
# ---------------------------------------------------------------------
def create_cyclist_fatality_trend(df):
    if df.empty: return _create_empty_figure("Cyclist Fatalities")
    
    # Group by Year to see the trend over time
    grouped = df.groupby(['YEAR'])['NUMBER_OF_CYCLIST_KILLED'].sum().reset_index()
    
    fig = px.bar(
        grouped, x='YEAR', y='NUMBER_OF_CYCLIST_KILLED',
        title='5. Cyclist Fatalities by Year',
        template='plotly_dark',
        color='NUMBER_OF_CYCLIST_KILLED',
        color_continuous_scale='Viridis'
    )
    fig.update_xaxes(dtick=1)
    return fig

# ---------------------------------------------------------------------
# CHART 6: Motorist Fatalities (Borough Breakdown)
# ---------------------------------------------------------------------
def create_motorist_fatality_trend(df):
    if df.empty: return _create_empty_figure("Motorist Fatalities")

    grouped = df.groupby(['YEAR', 'BOROUGH'])['NUMBER_OF_MOTORIST_KILLED'].sum().reset_index()
    
    fig = px.bar(
        grouped, x='YEAR', y='NUMBER_OF_MOTORIST_KILLED', color='BOROUGH',
        title='6. Motorist Fatalities by Borough & Year',
        barmode='group',
        template='plotly_dark'
    )
    fig.update_xaxes(dtick=1)
    return fig

# ---------------------------------------------------------------------
# CHART 7: Multi-Fatality Crashes (Where >1 Person Killed)
# ---------------------------------------------------------------------
def create_multi_fatality_boroughs(df):
    # Filter for severe crashes only
    severe_df = df[df['NUMBER_OF_PERSONS_KILLED'] > 0]
    if severe_df.empty: return _create_empty_figure("No Multi-Fatality Crashes Found")

    grouped = severe_df.groupby(['BOROUGH', 'HOUR'])['NUMBER_OF_PERSONS_KILLED'].count().reset_index(name='Crash Count')
    
    fig = px.bar(
        grouped, x='BOROUGH', y='Crash Count', color='HOUR',
        title='7. Distribution of Fatal Crashes by Borough',
        template='plotly_dark'
    )
    return fig



# ---------------------------------------------------------------------
# CHART 10: Long Term Trends (Area Chart)
# ---------------------------------------------------------------------
def create_long_term_trends(df):
    if df.empty: return _create_empty_figure("Long Term Trends")

    # Resample/Group by Year-Month to get a timeline
    # Note: Requires a proper datetime column. Assuming 'CRASH_DATETIME' exists and is datetime type.
    # If not, we use Year/Month columns.
    
    if 'CRASH_DATETIME' in df.columns:
        # Create a temporary date column for plotting
        temp_df = df.copy()
        temp_df['Date'] = pd.to_datetime(temp_df[['YEAR', 'MONTH']].assign(DAY=1))
        grouped = temp_df.groupby('Date')[['NUMBER_OF_PERSONS_INJURED', 'NUMBER_OF_PERSONS_KILLED']].sum().reset_index()
        
        fig = px.area(
            grouped, x='Date', y=['NUMBER_OF_PERSONS_INJURED', 'NUMBER_OF_PERSONS_KILLED'],
            title='10. Long-Term Trends: Injuries vs Fatalities',
            template='plotly_dark'
        )
    else:
        # Fallback if datetime conversion fails
        grouped = df.groupby('YEAR')[['NUMBER_OF_PERSONS_INJURED', 'NUMBER_OF_PERSONS_KILLED']].sum().reset_index()
        fig = px.bar(
            grouped, x='YEAR', y=['NUMBER_OF_PERSONS_INJURED', 'NUMBER_OF_PERSONS_KILLED'],
            barmode='group',
            title='10. Annual Trends: Injuries vs Fatalities',
            template='plotly_dark'
        )
        
    return fig
