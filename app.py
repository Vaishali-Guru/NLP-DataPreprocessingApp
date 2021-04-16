import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from functions import *

logo = Image.open('logo.png')

st.set_page_config(page_title = 'NLP-Data Preprocessing App', page_icon = logo, layout = 'wide')

_, col1, _ = st.beta_columns(3)

with col1:
    st.title('NLP-Data Preprocessing App')

c1 = st.beta_expander('App Description: ', expanded = True)

with c1:
    st.markdown('Get preprocessed and cleaned textual data instantly with NLP-Data Preprocessing App! It is a NLP based Data Cleaning App build on Python using Streamlit!')

st.write('\n')

upload_file()