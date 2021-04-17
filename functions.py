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
import io
import base64

nltk.download('stopwords')
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

# Function to remove multiple(>2) repetitions of a single character in a word - (helloooooo - hello)
def standardize_words(text):
    text = re.sub(r'(.)\1{2,}', r'\1', text)
    return text

# Function to remove small words (words with 2 letter/characters or less)
def remove_smallwords(text):
    text = re.sub(r'\W*\b\w{1,2}\b', ' ', text)
    return text

# Function to remove extra whitespaces
def remove_extrawhitespaces(text):
    text = ' '.join(word.strip() for word in text.split())
    return text

# Function to upload the file
def upload_file():

    inp_file = st.file_uploader('Upload a CSV or Excel file: ', type = ['csv', 'xlsx', 'xls'], key = 'input_file')

    if(inp_file):
        ext = inp_file.name.split('.')[1]
        st.success('File uploaded successfully')

        if ext == 'csv':
            df = pd.read_csv(inp_file, encoding = 'ISO-8859-1')

        elif ext == 'xlsx':
            df = pd.read_excel(inp_file, engine = 'openpyxl')

        elif ext == 'xls':
            df = pd.read_excel(inp_file)
            
        st.dataframe(df.head(10))

        cat_cols = list(set(list(df.select_dtypes(include = ['object']).columns)))
        
        total_cols = len(cat_cols)
        num_cols = 2
        num_each_col = total_cols//num_cols

        st.write('Select the columns to preprocess: ')

        col1, col2 = st.beta_columns(num_cols)

        selected_cols = []
        for col in cat_cols[:num_each_col+1]:
            with col1:
                x = st.checkbox(f'{col}', value = True)
                selected_cols.append(x)
        
        for col in cat_cols[num_each_col+1:]:
            with col2:
                x = st.checkbox(f'{col}', value = True)
                selected_cols.append(x)

        current_selection = []
        for col, val in zip(cat_cols, selected_cols):
            if val == True:
                current_selection.append(col)
        
        st.write(f"Selected Categorical Columns: **{', '.join(current_selection)}**")

        e1 = st.beta_expander('Steps for using the App: ', expanded = True)
        with e1:
            st.markdown('1. Upload a CSV or Excel file to perform Data Cleaning on\n2. Tick the checkboxes to select the text columns to clean\n3. Click on Preprocess Data button to start data preprocessing\n4. See the sample of resultant dataset\n5. Click on Download File to download the resultant file')

        st.write('\n')

        _, col1, _ = st.beta_columns([2, 1, 2])

        with col1:
            inp_btn = st.button('Preprocess Data', key = 'start')

        if inp_btn:
            for col in current_selection:
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
                df[f'{col}_cleaned'] = df[f'{col}_cleaned'].dropna().apply(lambda x: standardize_words(x))
                df[f'{col}_cleaned'] = df[f'{col}_cleaned'].dropna().apply(lambda x: remove_smallwords(x))
                df[f'{col}_cleaned'] = df[f'{col}_cleaned'].dropna().apply(lambda x: remove_extrawhitespaces(x))

            st.dataframe(df.head(10))

            _, c1, _ = st.beta_columns([2, 1, 2])

            out_file = df.to_csv(index=False)
            b64 = base64.b64encode(out_file.encode()).decode()

            buffer = io.StringIO()
            df.info(verbose = False, memory_usage='deep', buf=buffer)
            df_info = buffer.getvalue()

            if 'MB' in df_info:
                size = int(buffer.getvalue().split(': ')[-1].split(' MB')[0].split('.')[0])
                if size > 50:
                    st.error(f'Output file of exceeded the file size limit of 50MB. Try uploading a smaller file in order to download the output file!')
                else:
                    with c1:
                        href = f'<a href="data:file/csv;base64,{b64}">Download File</a>'
                        st.markdown(href, unsafe_allow_html=True)
                        st.balloons()
            
            else:
                with c1:
                    href = f'<a href="data:file/csv;base64,{b64}">Download File</a>'
                    st.markdown(href, unsafe_allow_html=True)
                    st.balloons()