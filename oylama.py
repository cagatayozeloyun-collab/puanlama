import streamlit as st
import pandas as pd
import time
import random

# --- AYARLAR ---
st.set_page_config(page_title="YTÜ OYLAMA", layout="wide")

# CSS
css = """
<style>
.main { background-color: #0e1117; color: white; }
.baslik { color: #e63946; text-align: center; font-size: 40px; font-weight: 900; }
.isim { color: #e63946; font-size: 35px; font-weight: bold; text-align: center; }
.juri { padding: 8px; margin: 5px; background: #1a1c24; border-left: 5px solid #e63946; font-weight: bold; }
.sira-kutu { background: #e63946; color: white; padding: 15px; border-radius: 10px; text-align: center; font-size: 28px; font-weight: 900; margin-top: 15px; }
.stButton>button { width: 100%; background: #e63946; color: white; height: 3.5em; font-weight: bold; font-size: 18px; }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

F1 = {1: 25, 2: 18, 3:
