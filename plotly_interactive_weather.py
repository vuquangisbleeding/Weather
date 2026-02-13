import pandas as pd
import plotly.express as px

df = pd.read_csv(DATA_PATH, parse_dates=['date'])

# Read weather data
# You can change the path if needed
DATA_PATH = 'data/weather_data.csv'
df = pd.read_csv(DATA_PATH, parse_dates=['date'])

# Scatter plot of temperature with date range slider
fig = px.scatter(
    df,
    x='date',
    y='temp_celsius',
    color='rainfall_mm',
    title='Temperature by Date with Rainfall (Plotly)',
    labels={'temp_celsius': 'Temperature (°C)', 'rainfall_mm': 'Rainfall (mm)'},
)

# Add range slider and selector
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(visible=True),
        type="date"
    )
)

fig.show()
fig.write_html('plotly_weather.html', auto_open=True)
