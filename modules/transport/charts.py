import altair as alt
import pandas as pd
import streamlit as st

def kpi_card(title, value, help_text):
    st.metric(title, value, help=help_text)

def trend_chart(df: pd.DataFrame):
    daily_trips = df.groupby('pickup_date').size().reset_index(name='trip_count')
    chart = alt.Chart(daily_trips).mark_line(point=True).encode(
        x=alt.X('pickup_date:T', title='Date'),
        y=alt.Y('trip_count:Q', title='Number of Trips'),
        tooltip=['pickup_date:T', 'trip_count:Q']
    ).properties(title='Daily Trip Trend').interactive()
    return chart

def top_n_chart(df: pd.DataFrame, category: str, n: int = 10):
    top_items = df[category].value_counts().nlargest(n).reset_index()
    top_items.columns = [category, 'count']
    chart = alt.Chart(top_items).mark_bar().encode(
        x=alt.X('count:Q', title='Number of Trips'),
        y=alt.Y(f'{category}:N', title=category.replace("_", " ").title(), sort='-x'),
        tooltip=[alt.Tooltip(f'{category}:N'), 'count:Q']
    ).properties(title=f'Top {n} {category.replace("_", " ").title()}')
    return chart

def timing_heatmap(df: pd.DataFrame):
    heatmap_data = df.groupby(['pickup_weekday', 'pickup_hour']).size().reset_index(name='trip_count')
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    chart = alt.Chart(heatmap_data).mark_rect().encode(
        x=alt.X('pickup_hour:O', title='Hour of Day'),
        y=alt.Y('pickup_weekday:O', title='Day of Week', sort=weekday_order),
        color=alt.Color('trip_count:Q', title='Number of Trips'),
        tooltip=['pickup_weekday:N', 'pickup_hour:Q', 'trip_count:Q']
    ).properties(title='Trip Heatmap: Weekday vs. Hour')
    return chart

def distribution_chart(df: pd.DataFrame, field: str, title: str, x_title: str):
    """Creates a histogram for a given field."""
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(f'{field}:Q', bin=alt.Bin(maxbins=50), title=x_title),
        y=alt.Y('count():Q', title='Number of Trips'),
        tooltip=[alt.Tooltip(f'{field}:Q', bin=alt.Bin(maxbins=50), title=x_title), alt.Tooltip('count():Q', title='Number of Trips')]
    ).properties(
        title=title
    ).interactive()
    return chart

def pie_chart(df: pd.DataFrame, category: str, title: str):
    """Creates a pie chart for a given category."""
    data = df[category].value_counts().reset_index()
    data.columns = [category, 'count']
    
    chart = alt.Chart(data).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="count", type="quantitative"),
        color=alt.Color(field=category, type="nominal", title="Payment Type"),
        tooltip=[category, 'count']
    ).properties(
        title=title
    )
    return chart
