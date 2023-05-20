
import streamlit as st
import pandas as pd
import interactive_dashboard as id
import modeling as pred
import sdg_data_analytics as da
import get_data as gd



def selected_trend(trend_options, df: pd.DataFrame):
    if trend_options == 'Current Analytics':
        da.main(df)
    elif trend_options == 'Future Analytics':
        pred.get_future_trend_par()



def display_team():
    st.sidebar.markdown('''
    ---
    Created by the Data Demystifiers Team.
    ''')
    st.sidebar.write("---\n")

def display_main_menu_sidebar():
    # Create the sidebar
    st.sidebar.header('Dashboard `version 1`')
    st.sidebar.markdown("---")

    st.sidebar.subheader('Functionality of choice:')
    options = ['Interactive Dashboard', 'Trends', 'Text Model']
    selected_options = st.sidebar.selectbox('', options) 
    return selected_options


def main_layout(df: pd.DataFrame):    
    
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    
    # st.title("Visualization for SA SDG Hub")
    selected_options = display_main_menu_sidebar()
    if selected_options == "Interactive Dashboard":
        st.sidebar.write('Text to analyze', '''
        It was the best of times, it was the worst of times, it was
        the age of wisdom, it was the age of foolishness, it was
        the epoch of belief, it was the epoch of incredulity, it
        was the season of Light, it was the season of Darkness, it
        was the spring of hope, it was the winter of despair, (...)
        ''')
        st.sidebar.markdown(':green[$\sqrt{x^2+y^2}=1$] is a Pythagorean identity. :pencil:\\')
        id.main(df)
        # display_team()
    elif selected_options == "Trends":
        st.sidebar.markdown("---")
        st.sidebar.subheader('Select Trend Option')
        trend_options = ['Current Analytics', 'Future Analytics']
        selected_trend_options = st.sidebar.selectbox("", trend_options)
        selected_trend(selected_trend_options, df)
    elif selected_options == "Text Model'":
        st.sidebar.markdown("---")
        # Add your code for Option 3 here
        pass

    display_team()



if __name__ == "__main__":
    # st.set_page_config(layout="wide")
    st.set_page_config(layout='wide', initial_sidebar_state='expanded')
    # id.main()
    df = gd.processData()
    main_layout(df)
    