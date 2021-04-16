import streamlit as st
import pandas as pd
import numpy as np
import html
import unidecode
import contractions
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

# nltk.download()
en_stopwords = stopwords.words('english')
lemmatizer = WordNetLemmatizer()

# Function to convert the text to lowercase
def tolower(text):
    text = text.lower()
    return text

# Function to unescape HTML characters - (&amp - &, &lt - <, etc)
def unescape_htmlcharacters(text):
    text = html.unescape(text)
    return text

# Function to remove accented characters
def remove_accentedcharacters(text):
    text = unidecode.unidecode(text)
    return text

# Function to expand contracted words - (i'll - i will, you're - you are, etc)
def expand_contractions(text):
    text = contractions.fix(text)
    return text

# Function to remove stopwords
def remove_stopwords(text):
    text = ' '.join(word for word in text.split() if not word in en_stopwords)
    return text

# Function to perform word lemmatization - standardizing the words
def lemmatization(text):
    text = ' '.join(lemmatizer.lemmatize(word) for word in text.split())
    return text

# Function to remove website urls/links
def remove_urls(text):
    text = re.sub(r'(http|www)\S+', '', text)
    return text

# Function to remove mentions/usernames - @usernames
def remove_mentions(text):
    text = re.sub('@[^\s]+', '', text)
    return text

# Function to remove email addresses
def remove_emailaddresses(text):
    text = re.sub('[\w\._]+@[\w\.-]+', '', text)
    return text

# Function to remove punctuations and special characters
def remove_specialcharacters(text):
    text = re.sub('[^A-Za-z0-9]+', ' ', text)
    return text

# Function to remove digits and numbers
def remove_digits(text):
    text = re.sub('\d+', '', text)
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
                df[f'{col}_cleaned'] = df[f'{col}_cleaned'].dropna().apply(lambda x: unescape_htmlcharacters(x))
                df[f'{col}_cleaned'] = df[f'{col}_cleaned'].dropna().apply(lambda x: remove_accentedcharacters(x))
                df[f'{col}_cleaned'] = df[f'{col}_cleaned'].dropna().apply(lambda x: expand_contractions(x))
                df[f'{col}_cleaned'] = df[f'{col}_cleaned'].dropna().apply(lambda x: remove_stopwords(x))
                df[f'{col}_cleaned'] = df[f'{col}_cleaned'].dropna().apply(lambda x: lemmatization(x))
                df[f'{col}_cleaned'] = df[f'{col}_cleaned'].dropna().apply(lambda x: remove_urls(x))
                df[f'{col}_cleaned'] = df[f'{col}_cleaned'].dropna().apply(lambda x: remove_mentions(x))
                df[f'{col}_cleaned'] = df[f'{col}_cleaned'].dropna().apply(lambda x: remove_emailaddresses(x))
                df[f'{col}_cleaned'] = df[f'{col}_cleaned'].dropna().apply(lambda x: remove_specialcharacters(x))
                df[f'{col}_cleaned'] = df[f'{col}_cleaned'].dropna().apply(lambda x: remove_digits(x))

            st.dataframe(df.head(10))

            st.balloons()