#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import json
import streamlit as st
import unicodedata


# In[3]:


pip install matplotlib


# In[4]:


from matplotlib import pyplot as plt


# In[3]:


from mplsoccer import Pitch


# In[4]:


pitch = Pitch(pitch_type='wyscout')  # example plotting an Opta/ Stats Perform pitch
fig, ax = pitch.draw()


# In[5]:


games_dict = {
    '29/5. Provincial - UribeFC 1:0': '3794687'}


# In[6]:


games_list = list(games_dict.keys())
games_id_list = list(games_dict.values())


# In[9]:


st.set_page_config(page_title='Uribe Futbol Stats', page_icon=':soccer:', initial_sidebar_state='expanded')


# In[14]:


st.sidebar.markdown('## Select Football Game')
menu_game = st.sidebar.selectbox('Select Game', games_list, index=0)
st.sidebar.markdown("""Here you can select one of 15 football games from the UEFA Euro 2020 knockout stage: """)


# In[15]:


menu_game


# In[24]:


uribe_df = pd.read_excel("C:/Users/Mauricio/Desktop/SEMIF.xlsx")


# In[25]:


uribe_df


# In[21]:


uribe_df['jugador'] = uribe_df['jugador'].astype(str)
uribe_df['jugador'] = uribe_df['jugador'].apply    (lambda val: unicodedata.normalize('NFC', val).encode('ascii', 'ignore').decode('utf-8'))
uribe_df['jugador'] = uribe_df['jugador'].replace('nan', np.nan)


# In[26]:


team_1 = uribe_df['team'].unique()[0]
mask_1 = uribe_df.loc[uribe_df['team'] == team_1]
player_names_1 = mask_1['jugador'].dropna().unique()


# In[30]:


acciones = ['Pase', 'Remate', 'Perdida', 'Recuperacion']


# In[32]:


st.sidebar.markdown('## Selecciona Jugador y accion')
menu_team = st.sidebar.selectbox('Selecciona equipo', (team_1))
menu_team == team_1
menu_player = st.sidebar.selectbox('Selecciona Jugador', player_names_1)
menu_activity = st.sidebar.selectbox('Selecciona Accion', acciones)
st.sidebar.markdown('Select a player and activity. Statistics plot will appear on the pitch.')


# In[34]:


st.title('Football Game Stats')
st.markdown("""
The knockout phase of UEFA Euro 2020 took place between 26 June 2021 and 11 July 2021. It consisted of 
15 matches between 16 teams successfully qualified from the group stage. In the final game in London Italy 
won England on penalty kicks and took the trophy second time in their history.
""")
st.write("""* Use dropdown-menus on the left side to select a game, team, player, and activity. 
Statistics plot will appear on the pitch below.""")
st.write('###', menu_activity, 'map')
st.write('###### Game:', menu_game)
st.write('###### Player:', menu_player, '(', menu_team, ')')


# In[1]:


def pass_map():
    df_pass = uribe_df.loc[(uribe_df['jugador'] == menu_player) & (uribe_df['accion'] == 'Pase')]
    location = df_pass['X1'].tolist()
    pass_end_location = df_pass['Y1'].tolist()
    color = 'blue' if menu_team == team_1 else 'red'
    if menu_team == team_1:
        x1 = np.array([el[0] for el in location])
        y1 = pitch_height-np.array([el[1] for el in location])
        x2 = np.array([el[0] for el in pass_end_location])
        y2 = pitch_height-np.array([el[1] for el in pass_end_location])
    else:
        x1 = pitch_width-np.array([el[0] for el in location])
        y1 = np.array([el[1] for el in location])
        x2 = pitch_width-np.array([el[0] for el in pass_end_location])
        y2 = np.array([el[1] for el in pass_end_location])
    u = x2-x1
    v = y2-y1
    ax.quiver(x1, y1, u, v, color=color, width=0.003, headlength=4.5)
    return ax


# In[ ]:




