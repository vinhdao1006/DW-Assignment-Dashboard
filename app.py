import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop 
import plotly.express as px # interactive charts 
import folium
from folium.plugins import MarkerCluster
import random
import seaborn as sns
import matplotlib.pyplot as plt
from lat_lon_data import get_lat_lon
from weather_data import get_weather_data
from datetime import datetime
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import requests


# page settings
st.set_page_config(
    page_title = 'Real-Time USA Accidents Dashboard',
    page_icon = '🚨',
    layout = 'wide',
)

# dashboard title
st.title("Real-Time USA Accidents Dashboard")

# Function to connect to MongoDB
@st.cache_resource
def get_mongo_client():
    db_uri = "mongodb+srv://vinhdaovinh1006:VinhDao1006@cluster1.0fg9v.mongodb.net/test"
    return MongoClient(db_uri, tls=True, tlsAllowInvalidCertificates=True)

# Function to fetch data from MongoDB
@st.cache_data
def fetch_accident_data():
    client = get_mongo_client()
    db = client['accident_db']
    reports_collection = db['accidents']
    data = list(reports_collection.find({}, {"_id": 0}))
    return pd.DataFrame(data)

# Establish connection and fetch data
try:
    df_accidents = fetch_accident_data()
    st.success("Connected to MongoDB and data fetched successfully!")
except Exception as e:
    st.error(f"Error connecting to MongoDB: {e}")

# Refresh data
def refresh_data():
    fetch_accident_data.clear()  # Clear the cached data
    df_accidents = fetch_accident_data()
    st.success("Data refreshed!")
    return df_accidents


selected_page = st.radio("Welcome!", ["Dashboard", "Report"], horizontal=True)

# # Dashboard Page
if selected_page == "Dashboard":
    ######### only refresh data when user is on dashboard
    
    st.header("Dashboard")
    
    # creating a single-element container.
    placeholder = st.empty()

    #current_time = datetime.now()

    current_time = datetime(2016, 5, 2, 0, 0, 0)
    st.write(f"Current Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")


    for seconds in range(180):
    #while True:
        # prepare data, dataframe and variables for all visualization
        
        # Filter data for the selected day
        df_accidents['Start_Time'] = pd.to_datetime(df_accidents['Start_Time'])
        current_day = current_time.date()
        previous_day = (current_time - pd.Timedelta(days=1)).date()

        # Get accidents for the current day
        current_day_accidents = df_accidents[df_accidents['Start_Time'].dt.date == current_day]
        total_current_day = len(current_day_accidents)

        # Get accidents for the previous day
        previous_day_accidents = df_accidents[df_accidents['Start_Time'].dt.date == previous_day]
        total_previous_day = len(previous_day_accidents)

        # Calculate percentage increase
        if total_previous_day == 0:
            percent_increase = "N/A (No accidents on the previous day)"
        else:
            percent_increase = ((total_current_day - total_previous_day) / total_previous_day) * 100
        
        with placeholder.container():
            #visualize
            # Display metrics
            st.metric(label="Total Accidents Today", value=total_current_day)
            st.metric(label="Total Accidents Yesterday", value=total_previous_day)
            if isinstance(percent_increase, str):
                st.write(f"Percentage Increase: {percent_increase}")
            else:
                st.metric(label="Percentage Increase from Yesterday", value=f"{percent_increase:.2f}%")




#     # Fetch data from MongoDB
#     accident_data = pd.DataFrame(list(accidents_collection.find()))
    
#     if not accident_data.empty:
#         # Summary Numbers
#         st.subheader("Accident Summary")
#         st.metric("Total Accidents", len(accident_data))
#         st.metric("High Severity Accidents", len(accident_data[accident_data["severity"] == "High"]))

#         # Heatmap of Accidents
#         st.subheader("Accident Heatmap")
#         plt.figure(figsize=(10, 6))
#         heatmap_data = accident_data.groupby(['latitude', 'longitude']).size().reset_index(name="count")
#         heatmap_pivot = heatmap_data.pivot("latitude", "longitude", "count")
#         sns.heatmap(heatmap_pivot, cmap="YlGnBu")
#         st.pyplot(plt)

#         # Real-Time Graphs
#         st.subheader("Accidents Over Time")
#         accident_data['date'] = pd.to_datetime(accident_data['submit_time'])
#         time_series = accident_data.groupby(accident_data['date'].dt.date).size()
#         st.line_chart(time_series)
#     else:
#         st.write("No data available in the accidents collection.")


