import streamlit as st

def get_date_and_sentiment_inputs():
    col1, col2, col3 = st.columns(3)

    with col1:
        start_date = st.date_input("Select Start Date", value="2020-01-01")
    with col2:
        end_date = st.date_input("Select End Date", value="2025-01-01")
    with col3:
        sentiment = st.selectbox("Select a Sentiment Type", 
                                 ["positive", "negative", "neutral", "all"], index=3)

    return start_date, end_date, sentiment
