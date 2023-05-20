
import streamlit as st

import get_data as gd
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio


def overall_analysis(df):
    col1, col2 =  st.columns([1, 2])

    with col1:
        locations = df["location"].unique().tolist()
        locations.insert(0, "All")  # Add "All" option to the dropdown
        selected_location = st.selectbox("Select Country", locations)

    with col2:
        # Define options for the multi-select dropdown
        institute = df["institute"].unique().tolist()
        # Display the multi-select dropdown
        selected_institutes = st.multiselect('Select institution', institute)
        # st.write(selected_institutes)
    
    col3, col4 =  st.columns([2,1])
    with col3:
        # Define options for the multi-select dropdown
        type = df["type"].unique().tolist()
        # Display the multi-select dropdown 
        selected_type = st.multiselect('Select publications', type)

    with col4:
        # Define options for the multi-select dropdown
        sdg = df["sdg"].unique().tolist()
        # Display the multi-select dropdown 
        selected_sdgs = st.multiselect('Select sdg category', sdg)

    filtered_loc = filtered_location(selected_location, df)
    st.write(build_sdg_loc_figure(filtered_loc))

    # Filter dataframe based on selected countries
    filtered_sdg_loc = filtered_location(selected_location, df)
    st.write(build_sdg_by_year_loc(filtered_sdg_loc))

    # Filter dataframe based on selected countries
    filtered_inst = filtered_institution(selected_institutes, df) #df[df['institute'].isin(selected_institutes)]
    st.write(build_sdg_by_year_inst(filtered_inst))

    # Filter dataframe based on selected countries
    filtered_type = filtered_publications(selected_type, df) #df[df['institute'].isin(selected_institutes)]
    st.write(build_sdg_by_year_type(filtered_type))

    # # Filter dataframe based on selected countries
    # filtered_sdg = filtered_sdg_categories(selected_sdgs, df) #df[df['institute'].isin(selected_institutes)]
    # st.write(build_sdg_by_year(filtered_sdg))

        
def independent_analysis(df):
    locations_t2 = df["location"].unique().tolist()
    locations_t2.insert(0, "All")  # Add "All" option to the dropdown
    selected_location_t2 = st.selectbox("Select Country ", locations_t2)   
    col1, col2 = st.columns(2)
    with col1:
        filtered_loc_t2 = filtered_location(selected_location_t2, df)
        st.write(build_sdg_loc_figure(filtered_loc_t2))
    with col2:
        # Filter dataframe based on selected countries
        filtered_sdg_loc_t2 = filtered_location(selected_location_t2, df)
        st.write(build_sdg_by_year_loc(filtered_sdg_loc_t2))

    # Define options for the multi-select dropdown
    institute_t2 = df["institute"].unique().tolist()
    # Display the multi-select dropdown
    selected_institutes_t2 = st.multiselect('Select institution ', institute_t2)
    # Filter dataframe based on selected countries
    filtered_inst_t2 = filtered_institution(selected_institutes_t2, df)
    st.write(build_sdg_by_year_inst(filtered_inst_t2))

    # Define options for the multi-select dropdown
    type_t2 = df["type"].unique().tolist()
    # Display the multi-select dropdown 
    selected_type_t2 = st.multiselect('Select publications ', type_t2)
    # Filter dataframe based on selected countries
    filtered_type_t2 = filtered_publications(selected_type_t2, df)
    st.write(build_sdg_by_year_type(filtered_type_t2))

    # Define options for the multi-select dropdown
    sdg_t2 = df["sdg"].unique().tolist()
    # Display the multi-select dropdown 
    selected_sdgs_t2 = st.multiselect('Select sdg category ', sdg_t2)
    # Filter dataframe based on selected countries
    filtered_sdg_t2 = filtered_sdg_categories(selected_sdgs_t2, df)
    st.write(build_sdg_by_year(filtered_sdg_t2))



def filtered_location(selected_location, small_dataset):
    # Filter the data based on the selected location
    if selected_location != "All":
        filtered_df = small_dataset[small_dataset["location"] == selected_location]
    else:
        filtered_df = small_dataset
    return filtered_df

def filtered_institution(selected_inst, small_dataset):
    if not selected_inst:
        filtered_inst = small_dataset
    else:
        filtered_inst = small_dataset[small_dataset['institute'].isin(selected_inst)]
    return filtered_inst

def filtered_publications(selected_type, small_dataset):
    if not selected_type:
        filtered_type = small_dataset
    else:
        filtered_type = small_dataset[small_dataset['type'].isin(selected_type)]
    return filtered_type

def filtered_sdg_categories(selected_sdgs, small_dataset):
    if not selected_sdgs:
        filtered_sdg = small_dataset
    else:
        filtered_sdg = small_dataset[small_dataset['sdg'].isin(selected_sdgs)]
    return filtered_sdg


def build_sdg_loc_figure(df: pd.DataFrame) -> go.Figure:
    order = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17']
    return px.histogram(
        df,
        x="sdg", 
        color='location',
        # histfunc='sum',
        category_orders={'sdg': order},
        title='Count of sdgs per country'
        # height=800,
    )

def build_sdg_by_year_loc(df: pd.DataFrame) -> go.Figure:
    grouped_df = df.groupby(['year', 'location'], as_index=False)['sdg'].count()
    return px.bar(
        grouped_df, 
        x='year', 
        y='sdg', 
        color='location', 
        title='Count of sdgs by year and country'
    )

def build_sdg_by_year_inst(df: pd.DataFrame) -> go.Figure:
    grouped_df = df.groupby(['year', 'institute'], as_index=False)['sdg'].count()
    return px.bar(
        grouped_df, 
        x='year', 
        y='sdg', 
        color='institute', 
        title='Count of sdgs by year and institution'
    )
    
def build_sdg_by_year_type(df: pd.DataFrame) -> go.Figure:
    grouped_df = df.groupby(['year', 'type'], as_index=False)['sdg'].count()
    return px.bar(
        grouped_df, 
        x='year', 
        y='sdg', 
        color='type', 
        title='Count of sdgs by year and publication type'
    )

def build_sdg_by_year(df: pd.DataFrame) -> go.Figure:
    grouped_df = df.groupby(['year'], as_index=False)['sdg'].count()
    return px.bar(
        grouped_df, 
        x='year', 
        y='sdg', 
        color='sdg', 
        title='Count of sdgs by year'
    )
    




def main(df):
    st.header("Current Analysis of the SDG")
    st.info("""Select the following options:\\
        Overall analysis to make analysis on all selected input parameters for all display.\\
        Independent analysis to make analysis on each input parameter for each display.
    """)

    t1, t2 = st.tabs(["Overall analysis", "Independent analysis"])
    with t1:
        overall_analysis(df)
    with t2:
        independent_analysis(df)
    # st.write(build_sdg_loc_figure(df))
    # st.write(build_sdg_by_year_loc(df))
    # st.write(build_sdg_by_year_inst(df))
    # st.write(build_sdg_by_year_type(df))
    # st.write(build_sdg_by_year(df))