import streamlit as st
import pandas as pd
import plotly.express as px


def chart1(df_accidents, granularity, state=None, city=None):
    if granularity == "USA":
        filtered_df = df_accidents
    elif granularity == "State" and state:
        filtered_df = df_accidents[df_accidents["State"] == state]
    elif granularity == "City" and state and city:
        filtered_df = df_accidents[
            (df_accidents["State"] == state) & (df_accidents["City"] == city)
        ]
    else:
        raise ValueError("Invalid granularity or missing parameters for State/City.")

    filtered_df["Month"] = filtered_df["Start_Time"].dt.to_period("M")
    severity_counts = (
        filtered_df.groupby(["Month", "Severity"])
        .size()
        .reset_index(name="Accident_Count")
    )

    trend_counts = (
        filtered_df.groupby("Month").size().reset_index(name="Total_Accidents")
    )

    combined_data = pd.merge(
        severity_counts, trend_counts, on="Month", how="left"
    )

    combined_data["Month"] = combined_data["Month"].dt.to_timestamp()

    fig = px.bar(
        combined_data,
        x="Month",
        y="Accident_Count",
        color="Severity",
        labels={"Accident_Count": "Number of Accidents"},
        opacity=0.7,
        title=f"Monthly Accident Trends and Severity Levels ({granularity})",
    )

    fig.add_scatter(
        x=combined_data["Month"],
        y=combined_data["Total_Accidents"],
        mode="lines+markers",
        name="Total Accidents",
        line=dict(color="black", width=2),
    )

    fig.update_layout(
        barmode="stack",
        xaxis_title="Month",
        yaxis_title="Number of Accidents",
        legend_title="Legend",
        hovermode="x unified",
        height=600,
    )

    return fig

def chart2(df_accidents, granularity, state=None, city=None):
    if granularity == "USA":
        filtered_df = df_accidents
    elif granularity == "State" and state:
        filtered_df = df_accidents[df_accidents["State"] == state]
    elif granularity == "City" and state and city:
        filtered_df = df_accidents[
            (df_accidents["State"] == state) & (df_accidents["City"] == city)
        ]
    else:
        raise ValueError("Invalid granularity or missing parameters for State/City.")

    filtered_df["Year"] = filtered_df["Start_Time"].dt.year
    filtered_df["Month"] = filtered_df["Start_Time"].dt.month
    filtered_df["Year_Month"] = (
        filtered_df["Start_Time"].dt.to_period("M").astype(str)
    )  # Format: "YYYY-MM"

    weather_severity_counts = (
        filtered_df.groupby(["Year_Month", "Weather_Condition", "Severity"])
        .size()
        .reset_index(name="Accident_Count")
    )

    fig = px.bar(
        weather_severity_counts,
        x="Weather_Condition",
        y="Accident_Count",
        color="Severity",
        animation_frame="Year_Month",
        labels={
            "Weather_Condition": "Weather Condition",
            "Accident_Count": "Number of Accidents",
            "Severity": "Severity Level",
            "Year_Month": "Time (Year-Month)",
        },
        title=f"Monthly Accident Trends by Weather Condition and Severity ({granularity})",
    )

    fig.update_layout(
        barmode="stack",
        xaxis_title="Weather Condition",
        yaxis_title="Number of Accidents",
        legend_title="Severity",
        hovermode="x unified",
        xaxis=dict(tickangle=-45),
        height=600,
    )

    return fig


def chart3(df_accidents, granularity, state=None, city=None):
    if granularity == "USA":
        filtered_df = df_accidents
    elif granularity == "State" and state:
        filtered_df = df_accidents[df_accidents["State"] == state]
    elif granularity == "City" and state and city:
        filtered_df = df_accidents[
            (df_accidents["State"] == state) & (df_accidents["City"] == city)
        ]
    else:
        raise ValueError("Invalid granularity or missing parameters for State/City.")

    filtered_df["Year_Month"] = (
        filtered_df["Start_Time"].dt.to_period("M").astype(str)
    )  # Format: "YYYY-MM"

    fig = px.density_mapbox(
        filtered_df,
        lat="Start_Lat",
        lon="Start_Lng",
        z=None, 
        animation_frame="Year_Month",
        radius=10,
        mapbox_style="carto-positron",
        color_continuous_scale="inferno",
        title=f"Monthly Accident Density Map ({granularity})",
        labels={"Year_Month": "Time (Year-Month)"},
        center={"lat": filtered_df["Start_Lat"].mean(),
            "lon": filtered_df["Start_Lng"].mean(),},
        zoom=2.95 if granularity == "USA" else 5,
    )

    fig.update_layout(
        height=600,
        coloraxis_colorbar=dict(
            title="Density",
            thicknessmode="pixels",
            thickness=20,
            lenmode="fraction",
            len=0.5,
        ),
    )

    return fig


