import streamlit as st
import pandas as pd
import numpy as np

# Function to convert the text to lowercase
def tolower(text):
    text = text.lower()
    return text

# Function to upload the file
def upload_file():

    inp_file = st.file_uploader('Upload a CSV file: ', type = ['csv'], key = 'input_file')

    if(inp_file):
        st.success('File uploaded successfully')
        df = pd.read_csv(inp_file)
        st.dataframe(df.head(10))

        cat_cols = list(set(list(df.select_dtypes(include = ['object']).columns)))
        st.write(f"Selected Categorical Columns: **{', '.join(cat_cols)}**")

        _, col1, _ = st.beta_columns([2, 1, 2])

        with col1:
            inp_btn = st.button('Preprocess Data', key = 'start')

        if inp_btn:
            for col in cat_cols:
                df[f'{col}_cleaned'] = df[col].dropna().apply(lambda x: tolower(x))

            st.dataframe(df.head(10))

            st.balloons()