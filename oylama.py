import streamlit as st
import pandas as pd
import time
import random

# --- SAYFA AYARLARI VE KARANLIK TEMA ---
st.set_page_config(page_title="MR.WHITE Racing - Reveal", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #e63946; color: white; border: none; font-weight: bold; height: 3em; }
    .car-header { color: #e63946; font-size: 45px; text-align: center; font-weight: bold; text-transform: uppercase; margin: 20px 0; border-bottom: 2px solid #e63946; }
    .jury-score-box { background-color: #1a1c24; padding: 15px; border-radius: 10px; border-left: 5px solid #e63946; margin: 10px 0; text-align: center; }
    .rank-info { background-color: #262730; padding: 25px; border-radius: 15px; text-align: center; border: 1px solid #e63946; font-size: 22px; margin-top: 15px; }
    h1, h2 { text-align: center; color: #e63946; font-family: 'Arial Black', sans-serif; }
    .stTable { background-color: #1a1c24; border-radius: 10px; }
    </style>
    """, unsafe_allow_index=True)

# --- SABİTLER ---
F1_POINTS = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

# --- SESSION STATE (VERİ YÖNETİMİ) ---
if 'all_votes' not in st.session_state:
    st.session_state.all_votes = []
if 'cars' not in st.session_state:
    # Varsayılan ikonik modeller
    st.session_state.cars = ["Ferrari F40", "BMW M5 E39", "McLaren F1", "Porsche 911 GT3 RS", "Lancia Delta Integrale", "Nissan GT-R R34"]

# --- SIDEBAR: YÖNETİM ---
with st.sidebar:
    st.header("⚙️ Garaj Yönetimi")
    new_car = st.text_input("Listeye Yeni Araba Ekle:")
    if st.button("Ekle") and new_car:
        st.session_state.cars.append(new_car)
        st.rerun()
    
    st.divider()
    if st.button("Tüm Verileri Sıfırla"):
        st.session_state.all_votes = []
        st.rerun()

st.title("🏎️ MR.WHITE RACING: THE REVEAL")

# --- 1. ADIM: GİZLİ OYLAMA ---
st.subheader("🗳️ Jüri Oylama Paneli")
with st.container():
    col1, col2 = st.columns([1, 2])
    with col1:
        voter_name = st.text_input("Jüri Adı:", placeholder="İsminizi girin...")
    with col2:
        selected_order = st.multiselect(
            "Arabaları En İyiden En Kötüye Doğru Sıralayın:", 
            st.session_state.cars, 
            default=st.session_state.cars
        )

    if st.button("Oyu Sisteme Gönder (Gizli)"):
        if voter_name and len(selected_order) == len(st.session_state.cars):
            st.session_state.all_votes.append({"voter": voter_name, "order": selected_order})
            st.success(f"Teşekkürler {voter_name}, oyların kaydedildi!")
            time.sleep