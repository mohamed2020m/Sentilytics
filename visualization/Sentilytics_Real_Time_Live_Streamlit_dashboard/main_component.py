import streamlit as st
import json
from streamlit_lottie import st_lottie

with open('animation.json', 'r') as f:
    animation = json.load(f)

def main_component():
    st.markdown("<h1 style='text-align: center;'>Feel the Pulse of the World ⚡</h1>", unsafe_allow_html=True)
    st.write("Dive deep into the global mood! Sentilytics uses real-time data from YouTube and The New York Times to analyze the world's sentiment. Discover trending topics, understand public opinion, and stay ahead of the curve.")

    animation_style = """
    <style>
        .centered-lottie {
            display: flex;
            justify-content: center;
            align-items: center;
        }
    </style>
    """
    st.markdown(animation_style, unsafe_allow_html=True)

    # Animation Lottie centrée
    st.markdown('<div class="centered-lottie">', unsafe_allow_html=True)
    st_lottie(animation, speed=1, height=900, width=1700, key="animation")
    st.markdown('</div>', unsafe_allow_html=True)
