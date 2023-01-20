import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title='VGsales')
st.header('VG Sales across world')
st.subheader('Is the Dashboard clear')

## - Load dataframe

excel_file= 'vgsales.xlsm'
sheet_name = 'vgsales'

df= pd.read_excel(excel_file,sheet_name=sheet_name,usecols='A:K',
                header=0)
app = dash.Dash(__name__)
server = app.server
st.dataframe(df)

bar_chart = px.bar(df,title='North America Sales',
                   x='Year', y='North American Sales')

st.plotly_chart(bar_chart)

Genre = df['Genre'].unique().tolist()
Year = df['Year'].unique().tolist()

year_selection = st.slider('Year:', min_value=min(Year),
                           max_value=max(Year),
                           value=(min(Year),max(Year)))

genre_selection = st.multiselect('Genre:',
                                 Genre,
                                 default=Genre)

mask = (df['Year'].between(*year_selection)) & (df['Genre'].isin(genre_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_result}*')

df_grouped = df[mask].groupby(by=['Platform']).count()[['Year']]
df_grouped = df_grouped.rename(columns={'Year':'Period'})
df_grouped = df_grouped.reset_index()

bar_chart = px.bar(df_grouped,
                   x='Platform',
                   y='Period',
                   text='Period',
                   color_discrete_sequence=['#F63366']*len(df_grouped),
                   template='plotly_white')

st.plotly_chart(bar_chart)
