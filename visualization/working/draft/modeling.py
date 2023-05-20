import numpy as np
import pickle as pk
import streamlit as st
import time


def trend_prediction(loc_int, loc_sa, year, sdg):
    loaded_xgb_loc_model = pk.load(open("../../../../src/models/trend_model_loc.sav", 'rb'))
    if year <= 2018:
        st.write("Select year greater than 2018")
    else:
        input_data = [loc_int, loc_sa, year, sdg]
        input_data_numpy = np.asarray(input_data)
        input_data_reshaped = input_data_numpy.reshape(1,-1)

        prediction = loaded_xgb_loc_model.predict(input_data_reshaped)
    return prediction


def get_future_trend_par():
    st.header("Future Analysis of the SDG")
    international = st.text_input("International:")
    south_african = st.text_input("South African:")
    year = st.text_input("Year of publication:")
    sdg = st.text_input("SDG category number:")
    trend_pred = ''
    # create a button for prediction
    if st.button("Trend Prediction"):
        trend_pred = trend_prediction(int(international), int(south_african), int(year), int(sdg))
        with st.spinner('predicting, Wait for it...'):
            time.sleep(1)
        # if isValid:
        st.success(trend_pred, icon="✅")
        st.balloons()
       
    # st.error('This is an error', icon="🚨")

    # st.info('This is a purely informational message', icon="ℹ️")