import streamlit as st
import pandas as pd
import time
import random

# --- SAYFA AYARI ---
st.set_page_config(page_title="YTÜ OYLAMA", layout="wide")

# --- CSS (Kısa Satırlar) ---
css = """
<style>
.main { background-color: #0e1117; color: white; }
.baslik { color: #e63946; text-align: center; font-size: 40px; font-weight: 900; }
.isim { color: #e63946; font-size: 30px; font-weight: bold; text-align: center; }
.juri { padding: 5px; margin: 5px; background: #1a1c24; border-left: 4px solid #e63946; }
.sira { background: #e63946; color: white; padding: 10px; border-radius: 10px; text-align: center; font-size: 25px; margin-top: 10px; }
.stButton>button { width: 100%; background: #e63946; color: white; height: 3em; }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- PUANLAR ---
P = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

# --- HAFIZA ---
if 'votes' not in st.session_state: st.session_state.votes = []
if 'comps' not in st.session_state: st.session_state.comps = {}

# --- SOL PANEL ---
with st.sidebar:
    st.header("PANEL")
    ad = st.text_input("ISIM:", key="s_ad")
    foto = st.file_uploader("FOTO:", type=['png','jpg','jpeg'], key="s_foto")
    
    if st.button("EKLE") and ad:
        st.session_state.comps[ad] = foto
        st.success("EKLENDİ")
    
    st.divider()
    if st.button("SIFIRLA"):
        st.session_state.votes = []
        st.session_state.comps = {}
        st.rerun()

# --- BAŞLIK ---
html_baslik = '<div class="baslik">YTÜ CİNGEN DÜĞÜN ORGANİZASYONLARI EKİBİ OYLUYOR</div>'
st.markdown(html_baslik, unsafe_allow_html=True)

# --- OYLAMA ---
with st.expander("JÜRİ GİRİŞİ"):
    j_ad = st.text_input("JÜRİ ADI:", key="j_ad")
    havuz = list(st.session_state.comps.keys())
    
    if havuz:
        secim = st.multiselect("SIRALAMA:", havuz, default=havuz, key="j_secim")
        if st.button("KAYDET"):
            if j_ad and len(secim) == len(havuz):
                veri = {"voter": j_ad, "order": secim}
                st.session_state.votes.append(veri)
                st.success("OK")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("EKSİK")
    else:
        st.info("ADAY YOK")

# --- SEREMONİ ---
if st.button("BAŞLAT"):
    if not st.session_state.votes:
        st.error("OY YOK")
    elif not st.session_state.comps:
        st.error("ADAY YOK")
    else:
        liste = list(st.session_state.comps.keys())
        random.shuffle(liste)
        tablo = []
        rapor = []
        
        st.divider()
        kutu = st.empty()

        for aday in liste:
            puan = 0
            siralar = []
            loglar = []
            
            for v in st.session_state.votes:
                if aday in v['order']:
                    s = v['order'].index(aday) + 1
                    p = P.get(s, 0)
                else:
                    s, p = 99, 0
                
                puan += p
                siralar.append(s)
                loglar.append(f"{v['voter']}: +{p}")
