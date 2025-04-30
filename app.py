import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Streamlit page config
st.set_page_config(layout="wide")
st.title("U.S. Climate Risk Dashboard")
st.markdown("This dashboard displays simulated heat index and flood risk data by U.S. state.")

# Generate mock data
state_abbr = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL',
    'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT',
    'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI',
    'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

np.random.seed(42)
data = []
years = [2021, 2022, 2023]
for year in years:
    for state in state_abbr:
        data.append({
            'Year': year,
            'State': state,
            'Heat Index (°F)': round(np.random.uniform(85, 105), 1),
            'Flood Risk (%)': round(np.random.uniform(10, 90), 1),
            'Category': 'Aspirational' if np.random.rand() > 0.5 else 'General'
        })

df = pd.DataFrame(data)

# Sidebar UI ------------------------
st.sidebar.header("Filters")

# Year selector
year = st.sidebar.selectbox("Select Year", sorted(df['Year'].unique(), reverse=True))
df = df[df['Year'] == year]

# Category filter
category = st.sidebar.radio("Category", ['All', 'Aspirational', 'General'])
if category != 'All':
    df = df[df['Category'] == category]

# State multiselect
selected_states = st.sidebar.multiselect(
    "Filter by State", options=sorted(df['State'].unique()), default=sorted(df['State'].unique())
)
df = df[df['State'].isin(selected_states)]

# Indicator selection (expandable style)
st.sidebar.markdown("### Select Indicator")
with st.sidebar.expander("Climate Indicators"):
    indicator = st.radio("", ['Heat Index (°F)', 'Flood Risk (%)'], label_visibility="collapsed")

# Highlight one state (simulate zoom by filtering data)
highlight_state = st.sidebar.selectbox("Zoom to and Highlight State", ['All'] + sorted(df['State'].unique()))

# Filter only to selected state to simulate zoom
if highlight_state != 'All':
    df = df[df['State'] == highlight_state]
    zooming = True
else:
    zooming = False

# Normalize values for coloring
color_data = df[indicator]

# Determine appropriate colorscale
if indicator == 'Flood Risk (%)':
    colorscale = 'Blues' if zooming else [[0.0, 'rgb(230,240,255)'], [1.0, 'rgb(0,70,180)']]
else:
    colorscale = 'YlOrRd' if zooming else [[0.0, 'rgb(240,240,240)'], [1.0, 'rgb(200,0,0)']]

# Base choropleth
fig = go.Figure()
fig.add_trace(go.Choropleth(
    locations=df['State'],
    z=color_data,
    locationmode='USA-states',
    colorscale=colorscale,
    zmin=color_data.min(),
    zmax=color_data.max(),
    marker_line_color='black' if zooming else 'white',
    marker_line_width=2 if zooming else 1,
    showscale=True,
    colorbar_title=indicator,
    hovertext=[
        f"{row['State']}<br>Heat Index: {row['Heat Index (°F)']}°F<br>Flood Risk: {row['Flood Risk (%)']}%"
        for _, row in df.iterrows()
    ],
    hoverinfo="text"
))

fig.update_geos(
    scope='usa',
    projection_type='albers usa',
    bgcolor='rgba(0,0,0,0)'
)

fig.update_layout(
    title_text=f"U.S. States by {indicator} ({year})",
    margin=dict(l=0, r=0, t=40, b=0),
    geo=dict(bgcolor='rgba(0,0,0,0)')
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("Data shown is simulated for demonstration. Built with Streamlit and Plotly.")