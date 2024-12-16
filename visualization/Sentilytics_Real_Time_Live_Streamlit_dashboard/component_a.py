import streamlit as st
from Visualisation.sentiment_distribution import display_sentiment_distribution
from Visualisation.comments_volume_chart import generate_comments_volume_chart
from Visualisation.trends import generate_trends_chart
from Visualisation.utilsFront import get_date_and_sentiment_inputs
from Visualisation.top_comments import generate_top_commented_likes
from Visualisation.wordcloud_component import wordcloud_component
from Visualisation.trends_area import generate_trends_area_chart
from Visualisation.density_heatmap import compare_platforms_component
from Visualisation.counts import counts


def component_a():
    placeholder = st.empty()

    with placeholder.container():
        st.title("Historical Data Dashboard")
        start_date, end_date, sentiment = get_date_and_sentiment_inputs()
        
        counts(start_date, end_date, sentiment)


        fig_col1, fig_col2 = st.columns(2) 

        with fig_col1:
            st.subheader("Volume of Comments by Source")
            generate_comments_volume_chart(start_date, end_date, sentiment)

        with fig_col2:
            st.subheader("Sentiment Density by Date")
            compare_platforms_component(start_date, end_date, sentiment)
        generate_trends_chart(start_date, end_date, sentiment)
        #display_sentiment_distribution(start_date, end_date, sentiment)
        generate_top_commented_likes(start_date, end_date, sentiment)
        wordcloud_component(start_date, end_date, sentiment)
