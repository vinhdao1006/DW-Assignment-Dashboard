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

#read from mongodb

file_path = "sample.csv"
df = pd.read_csv(file_path)

st.set_page_config(
    page_title = 'Real-Time Data Science Dashboard',
    page_icon = '✅',
    layout = 'wide',
)

# dashboard title

st.title("DSS911")

selected_page = st.radio("Navigation", ["Dashboard", "Report"], horizontal=True)

# Dashboard Page
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
#         #placeholder.empty()
#         ##############################

    

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
if selected_page == "Report":
    st.header("Accident Report Submission")
    df = pd.read_csv("uscities.csv")
    df = df.dropna(subset=['state_name', 'county_name', 'city'])

    states = df['state_name'].unique()
    state = st.selectbox('Select State', states, index=0)
    df_state = df[df['state_name'] == state]
    
    counties = df_state['county_name'].unique()
    county = st.selectbox('Select County', counties, index=0)
    df_county = df_state[df_state['county_name'] == county]
    
    cities = df_county['city'].unique()
    city = st.selectbox('Select City', cities, index=0)

    street = st.text_input("Street")

    st.write(f"You selected {street} st. in {city} city in {county} county, {state} state.")
        
    description = st.text_area("Description of the Accident")
    severity = st.selectbox("Severity", ["1", "2", "3", "4", "5"])


    # Form to submit a report
    with st.form("report_form"):
        submitted = st.form_submit_button("Submit")

    if submitted:
        # Save to MongoDB
        report = {
            "Street": street,
            "City": city,
            "County": county,
            "State": state,
            "description": description,
            "severity": severity,
        }
        #reports_collection.insert_one(report) #to insert to mongodb
        st.success("Report submitted successfully!")



