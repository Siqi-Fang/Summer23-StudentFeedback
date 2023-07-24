import requests
import logging
import math

import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


EMAIL = st.secrets["EMAIL"]
PASSWORD = st.secrets["PASSWORD"]
# TODO: remeber to finish this map !!!!!
# also handles if DSIs change track ? 
TRACKS = ["One Week DS (EST)",
          "One Week DS (PST)",
          "One Week GameDev (EST)",
          "One Week GameDev (PST)",
          "3-Week DS (EST)",
          "3-Week DS (PST)",
          "3-Week CV (EST)",
          "3-Week CV (PST)",
          "3-Week NLP (EST)",
          "3-Week NLP (PST)",
          ]
NAME_2_TRACK = {
 "pixel-penguins": "One Week DS (EST)",
    "algorithmic-armadillos": "One Week DS (PST)",
    "cyborg-cheetahs": "One Week GameDev (PST)",
    "galactic-goblins": "3-Week NLP (EST)",
    "crystal-cyclones": "3-Week NLP (EST)",
    "delta-droids": "3-Week NLP (EST)",
    "energy-emperors": "3-Week NLP (EST)",
    "binary-breakers": "3-Week NLP (EST)",
    "twilight-titans": "3-Week NLP (EST)",
    "lunar-lasers": "3-Week NLP (EST)",
    "turbo-tornadoes": "3-Week CV (EST)",
    "vector-vipers": "3-Week CV (EST)",
    "diamond-dragons": "3-Week CV (EST)",
    "comet-crusaders" :"3-Week CV (EST)",
    "mystic-moons": "3-Week CV (EST)",
    "electron-elephants": "3-Week DS (EST)",
    "kepler-koalas": "3-Week DS (EST)",
    "solar-squirrels": "3-Week DS (EST)",

    "web-wolves": "One Week DS (EST)",
    "protocol-parrots": "One Week DS (EST)",
    "network-nighthawks": "One Week GameDev (EST)",
    "server-snakes": "One Week GameDev (EST)",

    "silicon-starlings": "One Week DS (PST)",
    "firewall-flamingos": "One Week DS (PST)",
    "overclock-owls": "One Week GameDev (PST)",
    "photon-phoenixes": "3-Week NLP (PST)",
    "helix-hawks": "3-Week NLP (PST)",
    "matrix-mustangs": "3-Week NLP (PST)",
    "fusion-flamingos": "3-Week NLP (PST)",
    "omega-otters": "3-Week NLP (PST)",
    "cyberspace-cheetahs": "3-Week CV (PST)",
    "jetstream-jaguars": "3-Week CV (PST)",
    "vortex-vultures": "3-Week CV (PST)",
    "data-dolphins": "3-Week CV (PST)",
    "lumen-lemurs": "3-Week CV (PST)",
    "spectrum-stingrays": "3-Week DS (PST)",
    "kilobit-koalas": "3-Week DS (PST)",
    "radiant-ravens": "3-Week DS (PST)",
    "fractal-firebirds": "3-Week DS (PST)",

    "agile-antelopes": "One Week DS (EST)",
    "brawny-beavers": "One Week DS (EST)",
    "crimson-crocodiles": "One Week GameDev (EST)", 
    "dynamic-dolphins": "One Week DS (PST)",

    "majestic-meerkats": "One Week GameDev (PST)",
    "whimsical-wolves": "One Week DS (PST)",
    "zesty-zebras": "One Week DS (PST)",
    "bubbly-butterflies": "One Week GameDev (EST)",
    "vivacious-vultures": "One Week DS (EST)",
    "whirlwind-walruses": "One Week GameDev (EST)",
    "stellar-stingrays": "One Week DS (EST)",
# BATCH B
    "crazy-centipedes": "One Week DS (EST)",

    "resilient-raccoons": "3-Week DS (EST)",
    "humble-hedgehogs": "3-Week DS (EST)",
    "openminded-octopuses": "3-Week DS (EST)",

    "passionate-pigeons": "3-Week DS (PST)",
    "wandering-woodpeckers": "3-Week DS (PST)",
    "dynamic-dalmations": "3-Week DS (PST)",
    "intelligent-irukandji": "3-Week DS (PST)",
    "witty-wombats": "3-Week DS (PST)",
    "quirky-quesadillas": "3-Week DS (PST)",

    "fabulous-flamingos": "3-Week NLP (EST)",
    "jolly-jackrabbits": "3-Week NLP (EST)",
    "lovely-llamas": "3-Week NLP (EST)",
    "peaceful-pandas": "3-Week NLP (EST)",
    "sensible-seahorses":"3-Week NLP (EST)",
    "harmonic-hawks": "3-Week NLP (EST)",
    "joyous-jackals": "3-Week NLP (EST)",
    "noteworthy-nuthatches": "3-Week NLP (EST)",

    "sincere-swallows": "3-Week NLP (PST)",
    "mystical-manatees": "3-Week NLP (PST)",
    "gentle-giraffes": "3-Week NLP (PST)",
    "fabulous-fajitas": "3-Week NLP (PST)",
    "proud-porcupines":"3-Week NLP (PST)",

    "gleeful-geese": "3-Week CV (EST)",
    "merry-mockingbirds": "3-Week CV (EST)",
    "cheerful-cheetahs": "3-Week CV (EST)",
    "ambitious-aardvarks": "3-Week CV (EST)",
    "dapper-dingoes": "3-Week CV (EST)",

    "feist-finches": "3-Week CV (PST)",
    "lovable-lobsters": "3-Week CV (PST)",
    "curious-caterpillars": "3-Week CV (PST)",
    "brilliant-butterflies": "3-Week CV (PST)",
    "radiant-roadrunners": "3-Week CV (PST)",
    #B2
    "unforgettable-udon": "One Week DS (EST)",
    "magnificent-macaroons": "One Week DS (EST)",
    "daring-dumplings":"One Week DS (EST)",
    "happy-hamburgers": "One Week DS (PST)",
    "bountiful-bagels": "One Week DS (PST)",
    "toasty-tangerine":"One Week DS (PST)",
    # B3
    "hungry-hashbrowns": "One Week DS (EST)",
    "jolly-jalapenos": "One Week GameDev (EST)",
    "whimsical-watermelons": "One Week DS (PST)",
    "giggly-gummybears": "One Week GameDev (EST)",

    # BATCH C 
    'fury-falcons': "Expert Course (EST)",
    'roaring-ravens': "Expert Course (EST)",
    'valkyrie-vipers': "Expert Course (PST)",
    'cyclone-cougars' :"Expert Course (PST)",
    'silver-spartans': "Expert Course (PST)", 
    'monarch-mammoths': "One Week DS (PST)",
    'magical-macaronis': "3-Week NLP (PST)",
    'swift-swans': "3-Week DS (PST)",
    'remarkable-ravioli': "3-Week DS (PST)",
    'prismatic-piccolos': "3-Week CV (PST)",
    'marvelous-mangos': "3-Week CV (PST)",
    'tuneful-trombones': "3-Week NLP (PST)",
    'mystical-mandolins': "3-Week NLP (PST)",
    'quality-quesadillas': "3-Week CV (PST)",
    'legendary-lasagnas': "3-Week CV (PST)",
    'laughing-llamas': "3-Week CV (PST)",
    'rhythmic-recorders': "3-Week NLP (PST)", 
    'curious-chickens': "3-Week NLP (EST)",
    'bouncing-blueberries': "3-Week NLP (EST)",
    'sweet-strawberries': "3-Week NLP (EST)",
    'amazing-avocados': "3-Week CV (EST)",
    'charming-cherries': "3-Week CV (EST)",
    'fearless-flamingos': "3-Week CV (EST)",
    'exquisite-eclairs': "3-Week CV (EST)",
    'astonishing-almonds': "3-Week DS (EST)",
    'tasty-tacos': "3-Week DS (EST)",
    'bold-badgers': "3-Week DS (EST)",
    'energetic-emus': "3-Week NCV (EST)",
    "keen-kiwis": "3-Week NLP (EST)",
    'generous-grapefruits': "3-Week NLP (EST)",
}

