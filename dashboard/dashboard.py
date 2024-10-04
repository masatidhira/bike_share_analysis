import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set_theme(style='dark')


def create_daily_orders_df(df):
    daily_orders_df = df.resample('M', on='date').sum()
    return daily_orders_df

def create_sum_casual_user_df(df):
    sum_casual_user_df = df.groupby("day").casual_user.sum().sort_values(ascending=False).reset_index()
    return sum_casual_user_df

def create_sum_registered_user_df(df):
    sum_registered_user_df = df.groupby("day").registered_user.sum().sort_values(ascending=False).reset_index()
    return sum_registered_user_df

def create_by_season_df(df):
    by_season_df = df.groupby("season").total_user.sum().sort_values(ascending=False).reset_index()
    return by_season_df

def create_by_weather_df(df):
    by_weather_df = df.groupby("weather").total_user.sum().sort_values(ascending=False).reset_index()
    return by_weather_df


# Load data
day_clean_df = pd.read_csv("dashboard/day_clean.csv")
hour_clean_df = pd.read_csv("dashboard/hour_clean.csv")


# Sort data by date and ensure 'date' datatype is date
for df in [day_clean_df, hour_clean_df]:
    df.sort_values(by="date", inplace=True)
    df.reset_index(inplace=True)
    df['date'] = pd.to_datetime(df['date'])

# Get minimum and maximum date
min_date = min(day_clean_df["date"].min(), hour_clean_df["date"].min()) 
max_date = max(day_clean_df["date"].max(), hour_clean_df["date"].max()) 

with st.sidebar:

    st.header(":sparkles: BikeShare :sparkles:")

    start_date, end_date = st.date_input(
        label='Time span',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_day_df = day_clean_df[(day_clean_df["date"] >= str(start_date)) & (day_clean_df["date"] <= str(end_date))]
main_hour_df = hour_clean_df[(hour_clean_df["date"] >= str(start_date)) & (hour_clean_df["date"] <= str(end_date))]


daily_orders_df = create_daily_orders_df(main_day_df)
sum_casual_user_df = create_sum_casual_user_df(main_day_df)
sum_registered_user_df = create_sum_registered_user_df(main_day_df)
by_season_df = create_by_season_df(main_day_df)
by_weather_df = create_by_weather_df(main_day_df)


# Header
st.header('Bike Share Dashboard :sparkles:')


# Total number of bicycles borrowed
st.subheader('Total Bike Borrowed')
col1, col2, col3 = st.columns(3)

with col1:
    total_casual = daily_orders_df.casual_user.sum()
    st.metric("by Casual User", value=f'{total_casual:,}')

with col2:
    total_registered = daily_orders_df.registered_user.sum()
    st.metric("by Registered User", value=f'{total_registered:,}')

with col3:
    total_users = daily_orders_df.total_user.sum()
    st.metric("Total", value=f'{total_users:,}')

colors = ["#A5B68D", "#FCFAEE", "#FCFAEE", "#FCFAEE"]


########################################## PLOT 1 ##########################################
st.subheader("Number of Bike Borrowed by Season")
fig_by_season, ax = plt.subplots(figsize=(30, 15))

sns.barplot(
    y="total_user", 
    x="season", 
    data=by_season_df,
    palette=colors,
    hue="season",
    ax=ax
)
ax.set_ylabel("Total User", fontsize=30)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis ='x', labelsize=30)
ax.ticklabel_format(style='plain', axis='y')

st.pyplot(fig_by_season)

########################################## PLOT 2 ##########################################
st.subheader("Number of Bike Borrowed by Weather")
fig_by_weather, ax = plt.subplots(figsize=(30, 15))

sns.barplot(
    y="total_user", 
    x="weather", 
    data=by_weather_df,
    palette=colors,
    hue="weather",
    ax=ax
)
ax.set_ylabel("Total User", fontsize=30)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis ='x', labelsize=30)
ax.ticklabel_format(style='plain', axis='y')

st.pyplot(fig_by_weather)

########################################## PLOT 3 ##########################################
st.subheader("Number of Bike Borrowed by Time of The Day")
fig_by_time_of_day, ax = plt.subplots(figsize=(30, 15))
sns.pointplot(
    data=main_hour_df,
    x='time_of_day',
    y='total_user',
    hue='workingday',
    errorbar=None,
    ax=ax)

ax.set_ylabel('Total User', fontsize=30)
ax.set_xlabel('Time of the day', fontsize=30)
ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis ='x', labelsize=30)

st.pyplot(fig_by_time_of_day)