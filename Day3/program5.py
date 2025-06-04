import streamlit as st
import pandas as pd
import numpy as np

st.title('My first app')
st.write('Welcome to my first app on Streamlit!')

# load the dataframe
# df = pd.read_csv('./Salary_Data.csv')
# st.write(df)

# map_data = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#     columns=['lat', 'lon'])

# st.map(map_data)

# get text input from user
text_input = st.text_input("Enter your name")
if text_input:
    st.write('Hello, ', text_input)

# get address from user
address = st.text_area("Enter your address")
if address:
    st.write('Your address is: ', address)

# get date from user
date = st.date_input("Enter your date of birth")
if date:
    st.write('Your date of birth is: ', date)

# get user prompt
prompt = st.chat_input("Enter your prompt")
if prompt:
    st.write('You entered: ', prompt)