CURRENT_CLASSES = [
    'fury-falcons',
    'roaring-ravens',
    'valkyrie-vipers',
    'cyclone-cougars',
    'silver-spartans',
    "keen-kiwis",
    'generous-grapefruits',
    'monarch-mammoths',
    'tasty-tamales',
    'magical-macaronis',
    'swift-swans',
    'remarkable-ravioli',
    'prismatic-piccolos',
    'marvelous-mangos',
    'tuneful-trombones',
    'mystical-mandolins',
    'quality-quesadillas',
    'legendary-lasagnas',
    'laughing-llamas',
    'rhythmic-recorders',
    'curious-chickens',
    'bouncing-blueberries',
    'sweet-strawberries',
    'amazing-avocados',
    'charming-cherries',
    'fearless-flamingos',
    'exquisite-eclairs',
    'astonishing-almonds',
    'tasty-tacos',
    'bold-badgers',
    'energetic-emus',
]

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


def create_data(service, rating_type=0):
    """rating type = 0 -> returns df of cumulative rating
        rating type = 1 -> raturns df of todays rating 
    """
    if rating_type == 0:
        df_rating = service.retrieve(639)
    else:
        df_rating = service.retrieve(638)
    # retrieve student info data
    df_class_student = service.retrieve(640)

    df = pd.merge(df_rating, df_class_student,
                  on='discordId', how='inner')

    df['track'] = df['name'].map(NAME_2_TRACK)

    df = df[df['track'].notna()]

    return df

