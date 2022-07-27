import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import seaborn as sns

def df_chain_explain(df, cat):
    '''Ecrit une chaine de caractéres permettant d\'expliquer l\'influence des features dans le résultat de l\'algorithme '''
    if cat == 'positif':
        chaine = '### Principales caractéristiques contribuantes ###  \n'
    else:
        chaine = '### Principales caractéristiques discriminantes ###  \n'

    for feature in df['feature'].values:

        chaine += '### Caractéristique : ' + str(feature) + '###  \n'
        chaine += '* **Prospect : **' + str(df[df['feature'] == feature]['customer_values'].values[0])
        chaine_discrim = ' (seuil de pénalisation : ' + str(df[df['feature'] == feature]['signe'].values[0]) + ' '
        chaine_discrim += str(df[df['feature'] == feature]['val_lim'].values[0]) + ')'

        if cat == 'negatif':
            chaine += '<span style=\'color:red\'>' + chaine_discrim + '</span>  \n'
        else:
            chaine += '<span style=\'color:green\'>' + chaine_discrim + '</span>  \n'

    return chaine


def graphes_streamlit(df, cat):
    '''A partir du df, affichage un subplot de 6 graphes représentatif du client comparé à d'autres clients sur 6 features'''
    f, ax = plt.subplots(2, 3, figsize=(10, 10), sharex=False)
    plt.subplots_adjust(hspace=0.5, wspace=0.5)

    i = 0
    j = 0
    liste_cols = ['Client', 'global', 'En Règle', 'En défaut']
    for feature in df['feature'].values:

        sns.despine(ax=None, left=True, bottom=True, trim=False)
        sns.barplot(
            y=df[df['feature'] == feature][['customer_values', 'moy_global', 'moy_en_regle', 'moy_defaut']].values[0],
            x=liste_cols,
            ax=ax[i, j])
        sns.axes_style("white")

        if len(feature) >= 18:
            chaine = feature[:18] + '\n' + feature[18:]
        else:
            chaine = feature
        if cat == 'negatif':
            chaine += '\n(pénalise le score)'
            ax[i, j].set_facecolor('#ffe3e3')  # contribue négativement
            ax[i, j].set_title(chaine, color='#990024')
        else:
            chaine += '\n(améliore le score)'
            ax[i, j].set_facecolor('#e3ffec')
            ax[i, j].set_title(chaine, color='#017320')

        if j == 2:
            i += 1
            j = 0
        else:
            j += 1
        if i == 2:
            break
    for ax in f.axes:
        plt.sca(ax)
        plt.xticks(rotation=45)
    if i != 2:  # cas où on a pas assez de features à expliquer (ex : 445260)
        True
    st.pyplot()

    return True

def fo_chart(proba):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=proba,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "probability of payment", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [None, 1], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 0.2], 'color': 'red'},
                {'range': [0.2, 0.4], 'color': 'orange'},
                {'range': [0.4, 0.6], 'color': 'yellow'},
                {'range': [0.6, 1], 'color': 'green'}],
            'threshold': {
                'line': {'color': "grey", 'width': 4},
                'thickness': 0.75,
                'value': proba}}))

    fig.update_layout(paper_bgcolor="lavender", font={'color': "darkblue", 'family': "Arial"})

    return fig


