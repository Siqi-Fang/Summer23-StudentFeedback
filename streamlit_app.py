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
#df_today = create_data(service, 1)

# ==== NUMEBRS ====
avg_score_overall = df_overall['rating'].mean()
#avg_score_today = df_today['rating'].mean()

# ==== FIGS ====
fig_avg_rating_overall = pie_rating_count(df_overall)
fig_rating_by_class_overall = bar_rating_by_class(df_overall)
fig_rating_overtime = timeseries_rating(df_overall)
fig_rating_by_class_by_date = rating_by_date_class(df_overall)

# ==== DASHBOARD ====
#st.write("The average rating of today is {}".format(avg_score_today))
st.write("The average rating of 2023 Summer Camp is {0:.{1}f}".format(
    avg_score_overall, 2))

st.plotly_chart(fig_avg_rating_overall, theme="streamlit",
                use_container_width=True)
st.plotly_chart(fig_rating_by_class_overall, theme="streamlit",
                use_container_width=True)
st.plotly_chart(fig_rating_overtime, theme="streamlit",
                use_container_width=True)
st.plotly_chart(fig_rating_by_class_by_date, theme="streamlit",
                use_container_width=True)
