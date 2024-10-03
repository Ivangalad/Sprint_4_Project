''' This file reads vehicles_us.csv containing the car sales data, cleans it up, 
    produces plotly figures, and then shows them on streamlit.
    It requires the vehicles_us.csv file in the same folder to run.
    '''

import streamlit as st
import pandas as pd
import plotly.express as px

# Read in data
car_df = pd.read_csv('vehicles_us.csv')

# Clean up data

car_df['model_year'] = car_df.groupby('model')['model_year'].transform(lambda x: x.fillna(x.median())) #Fill model year nulls with median year by model 
car_df['model_year'] = car_df['model_year'].astype('int')

car_df['cylinders'] = car_df.groupby('model')['cylinders'].transform(lambda x: x.fillna(x.median()))
car_df['cylinders'] = car_df['cylinders'].astype('int')

car_df['odometer'] = car_df.groupby(['model_year'])['odometer'].transform(lambda x: x.fillna(x.median()))
car_df['odometer'] = car_df['odometer'].fillna(car_df[car_df['model'] == 'ford f-150']['odometer'].median()).astype('int') #One null required special treatment

car_df['paint_color'] = car_df['paint_color'].fillna('unlisted')

car_df['is_4wd'] = car_df['is_4wd'].fillna(0).astype('int64')

#This is old preprocessing
#car_df['model_year'] = car_df['model_year'].fillna(1).astype('int64') 
#car_df['cylinders'] = car_df['cylinders'].fillna(1).astype('int64')
#car_df['odometer'] = car_df['odometer'].fillna(-1).astype('int64')
#car_df['paint_color'] = car_df['paint_color'].fillna('unlisted')
#car_df['is_4wd'] = car_df['is_4wd'].fillna(0).astype('int64')

# Slice DataFrames by model year, cut out low price values
old_car_df = car_df.loc[(car_df['model_year'] < 1960) & (car_df['price'] >= 500)]
muscle_car_df = car_df.loc[(car_df['model_year'] >= 1960) & (car_df['model_year'] < 1980) & (car_df['price'] >= 500)]
pre_new_car_df = car_df[(car_df['model_year'] >= 1980) & (car_df['model_year'] < 2000) & (car_df['price'] >= 500)]
new_car_df = car_df[(car_df['model_year'] >= 2000) & (car_df['price'] >= 500)]

#Group by paint color and make
old_car_group = old_car_df.groupby(['paint_color', 'make'])['model'].count().reset_index()
old_car_group.columns = ['paint_color', 'make', 'count']

muscle_car_group = muscle_car_df.groupby(['paint_color', 'make'])['model'].count().reset_index()
muscle_car_group.columns = ['paint_color', 'make', 'count']

pre_new_car_group = pre_new_car_df.groupby(['paint_color', 'make'])['model'].count().reset_index()
pre_new_car_group.columns = ['paint_color', 'make', 'count']

new_car_group = new_car_df.groupby(['paint_color', 'make'])['model'].count().reset_index()
new_car_group.columns = ['paint_color', 'make', 'count']

# Create Plotly Figures
old_car_hist = px.bar(old_car_group.sort_values(['paint_color', 'make']), 
                      x='paint_color', 
                      y='count', 
                      color='make', 
                      title='Number of Cars of Each Color, 1900-1959')

old_car_scat = px.scatter(old_car_df.sort_values(['paint_color', 'make']), 
                          x='paint_color', 
                          y='price', 
                          color='make', 
                          title='Listed Price in USD vs Color, 1900-1959')

muscle_car_hist = px.bar(muscle_car_group.sort_values(['paint_color', 'make']), 
                         x='paint_color', 
                         y='count', 
                         color='make', 
                         title='Number of Cars of Each Color, 1960-1979')

muscle_car_scat = px.scatter(muscle_car_df.sort_values(['paint_color', 'make']), 
                             x='paint_color', 
                             y='price', 
                             color='make', 
                             title='Listed Price in USD vs Color, 1960-1979')

pre_new_car_hist = px.bar(pre_new_car_group.sort_values(['paint_color', 'make']), 
                          x='paint_color', 
                          y='count', 
                          color='make', 
                          title='Number of Cars of Each Color, 1980-1999')

pre_new_car_scat = px.scatter(pre_new_car_df.sort_values(['paint_color', 'make']), 
                              x='paint_color', 
                              y='price', 
                              color='make', 
                              title='Listed Price in USD vs Color, 1980-1999')

new_car_hist = px.bar(new_car_group.sort_values(['paint_color', 'make']), 
                      x='paint_color', 
                      y='count', 
                      color='make', 
                      title='Number of Cars of Each Color, 2000-2019')

new_car_scat = px.scatter(new_car_df.sort_values(['paint_color', 'make']), 
                          x='paint_color', 
                          y='price', 
                          color='make', 
                          title='Listed Price in USD vs Color, 2000-2019')

#Make webpage showing figures with streamlit
st.header('Car Sales, Their Prices and Colors, By Generation', divider='rainbow')

old_car_box = st.checkbox('1900-1959')
muscle_car_box = st.checkbox('1960-1979')
pre_new_car_box = st.checkbox('1980-1999')
new_car_box = st.checkbox('2000-2019')

if old_car_box:
    st.plotly_chart(old_car_hist)
    st.plotly_chart(old_car_scat)

if muscle_car_box:
    st.plotly_chart(muscle_car_hist)
    st.plotly_chart(muscle_car_scat)

if pre_new_car_box:
    st.plotly_chart(pre_new_car_hist)
    st.plotly_chart(pre_new_car_scat)

if new_car_box:
    st.plotly_chart(new_car_hist)
    st.plotly_chart(new_car_scat)