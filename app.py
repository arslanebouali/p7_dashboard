# utils
from PIL import Image
from random import randint

# streamlit

#from streamlit.session_state import get_session_state
from streamlit import session_state


import streamlit as st
from pages.page00 import api_response,get_clients


clients= get_clients()
image = Image.open("img.png")
#Chargement des données


#-----------------------------------------
#   Head
#-----------------------------------------

# Main title
def main_page():

    title ='<h1 style="font-size: 4rem; color: #826d8c"">Prêt à dépenser</h1>'
    st.markdown(title, unsafe_allow_html=True)

    # Add session state
    if 'key' not in st.session_state:
        st.session_state['key'] =  str(randint(1000, 100000000))

    st.image(Image.open("clip-1089.png"))
#-----------------------------------------
#   Sidebar
#-----------------------------------------

# logo

st.sidebar.image(image)

# Title of Sidepage
title ='<h1 style="font-size: 1.1rem; color: #826d8c""> Choose a page </h1>'
st.sidebar.markdown(title, unsafe_allow_html=True)



selected_page=st.sidebar.selectbox("please select option",options=["","client_base","fill form"])

if selected_page=="client_base":
    api_response()
elif selected_page=="":
    main_page()














