import streamlit as st
import pandas as pd
import time
import random

# --- 1. AYARLAR ---
st.set_page_config(page_title="YTÜ OYLAMA", layout="wide")

# CSS AYARLARI (Tırnak hatası olmaması için sadeleştirildi)
css_kod = """
<style>
.main { background-color: #0e1117; color: white; }
.baslik { color: #e63946; text-align: center; font-size: 40px; font-weight: 900; }
.isim { color: #e63946; font-size: 35px; font-weight: bold; text-align: center; }
.juri { padding: 8px; margin: 5px; background: #1a1c24; border-left: 5px solid #e63946; font-weight: bold; }
.sira-kutu { background: #e63946; color: white; padding: 15px; border-radius: 10px; text-align: center; font-size: 28px; font-weight: 900; margin-top: 15px; }
.stButton>button { width: 100%; background: #e63946; color: white; height: 3.5em; font-weight: bold; font-size: 18px; }
</style>
"""
st.markdown(css_kod, unsafe_allow_html=True)

# PUAN SİSTEMİ
F1 = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

# --- 2. HAFIZA ---
if 'votes' not in st.session_state: st.session_state.votes = []
if 'comps' not in st.session_state: st.session_state.comps = {}
if 'stage' not in st.session_state: st.session_state.stage = 0 
if 'step' not in st.session_state: st.session_state.step = 0
if 'order' not in st.session_state: st.session_state.order = []
if 'last_img' not in st.session_state: st.session_state.last_img = None

# --- 3. PANEL (OTO İSİM ÖZELLİKLİ) ---
with st.sidebar:
    st.header("PANEL")
    
    # Dosya Yükleyici
    s_img = st.file_uploader("FOTO:", type=['png','jpg','jpeg'], key="upl")
    
    # Oto İsim Mantığı
    if s_img and s_img != st.session_state.last_img:
        st.session_state.last_img = s_img
        # Dosya adından uzantıyı at (orn: Ahmet.jpg -> Ahmet)
        yeni_ad = s_img.name.rsplit('.', 1)[0]
        st.session_state.s_ad_key = yeni_ad
    
    # İsim Alanı
    s_ad = st.text_input("ISIM:", key="s_ad_key")
    
    if st.button("EKLE") and s_ad:
        st.session_state.comps[s_ad] = s_img
        st.success("EKLENDİ")
    
    st.divider()
    if st.button("SIFIRLA"):
        for k in st.session_state.keys():
            del st.session_state[k]
        st.rerun()

# --- BAŞLIK ---
st.markdown('<div class="baslik">YTÜ CİNGEN DÜĞÜN ORGANİZASYONLARI EKİBİ OYLUYOR</div>', unsafe_allow_html=True)

# --- 4. OYLAMA ---
if st.session_state.stage == 0:
    with st.expander("JÜRİ GİRİŞİ", expanded=True):
        j_ad = st.text_input("JÜRİ ADI:")
        pool = list(st.session_state.comps.keys())
        
        if pool:
            secim = st.multiselect("SIRALAMA:", pool, default=pool)
            if st.button("KAYDET"):
                if j_ad and len(secim) == len(pool):
                    ver = {"voter": j_ad, "order": secim}
                    st.session_state.votes.append(ver)
                    st.success("KAYDEDİLDİ")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.warning("EKSİK BİLGİ")
        else:
            st.info("ADAY YOK")
    
    st.divider()
    if st.button("SEREMONİYİ BAŞLAT"):
        if st.session_state.votes and st.session_state.comps:
            keys = list(st.session_state.comps.keys())
            random.shuffle(keys)
            st.session_state.order = keys
            st.session_state.stage = 1
            st.session_state.step = 0
            st.rerun()
        else:
            st.error("OY VEYA ADAY EKSİK")

# --- 5. SEREMONİ (MANUEL İLERLEME) ---
elif st.session_state.stage == 1:
    idx = st.session_state.step
    target = st.session_state.order
    
    if idx >= len(target):
        st.session_state.stage = 2
        st.rerun()
    
    curr = target[idx]
    
    # Hesaplamalar
    p_toplam = 0
    s_list = []
    logs = []
    
    for v in st.session_state.votes:
        if curr in v['order']:
            s = v['order'].index(curr) + 1
            p = F1.get(s, 0)
        else:
            s, p = 99, 0
        p_toplam += p
        s_list.append(s)
        logs.append(f"{v['voter']}: +{p}")

    avg = sum(s_list) / len(s_list) if s_list else 99