def pie_rating_count(df):
    """returns pie chart of rating count
        pass the appropriate df (prob better remove title and add it with strm UI)
    """
    rating_counts = df['rating'].value_counts()

    fig_rating_counts = px.pie(rating_counts, values=rating_counts.values,
                           names=rating_counts.index, title='2023 Summer Camp Rating Breakdown')

    return fig_rating_counts

def bar_rating_by_class(df, overall):
    if overall == 1:
        rating_by_class = df.groupby('name')['rating'].mean().reset_index()
    else:
        temp = df.groupby('name')['rating'].mean().reset_index()
        rating_by_class = temp[temp['name'].isin(CURRENT_CLASSES)]

    # Create a bar plot using Plotly Express
    fig_rating_by_class = px.bar(
        rating_by_class, x='name', y='rating', title='2023 Summer Camp Overall Rating by Class')

    fig_rating_by_class.update_layout(
        height=500,
        xaxis={'categoryorder': 'total ascending'})
    # Display the chart
    return fig_rating_by_class

def timeseries_rating(df):
    rating_by_date = df.groupby('date')['rating'].mean().reset_index()
    count_by_date = df.groupby('date')['rating'].count().reset_index()

    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=("2023 Summer Camp Daily Avg Rating",
                        "2023 Summer Camp Number of Ratings Recieved"),
        shared_xaxes=True,)

    fig.add_trace(go.Scatter(x=rating_by_date['date'], y=rating_by_date['rating']),
                1, 1)
    fig.add_trace(go.Scatter(x=count_by_date['date'], y=count_by_date['rating']),
                2, 1)

    fig.update_layout(height=500, width=700,
                    showlegend=False,
                    xaxis_tickformat="%d-%m",
                    xaxis_range=['2023-06-05', '2023-09-01'],
                    )
    fig.update_xaxes(
        rangebreaks=[dict(bounds=["sat", "mon"])])
    
    return fig

def rating_by_date_class(df, overall):
    """Takes the overall df as input"""
    if overall == 1:
        classes = df['name'].unique()
    else:
        classes = CURRENT_CLASSES
    total_num_of_classes = len(classes)
    COL_PER_ROW = 3
    num_of_rows = math.ceil(total_num_of_classes/COL_PER_ROW)

    fig = make_subplots(
        rows=num_of_rows, cols=COL_PER_ROW,
        subplot_titles=classes,
        #shared_xaxes=True,
    )

    for i, c in enumerate(classes):
        calss_avg_rating = df[df['name'] == c].groupby('date')['rating'].mean().reset_index()
        fig.add_trace(go.Bar(x=calss_avg_rating['date'], y=calss_avg_rating['rating']),
                      i//COL_PER_ROW+1, i % COL_PER_ROW+1)

    fig.update_layout(height=1800, width=700,
                        title_text="2023 Summer Camp Daily Avg Rating",
                        showlegend=False,
                      )
    return fig


def rating_by_date_track(df):
    tracks = df['track'].unique()
    print(tracks)
    total_num_of_tracks = len(tracks)
    COL_PER_ROW = 3
    num_of_rows = math.ceil(total_num_of_tracks/COL_PER_ROW)

    fig = make_subplots(
        rows=num_of_rows, cols=COL_PER_ROW,
        subplot_titles=tracks,
        #shared_xaxes=True,
    )

    for i, c in enumerate(tracks):
        rating = df[df['track'] == c]
        avg_rating = rating.groupby('date')['rating'].mean().reset_index()
        fig.add_trace(go.Bar(x=avg_rating['date'], y=avg_rating['rating']),
                        i//3+1, i % 3+1)

    fig.update_layout(height=700, width=700,
                    title_text="2023 Summer Camp Daily Avg Ratings",
                    showlegend=False)
    
    return fig
        
