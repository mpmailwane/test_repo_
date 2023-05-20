import sys
# sys.path.append("/opt/anaconda3/lib/python3.9/site-packages")
sys.path.append("C:/Users/Phoebe/AppData/Local/Programs/Python/Python310/lib/site-packages")

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from streamlit_plotly_events import plotly_events
import plotly.io as pio
pio.templates.default = "plotly"

import get_data as gd



# render the processed data to the UI
def render_preview_ui(df: pd.DataFrame):
    with st.expander("Preview Data"):
        st.write(df)




def build_sdg_figure(df: pd.DataFrame) -> go.Figure:
    fig = px.histogram(
        df,
        x="sdg", 
        color="sdg",
        category_orders={'sdg':['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17']},
        # height=800,
    )
    return fig

def build_location_figure(df: pd.DataFrame) -> go.Figure:
    # # Count the occurrences of each category
    # category_counts = df['location'].value_counts()
    # # Create a pie chart using Plotly
    # fig = go.Figure(data=go.Pie(labels=category_counts.index, values=category_counts))
   
    # # Display the chart using Streamlit
    # return st.plotly_chart(fig)

    return px.histogram(
        df,
        x="location", 
        color="location",
        # height=400,
    )

def show_map(df: pd.DataFrame):
    return px.choropleth(
        df, 
        locations='location', 
        locationmode='country names', 
        color='location',
        title='Choropleth Map with "Other" Category',
        color_continuous_scale='Blues'
    )

def build_institute_figure(df: pd.DataFrame) -> go.Figure:
    return px.histogram(
        df,
        x="institute", 
        color="institute",
        # height=400,
    )

def build_publication_figure(df: pd.DataFrame) -> go.Figure:
    return px.histogram(
        df,
        x="type", 
        color="type",
        # height=400,
    )


def render_sdg_plotly_ui(df: pd.DataFrame) -> go.Figure:
    sdg_figure = build_sdg_figure(df)     

    sdg_clicked = plotly_events(
            sdg_figure,
            select_event=True,
    )
    st.write(sdg_clicked) 
    return sdg_clicked   


def render_other_plotly_ui(df: pd.DataFrame) -> go.Figure:
    location_figure = build_location_figure(df)
    institute_figure = build_institute_figure(df)
    publication_figure = build_publication_figure(df)

    c1, c2 = st.columns(2)     
    with c1:       
        st.subheader("Continental emissions since 1850")  
        location_clicked = plotly_events(
            location_figure,
            click_event=True,
        )
    with c2: 
        st.subheader("Continental emissions since 1850")  
        publication_clicked = plotly_events(
            publication_figure,
            click_event=True,
        )

    show_map(df)

    st.subheader("Continental emissions since 1850")  
    institute_clicked = plotly_events(
            institute_figure,
            click_event=True,
    )
    
    st.write(location_clicked)
    return location_clicked


def get_current_query(selected_par, df):
    current_query = {}
    if selected_par == 'sdg':        
        sdg_clicked = render_sdg_plotly_ui(df)
        current_query["sdg"] = {e1["x"] for e1 in sdg_clicked}    
    return current_query

def get_future_query(selected_par, df):
    current_query = {}
    if selected_par == "location":
        location_clicked = render_other_plotly_ui(df)
        current_query["location"] = {e1["x"] for e1 in location_clicked}
    return current_query

def initialize_state():
    for q in ["sdg", "location"]: #, "institute", "publication"]:
        if f"{q}" not in st.session_state:
            st.session_state[f"{q}"] = None #set()


def update_state(current_query: dict[str, set]):
    rerun = False
    for q in ["sdg"]: #, "location"]: #, "institute", "publication"]:
        if current_query[q] != st.session_state[q]:
            st.session_state[q] = current_query[q] 
            rerun = True

    if rerun:
        st.experimental_rerun()


def query_data(df: pd.DataFrame) -> pd.DataFrame:
    df["sdg"] = df["sdg"].astype(str)
    df["selected"] = True
    for q in ["sdg"]: #, "location"]: #, "institute", "publication"]:
        if st.session_state[f"{q}"]:
            df.loc[~df[q].isin(st.session_state[f"{q}"]), "selected"] = False
    return df  

