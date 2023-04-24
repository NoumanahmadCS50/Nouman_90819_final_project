import altair as alt
import pandas as pd
import streamlit as st

# Load data
data = pd.read_csv("Crashdata.csv")

# Set up Streamlit app
st.title("Seasonality in Crashes")

# Show data
st.write("## Data")
st.write(data)


# Create a dropdown menu for selecting the crash month
crash_month = data['CRASH_MONTH'].unique().tolist()
selected_category = st.selectbox("Select a month ", ["All"] + crash_month)

# Filter the data based on the selected month
if selected_category == "All":
    filtered_data = data
else:
    filtered_data = data[data['CRASH_MONTH'] == selected_category]

month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
filtered_data['CRASH_MONTH'] = pd.Categorical(filtered_data['CRASH_MONTH'], categories=month_order, ordered=True)
crashes_by_month = filtered_data.groupby(['CRASH_MONTH']).size().reset_index(name='counts')

total_crashes = filtered_data.shape[0]
st.write("<h2 style='text-align: center; font-size: 36px;'>Total number of crashes in Alleghany County: {}</h2>".format(total_crashes), unsafe_allow_html=True)


# Plot a bar chart of the crashes by month with the ordered x-axis
st.write("## Crashes by Month")
chart_month = alt.Chart(crashes_by_month).mark_bar().encode(
    x=alt.X('CRASH_MONTH', sort=month_order, axis=alt.Axis(title='Month')),
    y=alt.Y('counts', axis=alt.Axis(title='Number of crashes')),
    tooltip=['CRASH_MONTH', 'counts']
).properties(
    title='Crashes by Month',
    width=600,
    height=400
).configure_axis(
    labelFontSize=14,
    titleFontSize=16
).configure_title(
    fontSize=18
)
st.altair_chart(chart_month)

st.write("Use the dropdown menu to select a specific day or reset to display all days. The visualizations will be updated accordingly.")

# Create a dropdown menu for selecting the crash day
crash_day = data['DAY_OF_WEEK'].unique().tolist()
selected_category = st.selectbox("Select a day ", ["All"] + crash_day)

# Filter the data based on the selected day
if selected_category == "All":
    filtered_data = data
else:
    filtered_data = data[data['DAY_OF_WEEK'] == selected_category]

day_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
filtered_data['DAY_OF_WEEK'] = pd.Categorical(filtered_data['DAY_OF_WEEK'], categories=day_order, ordered=True)

# Plot a bar chart of the crashes by day of the week with the ordered x-axis
st.write("## Crashes by Day")
crashes_by_day = filtered_data.groupby(['DAY_OF_WEEK']).size().reset_index(name='counts')
chart_day = alt.Chart(crashes_by_day).mark_bar().encode(
    x=alt.X('DAY_OF_WEEK', sort=day_order, axis=alt.Axis(title='Day')),
    y=alt.Y('counts', axis=alt.Axis(title='Number of crashes')),
    tooltip=['DAY_OF_WEEK', 'counts']
).properties(width=600, height=400, title='Crashes by Day')

x=alt.X('CRASH_MONTH', sort=month_order, axis=alt.Axis(title='Month')),
st.altair_chart(chart_day)


# Plot a line chart of the daily crash occurrences by average temperature
st.write("## Monthly crash occurrences by average temperature")
crashes_by_temperature = data.groupby("WEATHER").size().reset_index(name="counts")
temperature_range = st.slider(
    "Select a temperature range",
    min_value=int(data["WEATHER"].min()),
    max_value=int(data["WEATHER"].max()),
    value=(int(data["WEATHER"].min()), int(data["WEATHER"].max())),
    step=1
)

filtered_data = crashes_by_temperature[
    (crashes_by_temperature["WEATHER"] >= temperature_range[0]) &
    (crashes_by_temperature["WEATHER"] <= temperature_range[1])
]

chart = alt.Chart(filtered_data).mark_line().encode(
    x="WEATHER:Q",
    y="counts:Q",
    tooltip=["WEATHER", "counts"]
).properties(width=600, height=400, title="Crashes by Temperature")

st.altair_chart(chart)

st.write("<h2 style='text-align: center; font-size: 36px;'>Highest number of crashes recorded when temperature falls below 2 degrees Celsius.</h2>", unsafe_allow_html=True)

# Plot a line chart of the daily crash occurrences by hour of the day
st.write("## Monthly crash occurrences by hour")
crashes_by_temperature = data.groupby("HOUR_OF_DAY").size().reset_index(name="counts")
temperature_range = st.slider(
    "Select a range",
    min_value=int(data["HOUR_OF_DAY"].min()),
    max_value=int(data["HOUR_OF_DAY"].max()),
    value=(int(data["HOUR_OF_DAY"].min()), int(data["HOUR_OF_DAY"].max())),
    step=1
)

filtered_data = crashes_by_temperature[
    (crashes_by_temperature["HOUR_OF_DAY"] >= temperature_range[0]) &
    (crashes_by_temperature["HOUR_OF_DAY"] <= temperature_range[1])
]

chart = alt.Chart(filtered_data).mark_line().encode(
    x="HOUR_OF_DAY:Q",
    y="counts:Q",
    tooltip=["HOUR_OF_DAY", "counts"]
).properties(width=600, height=400, title="Crashes by Hour")

st.write("<h2 style='text-align: center; font-size: 36px;'>Highest number of crashes recorded during rush hours.</h2>", unsafe_allow_html=True)

st.altair_chart(chart)
