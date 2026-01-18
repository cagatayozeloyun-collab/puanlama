import streamlit as st
import pandas as pd
import time
import random

# --- 1. TASARIM VE STİL AYARLARI ---
st.set_page_config(page_title="YTÜ CİNGEN OYLAMA", layout="wide")

# CSS kodunu triple-quote hatalarını önlemek için en güvenli şekilde yazıyoruz
st.markdown("""
<style>
    .main { background-color: #0e1117; color: #ffffff; }
    .main-title {
        color: #e63946; text-align: center; font-family: 'Arial Black', sans-serif;
        font-size: 45px !important; font-weight: 900; margin-bottom: 30px;
        text-transform: uppercase; text-shadow: 2px 2px 10px rgba(230, 57, 70, 0.5);
    }
    .item-header { color: #e63946; font-size: 35px; font-weight: bold; text-transform: uppercase; margin-bottom: 15px; }
    .jury-text-box {
        font-size: 18px; font-weight: bold; margin-bottom: 8px;
        border-left: 5px solid #e63946; padding-left: 15px; background: #1a1c24;
        padding-top: 8px; padding-bottom: 8px; border-radius: 5px;
    }
    .live-rank-balon {
        background-color: #e63946; color: white; padding: 20px;
        border-radius: 15px; text-align: center; font-size: 32px;
        font-weight: 900; margin-top: 20px; box-shadow: 0 0 15px rgba(230,57,70,0.6);
        text-transform: uppercase;
    }
    .stTable { font-size: 18px !important; }
    th { background-color: #e63946 !important; color: white !important; font-size: 20px