def chart4(df_accidents, granularity, state=None, city=None):
    if granularity == "USA":
        filtered_df = df_accidents
    elif granularity == "State" and state:
        filtered_df = df_accidents[df_accidents["State"] == state]
    elif granularity == "City" and state and city:
        filtered_df = df_accidents[
            (df_accidents["State"] == state) & (df_accidents["City"] == city)
        ]
    else:
        raise ValueError("Invalid granularity or missing parameters for State/City.")

    severity_colors = {
        1: "blue",
        2: "green",
        3: "yellow",
        4: "orange",
        5: "red",
    }
    
    filtered_df["Year_Month"] = (
        filtered_df["Start_Time"].dt.to_period("M").astype(str)
    )  # Format: "YYYY-MM"

    fig = px.scatter_mapbox(
        filtered_df,
        lat="Start_Lat",
        lon="Start_Lng",
        color="Severity",
        animation_frame="Year_Month",
        color_discrete_map=severity_colors,
        hover_data=["City", "State", "Severity", "Start_Time"],
        center={"lat": 37.0902, "lon": -95.7129},
        zoom=3 if granularity == "USA" else 5,
        title="Accidents by Severity",
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_center={
            "lat": filtered_df["Start_Lat"].mean(),
            "lon": filtered_df["Start_Lng"].mean(),
        },
        height=600,
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
    )

    return fig


def chart5(df_accidents, granularity, state=None, city=None):
    if granularity == "USA":
        filtered_df = df_accidents
    elif granularity == "State" and state:
        filtered_df = df_accidents[df_accidents["State"] == state]
    elif granularity == "City" and state and city:
        filtered_df = df_accidents[
            (df_accidents["State"] == state) & (df_accidents["City"] == city)
        ]
    else:
        raise ValueError("Invalid granularity or missing parameters for State/City.")

    road_types = [
        "Amenity", "Bump", "Crossing", "Give_Way", "Junction", "No_Exit", "Railway",
        "Roundabout", "Station", "Stop", "Traffic_Calming", "Traffic_Signal", "Turning_Loop"
    ]

    filtered_df["Year"] = pd.to_datetime(filtered_df["Start_Time"]).dt.year

    severity_road_counts = (
        filtered_df.groupby(["Year", "Severity"])[road_types]
        .sum()
        .reset_index()
    )

    severity_road_counts["Severity"] = severity_road_counts["Severity"].astype(str)

    df_heatmap = severity_road_counts.melt(
        id_vars=["Year", "Severity"],
        var_name="Road_Type",
        value_name="Accident_Count"
    )

    fig = px.density_heatmap(
        df_heatmap,
        x="Road_Type",
        y="Severity",
        z="Accident_Count",
        animation_frame="Year",
        color_continuous_scale="inferno",
        title=f"Yearly Impact of Road Types by Accident Severity ({granularity})",
        labels={
            "Road_Type": "Road Type",
            "Severity": "Accident Severity",
            "Accident_Count": "Number of Accidents",
            "Year": "Year"
        },
    )

    fig.update_layout(
        height=600,
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        xaxis_title="Road Types",
        yaxis_title="Severity",
        yaxis=dict(
            categoryorder="array",
            categoryarray=["1", "2", "3", "4", "5"],
        )
    )

    return fig


def chart6(df_accidents, granularity, state=None, city=None):
    if granularity == "USA":
        filtered_df = df_accidents
    elif granularity == "State" and state:
        filtered_df = df_accidents[df_accidents["State"] == state]
    elif granularity == "City" and state and city:
        filtered_df = df_accidents[
            (df_accidents["State"] == state) & (df_accidents["City"] == city)
        ]
    else:
        raise ValueError("Invalid granularity or missing parameters for State/City.")

    if filtered_df.empty:
        raise ValueError(
            f"No data available for the selected criteria: granularity={granularity}, state={state}, city={city}"
        )

    filtered_df["Hour"] = pd.to_datetime(filtered_df["Start_Time"]).dt.hour
    filtered_df["Year"] = pd.to_datetime(filtered_df["Start_Time"]).dt.year

    required_columns = ["Year", "Hour", "Severity"]
    for col in required_columns:
        if col not in filtered_df.columns:
            raise KeyError(f"Missing required column: {col}")

    hourly_severity = (
        filtered_df.groupby(["Year", "Hour", "Severity"])
        .size()
        .reset_index(name="Accident_Count")
    )

    hourly_severity["Severity"] = hourly_severity["Severity"].astype(str)

    fig = px.density_heatmap(
        hourly_severity,
        x="Hour",
        y="Severity",
        z="Accident_Count",
        animation_frame="Year",
        color_continuous_scale="inferno",
        labels={
            "Hour": "Hour of Day",
            "Severity": "Accident Severity",
            "Accident_Count": "Number of Accidents",
        },
        title=f"Daily Distribution of Accident Severities Each Year ({granularity})",
    )

    fig.update_layout(
        height=600,
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        xaxis=dict(tickmode="linear", dtick=1),
    )

    return fig