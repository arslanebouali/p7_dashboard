# Libraries
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st
from urllib.request import urlopen
from pages.Utils.graph import  *
import streamlit.components.v1 as components


import json

def api_response( ):
    st.set_option('deprecation.showPyplotGlobalUse', False)
    clients=get_clients()
    client_id = st.selectbox(label="chose client by id", options=clients)
    API_url = "http://127.0.0.1:5000/"
    API_predict_url = API_url + "predict" + "/" + client_id
    API_explain_url = API_url + "explain" + "/" + client_id
    API_df_maps_url = API_url + "df_maps" + "/" + client_id


    if "select" in API_predict_url:
        st.write("select an existing_id")
    else:
        with st.spinner('Loading of client informations...'):

            print(API_predict_url)
            json_url = urlopen(API_predict_url)

            API_predict_data = json.loads(json_url.read())
            predict_response = API_predict_data
            probas = predict_response.get('proba')
            prediction = predict_response.get('prediction ')
            # Affichage du résultat en roouge ou vert en fonction du client
            if probas[0][0] > 0.5:

                    st.markdown('<font color="green">{}{}</font>'.format('Client peu risqué, avec une probabilité de ',
                                                                         probas[0][0]), unsafe_allow_html=True)
            else:
                    st.markdown('<font color="red">{}{}</font>'.format('Client risqué, avec une probabilité de ',
                                                                       probas[0][0]), unsafe_allow_html=True)
            st.plotly_chart(fo_chart(probas[0][0]))
            if st.button("explication") :
                print("button pressed")
                st.subheader("Caractéristiques influençant le score")


                print(API_explain_url)

                explain_response = urlopen(API_explain_url)

                components.html(explain_response.read(),height=200)

            if st.button("consulter profil")  :
                with st.spinner('Loading of more client informations...'):
                    print("button pressed")
                    json_url = urlopen(API_df_maps_url)
                    API_maps_data = json.loads(json_url.read())
                    negatif_map = API_maps_data.get("filtered_neg")
                    positif_map = API_maps_data.get("filtered_plus")

                    explanation_neg = pd.read_json(negatif_map)
                    explanation_pos = pd.read_json(positif_map)

                    st.markdown("### Top 6 des Caractéristiques qui contribue à l'accord du prêt ###")
                    st.markdown(df_chain_explain(explanation_pos, cat="positif"), unsafe_allow_html=True)
                    # graphe
                    # Affichage des graphes
                    graphes_streamlit(explanation_pos, cat='positif')

                    st.subheader("Définition des groupes")
                    st.markdown("\
                            \n\
                            * Client : la valeur pour le client considéré\n\
                            * En Règle : valeur moyenne pour l'ensemble des clients en règle\n\
                            * En Défaut : valeur moyenne pour l'ensemble des clients en défaut\n\
                            ")

                    st.markdown("### Top 6 des Caractéristiques qui s'oppose à l'accord du prêt ###")
                    st.markdown(df_chain_explain(explanation_neg, cat="negatif"), unsafe_allow_html=True)
                    # graphe
                    # Affichage des graphes
                    graphes_streamlit(explanation_neg, cat='negatif')

                    st.subheader("Définition des groupes")
                    st.markdown("\
                            \n\
                            * Client : la valeur pour le client considéré\n\
                            * En Règle : valeur moyenne pour l'ensemble des clients en règle\n\
                            * En Défaut : valeur moyenne pour l'ensemble des clients en défaut\n\
                            ")







@st.cache
def get_clients():
    # empty list to read list from a file
    clients = []

    # open file and read the content in a list
    with open(r'data/clients.txt', 'r') as fp:
        for line in fp:
            # remove linebreak from a current name
            # linebreak is the last character of each line
            x = line[:-1]

            # add current item to the list
            clients.append(x)

    # display list
    return(clients)





