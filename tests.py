import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st
from urllib.request import urlopen
import streamlit.components.v1 as components
import json
cliend_id="100009"
action="predict"
API_url = "http://127.0.0.1:5000/"
#API_url += action + "/" + cliend_id
print(API_url)



API_explain_url = API_url + "explain" + "/" + cliend_id

explain_response = urlopen(API_explain_url)
if st.button("Explain Results"):
    components.html(exp.as_html(), height=800)
