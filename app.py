import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from functions import *

logo = Image.open('logo.png')

st.set_page_config(page_title = 'NLP-Data Preprocessing App', page_icon = logo, layout = 'wide')

st.title('NLP-Data Preprocessing App')

st.markdown('''Get preprocessed and cleaned text data instantly with NLP-Data Preprocessing App! It is a NLP based Data Cleaning 
App build on Python using Streamlit!''')

e1 = st.beta_expander('Steps for using the App: ', expanded = True)
with e1:
    st.markdown('''1. Upload a CSV or Excel file to perform Data Cleaning\n2. Tick the checkboxes to select the text columns to 
    preprocess\n3. Click on **Preprocess Data** button to start data preprocessing\n4. See the preview of output dataset\n5. Click on 
    **Download File** to download the output file (Provide the file extension as **.csv** while saving the output file)''')
    st.info('Download option is only available if the output file size is less than **50MB**')

st.write('\n')

e2 = st.beta_expander('Data Preprocessing Functions: ', expanded = False)
with e2:
    st.markdown('''1. Lowercase the text\n2. Remove common words/stopwords (e.g., as, in, the, etc.)\n3. Get all the words to root/base 
    form\n4. Remove website URLs\n5. Remove email addresses\n6. Remove usernames or mentions(e.g., @xyz)\n7. Remove special characters 
    and digits\n8. Expand contractions(e.g., i'll -> i will, i've -> i have, etc.)''')

st.write('\n')

upload_file()