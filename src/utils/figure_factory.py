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
    
    grouped = df.groupby(['BOROUGH', 'HOUR'])['COLLISION_ID'].count().reset_index(name='Collision Count')
    
    fig = px.line(
        grouped, x='HOUR', y='Collision Count', color='BOROUGH',
        title='1. Collision Frequency by Hour & Borough',
        markers=True, template='plotly_dark'
    )
    fig.update_xaxes(dtick=1)
    return fig

# ---------------------------------------------------------------------
# CHART 2: Monthly Fatalities Trend
# ---------------------------------------------------------------------
def create_monthly_fatality_trend(df):
    if df.empty: return _create_empty_figure("Fatalities by Month")

    # Sum fatalities by Month and Year
    grouped = df.groupby(['YEAR', 'MONTH'])['NUMBER_OF_PERSONS_KILLED'].sum().reset_index()
    
    fig = px.line(
        grouped, x='MONTH', y='NUMBER_OF_PERSONS_KILLED', color='YEAR',
        title='2. Fatalities by Month (Seasonal Trend)',
        markers=True, template='plotly_dark'
    )
    fig.update_xaxes(dtick=1, title="Month")
    fig.update_yaxes(title="Persons Killed")
    return fig

# ---------------------------------------------------------------------
# CHART 3: Severity by Weekday & Hour
# ---------------------------------------------------------------------
def create_severity_by_hour_weekday(df):
    if df.empty: return _create_empty_figure("Severity by Weekday & Hour")

    # Group by Weekday and Hour, sum fatalities
    grouped = df.groupby(['WEEKDAY', 'HOUR'])['NUMBER_OF_PERSONS_KILLED'].sum().reset_index()
    
    # Pivot for Heatmap format: Index=Weekday, Columns=Hour, Values=Killed
    pivot = grouped.pivot(index='WEEKDAY', columns='HOUR', values='NUMBER_OF_PERSONS_KILLED').fillna(0)
    
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot = pivot.reindex(days_order)

    fig = px.imshow(
        pivot,
        labels=dict(x="Hour", y="Weekday", color="Fatalities"),
        x=pivot.columns,
        y=pivot.index,
        title="3. Severity (Fatalities) Heatmap by Time",
        template='plotly_dark'
    )
    fig.update_xaxes(dtick=1)
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
# CHART 8: Severe Pedestrian Injuries Distribution
# ---------------------------------------------------------------------
def create_severe_pedestrian_distribution(df):
    # Filter for pedestrian injury incidents
    ped_df = df[df['NUMBER_OF_PEDESTRIANS_INJURED'] > 0]
    if ped_df.empty: return _create_empty_figure("No Pedestrian Injuries")

    fig = px.histogram(
        ped_df, x='HOUR', y='NUMBER_OF_PEDESTRIANS_INJURED', color='BOROUGH',
        title='8. Pedestrian Injuries Distribution by Hour',
        nbins=24,
        template='plotly_dark',
        barmode='stack'
    )
    fig.update_xaxes(dtick=1)
    return fig

# ---------------------------------------------------------------------
# CHART 9: Fatality vs Injury Correlation
# ---------------------------------------------------------------------
def create_fatality_injury_correlation(df):
    if df.empty: return _create_empty_figure("Fatality vs Injury")

    # Aggregate by Hour to reduce point crowding
    grouped = df.groupby('HOUR').agg({
        'NUMBER_OF_PERSONS_KILLED': 'sum',
        'NUMBER_OF_PERSONS_INJURED': 'sum'
    }).reset_index()

    fig = px.scatter(
        grouped, x='NUMBER_OF_PERSONS_INJURED', y='NUMBER_OF_PERSONS_KILLED',
        size='NUMBER_OF_PERSONS_INJURED',  # Bubble size
        hover_data=['HOUR'],
        title='9. Correlation: High Injury Hours vs Fatalities',
        labels={'NUMBER_OF_PERSONS_INJURED': 'Total Injuries (per Hour)', 'NUMBER_OF_PERSONS_KILLED': 'Total Fatalities'},
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
