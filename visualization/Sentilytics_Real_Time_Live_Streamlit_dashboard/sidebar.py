import streamlit as st

def sidebar_button(label, icon):
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(f"<div style='font-size:24px;'>{icon}</div>", unsafe_allow_html=True)
    with col2:
        if st.button(f"{label}", use_container_width=True):
            st.session_state.page = label
    
    st.markdown("---")