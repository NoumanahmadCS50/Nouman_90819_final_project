
# Now you can safely import the required packages
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


# Load data
data = pd.read_excel("CrashData.xlsx")

# Set up Streamlit app
st.title("Weather and CRashes Analysis")

# Show data
st.write("## Data")
st.write(data)

st.write("Use the dropdown menu to select a specific month or reset to display all months. The visualizations will be updated accordingly.")

# Create a dropdown menu for selecting the crash    `1 month
crash_month = data['CRASH_MONTH'].unique().tolist()
selected_category = st.selectbox("Select a month ", ["All"] + crash_month)

# Filter the data based on the selected month
if selected_category == "All":
    filtered_data = data
else:
    filtered_data = data[data['CRASH_MONTH'] == selected_category]

# Use .loc to set values on the original DataFrame
filtered_data.loc[:, 'DATE'] = pd.to_datetime(filtered_data['DATE'])
filtered_data.loc[:, 'weather_category'] = pd.cut((filtered_data['high_temp'] + filtered_data['low_temp']) / 2, bins=[-100, 32, 60, 80, 1000], labels=['Freezing (<=0°C)', 'Cool (0°C to 15°C)', 'Warm (15°C to 26°C)', 'Hot (>26°C)'])

# Plot a bar chart of the crahses by months
st.write("## Crashes by Months")
crashes_by_months = filtered_data.groupby(['CRASH_MONTH']).size().reset_index(name='counts')
fig, ax = plt.subplots()
sns.barplot(x='CRASH_MONTH', y='counts', data=crashes_by_months, ax=ax, palette='viridis')
plt.xticks(rotation=90)
st.pyplot(fig)

st.write("Use the dropdown menu to select a specific day or reset to display all days. The visualizations will be updated accordingly.")

# Create a dropdown menu for selecting the crash    `1 day
crash_day = data['DAY_OF_WEEK'].unique().tolist()
selected_category = st.selectbox("Select a day ", ["All"] + crash_day)

# Filter the data based on the selected day
if selected_category == "All":
    filtered_data = data
else:
    filtered_data = data[data['DAY_OF_WEEK'] == selected_category]

# Use .loc to set values on the original DataFrame
filtered_data.loc[:, 'DATE'] = pd.to_datetime(filtered_data['DATE'])
filtered_data.loc[:, 'weather_category'] = pd.cut((filtered_data['high_temp'] + filtered_data['low_temp']) / 2, bins=[-100, 32, 60, 80, 1000], labels=['Freezing (<=0°C)', 'Cool (0°C to 15°C)', 'Warm (15°C to 26°C)', 'Hot (>26°C)'])

# Plot a bar chart of the crashes by day
st.write("## Crashes by Day")
crashes_by_day = filtered_data.groupby(['DAY_OF_WEEK']).size().reset_index(name='counts')
fig, ax = plt.subplots()
sns.barplot(x='DAY_OF_WEEK', y='counts', data=crashes_by_day, ax=ax, palette='viridis')
plt.xticks(rotation=90)
st.pyplot(fig)

# Plot a line chart of the monthly crime occurrences by average temperature
st.write("## Monthly crashes by average temperature")
monthly_crash = filtered_data.groupby(pd.Grouper(key='CRASH_MONTH', freq='M')).size().reset_index(name='counts')
monthly_weather = filtered_data.groupby(pd.Grouper(key='CRASH_MONTH', freq='M')).agg({'WEATHER': 'mean'}).reset_index()
monthly_weather['avg_temp'] = (monthly_weather['WEATHER'])
monthly_data = pd.merge(monthly_crime, monthly_weather, on='CRASH_MONTH', how='outer')
monthly_data = monthly_data.dropna()
st.line_chart(monthly_data.set_index('CRASH_MONT')[['counts', 'avg_temp']].rename(columns={'counts': 'Crash Occurrences', 'avg_temp': 'Avg. Temperature (C)'}), use_container_width=True)