def query_loc_data(df: pd.DataFrame) -> pd.DataFrame:
    df["location"] = df["location"].astype(str)
    df["selected"] = False
    for q in ["location"]: #, "location"]: #, "institute", "publication"]:
        st.write("q is:", q)
        if st.session_state[f"{q}"]:
            df.loc[df[q].isin(st.session_state[f"{q}"]), "selected"] = True
    return df  


def main(df):
    # Center-aligned header
    st.markdown(
        """
        <h1 style='text-align: center;'>SA SDG Dashboard </h1>
        """,
        unsafe_allow_html=True
    )
    initialize_state()
    
    # Create a container for the SDG's
    sdg_container = st.container()
    # Create a container for the second display (scatter plot)
    second_container = st.container()

    # Display the graph in the container1
    with sdg_container:
        sdg_container.write("This is inside the container")
        st.subheader("Continental emissions since 1850")
        st.info("An example of a Streamlit layout using columns")
        # second_container.empty()
        for q in ["sdg"]:#, "location"]:
            if q == "sdg":
                current_query = get_current_query(q, df)
                st.write(current_query)
                st.write("session status within sdg container")
                st.write(st.session_state)
                # Update the state if the query has changed
                if current_query[q] != st.session_state[q]:
                    update_state(current_query)
        # elif q == "location":
        #     current_query = get_future_query(q, df)
        #     st.write(current_query)
        #     st.write(st.session_state)
        #     if current_query[q] != st.session_state[q]:
        #         update_state(current_query)
    
    try:
        if st.session_state["sdg"]:
            # sdg_container.empty()
            st.write("session status for sdg")
            st.write(st.session_state)
            # selected_point = st.session_state
            transformed_df = query_data(df)
            # Create a new container for the bar chart
            with second_container:
                second_container.write("This is inside the container")
                st.subheader("Continental emissions since 1850")
                st.info("An example of a Streamlit layout using columns")
                selected_transformed_df = transformed_df[transformed_df['selected']==True]
                render_preview_ui(selected_transformed_df)
                render_other_plotly_ui(selected_transformed_df)

            
            # if st.session_state["location"]:
            #     # sdg_container.empty()
            #     st.write("session status for location")
            #     st.write(st.session_state)
            #     # selected_point = st.session_state["location"]
            #     transformed_loc_df = query_loc_data(selected_transformed_df)
            #     # Create a new container for the bar chart
            #     with second_container:
            #         for q in ["location"]:#, "location"]:
            #             if q == "location":
            #                 current_query = get_future_query(q, df)                        
            #                 # Update the state if the query has changed
            #                 if current_query[q] != st.session_state[q]:
            #                     update_state(current_query)
            #         st.write("current_query for location")
            #         st.write(current_query)
            #         st.write("session for sdg and loc")
            #         st.write(st.session_state)
            #         second_container.write("This is inside the container")
            #         selected_transformed_loc_df = transformed_loc_df[transformed_loc_df['selected']==True]
            #         render_preview_ui(selected_transformed_loc_df)
            #         render_other_plotly_ui(selected_transformed_loc_df)
    except Exception as e:
        st.error("An unexpected error occurred: " + st.exception(e)) # str(e)
        st.error('This is an error', icon="🚨")

    # Create the back button
    # if st.button('Back'):
    #     second_container.empty()
    #     # Reset the selected data and rerun the script
    #     # second_container.empty()
    #     st.write("I'm clicked")
    #     initialize_state()
    #     st.write(st.session_state["sdg"])
    #     # st.session_state = None
    #     st.write(st.session_state)
    #     # with sdg_container:
    #     #     second_container.empty()
    #     #     for q in ["sdg", "location"]:
    #     #         if q == "sdg":
    #     #             current_query = get_current_query(q, df)
    #     #             st.write(current_query)
    #     #             st.write(st.session_state)
    #     #             # Update the state if the query has changed
    #     #             if current_query[q] != st.session_state[q]:
    #     #                 update_state(current_query)
    #     st.experimental_rerun()
