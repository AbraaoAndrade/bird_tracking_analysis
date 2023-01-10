import streamlit as st



def about():
    
    if st.session_state.layout != "centered":
        st.session_state.layout = "centered"
        st.experimental_rerun()

    None