# Report Page
st.markdown("""
        <style>
        .stButton>button {
            background-color: #4CAF50;  /* Green background */
            color: white;  /* White text */
            width: 100%;  /* Full width of the form */
            padding: 10px;  /* Increase padding */
            border-radius: 8px;  /* Rounded corners */
            font-size: 16px;  /* Larger font */
            font-weight: bold;  /* Bold text */
            border: none;  /* Remove default border */
            transition: background-color 0.3s;  /* Smooth color transition */
        }
        .stButton>button:hover {
            background-color: #45a049;  /* Slightly darker green on hover */
        }
        .stButton>button:active {
            background-color: #3e8e41;  /* Even darker when clicked */
        }
        </style>
        """, unsafe_allow_html=True)

if selected_page == "Report":
    st.header("Accident Report Submission")
    df = pd.read_csv("uscities.csv")
    df = df.dropna(subset=['state_id', 'county_name', 'city'])

    states = df['state_name'].unique()
    state = st.selectbox('Select State', states, index=0)
    df_state = df[df['state_name'] == state]
    
    state = df_state['state_id'].iloc[0]
    
    counties = df_state['county_name'].unique()
    county = st.selectbox('Select County', counties, index=0)
    df_county = df_state[df_state['county_name'] == county]
    
    cities = df_county['city'].unique()
    city = st.selectbox('Select City', cities, index=0)

    street = st.text_input("Street")

    description = st.text_area("Description of the Accident")
    severity = st.selectbox("Severity", ["1", "2", "3", "4", "5"])

    # Button to submit a report
    # Centered, compact submit button
    col1, col2, col3 = st.columns([3,1,3])
    with col2:
        submitted = st.button("Submit", type="primary")
        

    if submitted:
        # Save to MongoDB
        
        # get lat, lon
        address = street + " " + city + " " + county + " " + state
        lat, lon = get_lat_lon(address)
        
        # get weather data
        weather_data = get_weather_data(lat, lon)
        print(address)
        print(weather_data)
        
        highest_id = 0
        for report in reports_collection.find().sort([("ID", pymongo.DESCENDING)]).limit(1):
            highest_id = int(report["ID"].split("-")[1])
        new_id = f"A-{highest_id + 1}"

        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        round_time = start_time

        weather_main = weather_data.get("main", {})
        weather_wind = weather_data.get("wind", {})
        weather_conditions = weather_data.get("weather", [{}])[0]
        
        weather_report = {
            "Weather_Timestamp": round_time,
            "Temperature(F)": round((weather_main.get("temp", 0) - 273.15) * 9/5 + 32, 2),
            "Wind_Chill(F)": "",
            "Humidity(%)": weather_main.get("humidity", ""),
            "Pressure(in)": round(weather_main.get("pressure", 0) * 0.02953, 2),
            "Visibility(mi)": round(weather_data.get("visibility", 0) / 1609.34, 2),
            "Wind_Direction": weather_wind.get("deg", ""),
            "Wind_Speed(mph)": round(weather_wind.get("speed", 0) * 2.23694, 2),
            "Precipitation(in)": weather_data.get("rain", {}).get("1h", ""),
            "Weather_Condition": weather_conditions.get("main", "Clear")
        }

        report = {
            "ID": new_id,
            "Source": "Source2",
            "Severity": severity,
            "Start_Time": start_time,
            "End_Time": "",
            "Start_Lat": lat,
            "Start_Lng": lon,
            "End_Lat": "",
            "End_Lng": "",
            "Distance(mi)": 0,
            "Description": description,
            "Street": street,
            "City": city,
            "County": county,
            "State": state,
            "Zipcode": 0,
            "Country": "US",
            "Timezone": "US/Pacific",
            "Airport_Code": "",
            **weather_report,
            "Amenity": "False",
            "Bump": "False",
            "Crossing": "False",
            "Give_Way": "False",
            "Junction": "True",
            "No_Exit": "False",
            "Railway": "False",
            "Roundabout": "False",
            "Station": "False",
            "Stop": "False",
            "Traffic_Calming": "False",
            "Traffic_Signal": "False",
            "Turning_Loop": "False",
            "Sunrise_Sunset": "Day",
            "Civil_Twilight": "Day",
            "Nautical_Twilight": "Day",
            "Astronomical_Twilight": "Day"
        }
        
         #to insert to mongodb
        reports_collection.insert_one(report)
        
        st.success("Report submitted successfully!")