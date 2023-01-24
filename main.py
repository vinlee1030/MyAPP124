import streamlit as st
from streamlit_option_menu import option_menu

# 1=sidebar menu, 2=horizontal menu, 3=horizontal menu w/ custom menu
EXAMPLE_NO = 1

with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu", #None
        options=["Home","Projects","Contact"],
        icons=["house","book","envelope"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical" #optional

    )
#st.title("My App")

if selected == "Home":
    st.title(f"*{selected}")
if selected == "Projects":
    st.title(f"*{selected}")
if selected == "Contact":
    st.title(f"*{selected}")