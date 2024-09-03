import streamlit as st 
import pandas as pd 

st.title("Cek Group nya ")

df = pd.read_csv("ios_processing.csv")
df["datetime_baru"] = pd.to_datetime(df["datetime_baru"])

df["tanggal"] = df["datetime_baru"].dt.date

dt = df.groupby(["tanggal"]).size().reset_index()
st.write(dt.describe())