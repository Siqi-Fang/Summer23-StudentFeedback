import pandas as pd
import requests
import logging
import os
import plotly.express as px
import streamlit as st


EMAIL = st.secrets["EMAIL"]
PASSWORD = st.secrets["PASSWORD"]
# TODO: remeber to finish this map !!!!!
# also handles if DSIs change track ? 
NAME_2_TRACK = {
    "pixel-penguins": "One Week DS (EST)",
    "algorithmic-armadillos": "One Week DS (PST)",
    "cyborg-cheetahs": "One Week GameDev (PST)",
}

class MetabaseService:
    '''
    Generic Metabase service class
    '''

    def __init__(self):
        self.session = requests.Session()
        self.logger = logging.getLogger('discord-bot')

    def retrieve_data(self, response):
        request_data_response = response
        request_data = request_data_response.json().get('data')
        request_rows = request_data.get('rows')

        request_columns_raw = request_data.get('cols')
        request_columns = []
        for request_column in request_columns_raw:
            request_columns.append(request_column.get('display_name'))

        request_database = pd.DataFrame(request_rows, columns=request_columns)

        return request_database

    def retrieve(self, id):
        """id is the number in the url of the metabase question you created
           ..../question/<id>/your-question-name
           returns a pandas dataframe
        """
        self.login()
        request_data_response = self.session.post(
            f'https://data.ai-camp.dev/api/card/{id}/query')
        request_database = self.retrieve_data(request_data_response)
        return request_database

    def login(self):
        '''
        Logs into metabase and stays logged in while the session is alive
        '''
        json = {
            'username': EMAIL,
            'password': PASSWORD 
        }
        response = self.session.post(
            'https://data.ai-camp.dev/api/session', json=json)
        if response.status_code == 200:
            token = response.json().get('id')
            self.logger.info(
                'Metabase login successful, new token created and saved')
        else:
            self.logger.error(f'Metabase login failed: {response.text}')


service = MetabaseService()

service.login()

# gets average overall rating
# avg_rating_overall = df_avg_rating_overall.iloc[0][0]
# print(f`Avg rating of today is {avg_rating_overall:.2f}'')


def create_data(service, rating_type=0):
    """rating type = 0 -> returns df of cumulative rating
        rating type = 1 -> raturns df of todays rating 
    """
    if rating_type == 0:
        df_rating = service.retrieve(633)
    else:
        df_rating = service.retrieve(634)
    # retrieve student info data
    df_class_student = service.retrieve(635)

    df = pd.merge(df_rating, df_class_student,
                  on='discord_id', how='inner')

    df['track'] = df['name'].map(NAME_2_TRACK)

    return df

def pie_rating_count(df):
    """returns pie chart of rating count
        pass the appropriate df (prob better remove title and add it with strm UI)
    """
    rating_counts = df['rating'].value_counts()

    fig_rating_counts = px.pie(rating_counts, values=rating_counts.values,
                           names=rating_counts.index, title='2023 Summer Camp Rating Breakdown')

    return fig_rating_counts

def bar_rating_by_class(df):
    rating_by_class = df.groupby('name')['rating'].mean().reset_index()


    # Create a bar plot using Plotly Express
    fig_rating_by_class = px.bar(
        rating_by_class, x='name', y='rating', title='2023 Summer Camp Avg Rating by Class')

    # Display the chart
    return fig_rating_by_class

def timeseries_rating(df):
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    rating_by_date = df.groupby('date')['rating'].mean().reset_index()

    fig_rating_by_date = px.line(rating_by_date, x='date', y='rating',
                                title='2023 Summer Camp Avg Rating Each Day', range_x=['2023-06-05', '2023-09-01'])
    #fig_rating_by_date.update_traces(mode='lines+markers+text', text=df['rating'])
    return fig_rating_by_date
