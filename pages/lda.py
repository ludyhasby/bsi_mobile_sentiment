import streamlit as st
import pickle
from sklearn.feature_extraction.text import CountVectorizer

st.title("Latent Dirichlet Analysis")
# dataset = 

with open('lda_model.pkl', 'rb') as handle:
    lda = pickle.load(handle)

with open('cv.pkl', 'rb') as cv_file:
    cv = pickle.load(cv_file)

n = 15
for index, topic in enumerate(lda.components_):
    st.write(f'The top {n} words for topic #{index}')
    st.write([cv.get_feature_names_out()[i] for i in topic.argsort()[-n:]])