from collections import namedtuple
import altair as alt
import pandas as pd
import streamlit as st
import plotly.express as px
from utils import create_data, MetabaseService, pie_rating_count, bar_rating_by_class, \
    timeseries_rating, rating_by_date_class, rating_by_date_track
import math 

st.set_page_config(layout="wide") # needs to be the first call!
st.title('Summer Camp 2023 Student Feedback & Ratings')

# log in to metabase 
service = MetabaseService()
service.login()

# ==== LOAD DATA ====
df_overall = create_data(service, 0)
df_overall['date'] = pd.to_datetime(
    df_overall['date'], format='ISO8601').dt.date
df_today = create_data(service, 1)
df_qualitative = df_overall[["date", "comment", "rating", "studentUsername","name","track"]]
df_qualitative = df_qualitative.sort_values(by='date', ascending=False)
df_qualitative_today = df_today[["comment",
                                 "rating", "studentUsername", "name", "track"]]
# ==== NUMEBRS ====
avg_score_overall = round(df_overall['rating'].mean(), 2)
avg_score_today = round(df_today['rating'].mean(), 2)
num_resp_today = df_today['rating'].count()

# ==== FIGS ====
fig_avg_rating_overall = pie_rating_count(df_overall)
fig_rating_by_class_overall = bar_rating_by_class(df_overall, 1)
fig_rating_by_class_overall_curr = bar_rating_by_class(df_overall, 0)
fig_rating_overtime = timeseries_rating(df_overall)
fig_rating_by_class_by_date = rating_by_date_class(df_overall, 1)
fig_rating_by_class_by_date_curr = rating_by_date_class(df_overall, 0)
fig_rating_by_track_by_date = rating_by_date_track(df_overall)

# ==== DASHBOARD ====
col1, col2, col3 = st.columns(3)
col1.metric("Overall Rating", avg_score_overall)
col2.metric("Todays Rating", avg_score_today)
col3.metric("Feedback Received Today", num_resp_today)

cs, cb = st.columns([1, 3])
cs.plotly_chart(fig_avg_rating_overall, theme="streamlit",
                use_container_width=True)
cb.plotly_chart(fig_rating_overtime, theme="streamlit",
                use_container_width=True)
st.plotly_chart(fig_rating_by_track_by_date, theme="streamlit",
                use_container_width=True)


curr_ratings, past_ratings, today_text, text = st.tabs(
    ["📈 Batch B Ratings", "📈 All Ratings", "📅 Today's Feedback ", "🗃 All Feedback", ])

curr_ratings.subheader("Batch B Ratings")
curr_ratings.plotly_chart(fig_rating_by_class_overall_curr, theme="streamlit",
                          use_container_width=True)
curr_ratings.plotly_chart(fig_rating_by_class_by_date_curr, theme="streamlit",
                          use_container_width=True)


past_ratings.subheader("All Ratings")
past_ratings.plotly_chart(fig_rating_by_class_overall, theme="streamlit",
                          use_container_width=True)
past_ratings.plotly_chart(fig_rating_by_class_by_date, theme="streamlit",
                          use_container_width=True)


today_text.subheader("Todays Feedback")
today_text.dataframe(df_qualitative_today, hide_index=True)

text.subheader("All Feedback")
text.dataframe(df_qualitative,
               hide_index=True,)

