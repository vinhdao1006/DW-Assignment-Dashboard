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
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import requests

#read from mongodb

file_path = "sample.csv"
df = pd.read_csv(file_path)

st.set_page_config(
    page_title = 'Real-Time USA Accidents Dashboard',
    page_icon = '🚨',
    layout = 'wide',
)

# dashboard title

st.title("Real-Time USA Accidents Dashboard")

selected_page = st.radio("Welcome!", ["Dashboard", "Report"], horizontal=True)

# # Dashboard Page
# if selected_page == "Dashboard":
    
#     st.header("Dashboard")
#     ##############################

#     # creating a single-element container.
#     placeholder = st.empty()


#     # near real-time / live feed simulation 

#     for seconds in range(200):
#     #while True: fdsdsafsadafdas
        
#         df['age_new'] = df['age'] * np.random.choice(range(1,5))
#         df['balance_new'] = df['balance'] * np.random.choice(range(1,5))

#         # creating KPIs 
#         avg_age = np.mean(df['age_new']) 

#         count_married = int(df[(df["marital"]=='married')]['marital'].count() + np.random.choice(range(1,30)))
        
#         balance = np.mean(df['balance_new'])

#         with placeholder.container():
#             # create three columns
#             kpi1, kpi2, kpi3 = st.columns(3)

#             # fill in those three columns with respective metrics or KPIs 
#             kpi1.metric(label="Age ⏳", value=round(avg_age), delta= round(avg_age) - 10)
#             kpi2.metric(label="Married Count 💍", value= int(count_married), delta= - 10 + count_married)
#             kpi3.metric(label="A/C Balance ＄", value= f"$ {round(balance,2)} ", delta= - round(balance/count_married) * 100)

#             # create two columns for charts 

#             fig_col1, fig_col2 = st.columns(2)
#             with fig_col1:
#                 st.markdown("### First Chart")
#                 fig = px.density_heatmap(data_frame=df, y = 'age_new', x = 'marital')
#                 st.write(fig)
#             with fig_col2:
#                 st.markdown("### Second Chart")
#                 fig2 = px.histogram(data_frame = df, x = 'age_new')
#                 st.write(fig2)
#             st.markdown("### Detailed Data View")
#             st.dataframe(df)
#             time.sleep(1)
        #placeholder.empty()
        ##############################

    
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
    df_id = df
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

        weather_main = weather_data.get("main", {})
        weather_wind = weather_data.get("wind", {})
        weather_conditions = weather_data.get("weather", [{}])[0]
        
        weather_report = {
            "Weather_Timestamp": start_time,
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
        #reports_collection.insert_one(report) #to insert to mongodb
        st.success("Report submitted successfully!")