import altair as alt
import pandas as pd
import streamlit as st

# Load data
data = pd.read_csv("CrashData.csv")

# Set up Streamlit app
st.title("Weather and Crashes Analysis")

# Show data
st.write("## Data")
st.write(data)

st.write("Use the dropdown menu to select a specific month or reset to display all months. The visualizations will be updated accordingly.")

# Create a dropdown menu for selecting the crash month
crash_month = data['CRASH_MONTH'].unique().tolist()
selected_category = st.selectbox("Select a month ", ["All"] + crash_month)

# Filter the data based on the selected month
if selected_category == "All":
    filtered_data = data
else:
    filtered_data = data[data['CRASH_MONTH'] == selected_category]

# Plot a bar chart of the crashes by month
st.write("## Crashes by Month")
crashes_by_month = filtered_data.groupby(['CRASH_MONTH']).size().reset_index(name='counts')
chart_month = alt.Chart(crashes_by_month).mark_bar().encode(
    x=alt.X('CRASH_MONTH', sort=None),
    y='counts',
    tooltip=['CRASH_MONTH', 'counts']
).properties(width=600, height=400, title='Crashes by Month')
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

# Plot a bar chart of the crashes by day
st.write("## Crashes by Day")
crashes_by_day = filtered_data.groupby(['DAY_OF_WEEK']).size().reset_index(name='counts')
chart_day = alt.Chart(crashes_by_day).mark_bar().encode(
    x=alt.X('DAY_OF_WEEK', sort=None),
    y='counts',
    tooltip=['DAY_OF_WEEK', 'counts']
).properties(width=600, height=400, title='Crashes by Day')
st.altair_chart(chart_day)
