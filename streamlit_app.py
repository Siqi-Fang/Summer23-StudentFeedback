from collections import namedtuple
import altair as alt
import pandas as pd
import streamlit as st
import plotly.express as px
from utils import create_data, MetabaseService, pie_rating_count, bar_rating_by_class, \
                    timeseries_rating, rating_by_date_class

st.title('Summercamp 2023 Student Feedback & Ratings')

# log in to metabase 
service = MetabaseService()
service.login()

# ==== LOAD DATA ====
df_overall = create_data(service, 0)
df_overall['date'] = pd.to_datetime(df_overall['date'])
df_overall['date'] = df_overall['date'].dt.strftime('%Y-%m-%d')
df_today = create_data(service, 1)

# ==== NUMEBRS ====
avg_score_overall = df_overall['rating'].mean().round(2)
avg_score_today = df_today['rating'].mean().round(2)
num_resp_today = df_today['rating'].count()

# ==== FIGS ====
fig_avg_rating_overall = pie_rating_count(df_overall)
fig_rating_by_class_overall = bar_rating_by_class(df_overall)
fig_rating_overtime = timeseries_rating(df_overall)
fig_rating_by_class_by_date = rating_by_date_class(df_overall)

# ==== DASHBOARD ====
#st.write("The average rating of today is {}".format(avg_score_today))
col1, col2, col3 = st.columns(3)
col1.metric("Overall Rating", avg_score_overall)
col2.metric("Todays Rating", avg_score_today)
col3.metric("Feedback Received Today", num_resp_today)

st.plotly_chart(fig_avg_rating_overall, theme="streamlit",
                use_container_width=True)
st.plotly_chart(fig_rating_overtime, theme="streamlit",
                use_container_width=True)

numbers, text = st.tabs(["📈 Ratings", "🗃 Qualitative Feedback"])

numbers.subheader("Ratings")
numbers.plotly_chart(fig_rating_by_class_overall, theme="streamlit",
                use_container_width=True)
numbers.plotly_chart(fig_rating_by_class_by_date, theme="streamlit",
                use_container_width=True)

text.subheader("Text feedback")
text.write("TBD")

