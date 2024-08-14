import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from visualize.maputils import add_color_to_data
from utils.transform import sort_df
import plotly.express as px


@st.cache_data
def load(datasources_path, data, selected_column="rating"):
    df = (
        pd.read_csv(f"{datasources_path}/{data}")
        if data
        else pd.DataFrame(
            {
                "id": [0],
                "rating": [0],
                "userRatingCount": [0],
                "longitude": [0],
                "latitude": [0],
                "types": [0],
            }
        )
    )

    elevation_scale = 10 if selected_column == "userRatingCount" else 300
    
    if selected_column == "scaledUserRatingCount":
        df["scaledUserRatingCount"] = np.log(df["userRatingCount"])
        sorted_df = sort_df(df, selected_column, selected_column)
    else:
        sorted_df = sort_df(df, selected_column)

    add_color_to_data(df, selected_column, [255, 255, 0], [200, 255, 0], [0, 255, 0])

    # Define the layer
    layer = pdk.Layer(
        "ColumnLayer",
        df,
        get_position=["longitude", "latitude"],
        get_elevation=selected_column,
        elevation_scale=elevation_scale,  # Adjust scale as needed
        radius=200,  # Adjust radius as needed
        get_fill_color="color",
        pickable=True,
        auto_highlight=True,
    )

    # Define the view
    view_state = pdk.ViewState(
        latitude=df["latitude"].mean(),
        longitude=df["longitude"].mean(),
        zoom=1 if not data else 10,
        pitch=45,
    )
    tooltip = {
        "html": "{" + selected_column + "} <br/>",
        "style": {
            "backgroundColor": "steelblue",
            "color": "black",
        },
    }

    # Render the deck
    r = pdk.Deck(
        layers=[layer],
        tooltip=tooltip,
        initial_view_state=view_state,
        map_style=pdk.map_styles.LIGHT,
    )

    # Display in Streamlit
    st.pydeck_chart(r)

    if data:
        fig = px.bar(sorted_df, x="id", y=selected_column)
        st.plotly_chart(fig)
        st.dataframe(sorted_df)
