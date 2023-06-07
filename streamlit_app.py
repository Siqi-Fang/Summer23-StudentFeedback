from collections import namedtuple
import altair as alt
import pandas as pd
import streamlit as st
import plotly.express as px
from utils import create_data, MetabaseService, pie_rating_count

"""
Data Preprocessing 
"""

st.title('Summercamp 2023 Student Feedback & Ratings')

# log in to metabase 
service = MetabaseService()
service.login()

# get the data
df_avg = create_data(service, 0)
fig_avg_rating = pie_rating_count(df_avg, 0)
#df_today = create_data(service, 1)

avg_rating_overall = 8.9
st.write("The average rating of today is {}".format(avg_rating_overall))
st.plotly_chart(fig_avg_rating, theme="streamlit", use_container_width=True)

