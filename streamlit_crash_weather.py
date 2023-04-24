# Now you can safely import the required packages
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Load data
data = pd.read_csv("CrashData.csv")

# Convert 'CRASH_MONTH' to numerical value and drop NaN values
data['CRASH_MONTH'] = pd.to_numeric(data['CRASH_MONTH'], errors='coerce')
data = data.dropna(subset=['CRASH_MONTH'])

# Set up Streamlit app
st.title("Weather and Crashes Analysis")

# Show data
st.write("## Data")
st.write(data)

# Create a dropdown menu for selecting the crashes by month
crash_month = data['CRASH_MONTH'].unique().tolist()
selected_category = st.selectbox("Select a month ", ["All"] + crash_month)

# Filter the data based on the selected month
if selected_category == "All":
    filtered_data = data
else:
    filtered_data = data[data['CRASH_MONTH'] == selected_category]

# Plot a bar chart of the crashes by month
st.write("## Crashes by Month")
crashes_by_months = filtered_data.groupby(['CRASH_MONTH']).size().reset_index(name='counts')
crashes_by_months = crashes_by_months.dropna()
fig, ax = plt.subplots()
sns.barplot(x='CRASH_MONTH', y='counts', data=crashes_by_months, ax=ax, palette='viridis')
plt.xticks(rotation=90)
st.pyplot(fig)

# Create a dropdown menu for selecting the crashes by day of the week
crash_day = data['DAY_OF_WEEK'].unique().tolist()
selected_category = st.selectbox("Select a day ", ["All"] + crash_day)

# Filter the data based on the selected day
if selected_category == "All":
    filtered_data = data
else:
    filtered_data = data[data['DAY_OF_WEEK'] == selected_category]

# Plot a bar chart of the crashes by day of the week
st.write("## Crashes by Day")
crashes_by_day = filtered_data.groupby(['DAY_OF_WEEK']).size().reset_index(name='counts')
fig, ax = plt.subplots()
sns.barplot(x='DAY_OF_WEEK', y='counts', data=crashes_by_day, ax=ax, palette='viridis')
plt.xticks(rotation=90)
st.pyplot(fig)

# Plot a line chart of the monthly crash occurrences by average temperature
st.write("## Monthly crashes by average temperature")
monthly_crash = filtered_data.set_index('DATE').resample('M')['CRASH_MONTH'].count().reset_index(name='counts')
monthly_weather = filtered_data.set_index('DATE').resample('M')['WEATHER'].mean().reset_index()
monthly_weather['avg_temp'] = (monthly_weather['WEATHER'])
monthly_data = pd.merge(monthly_crash, monthly_weather, on='CRASH_MONTH', how='outer')
monthly_data = monthly_data.dropna()
st.line_chart(monthly_data.set_index('CRASH_MONTH')[['counts', 'avg_temp']].rename(columns={'counts': 'Crash Occurrences', 'avg_temp': 'Avg. Temperature (C)'}), use_container_width=True)
