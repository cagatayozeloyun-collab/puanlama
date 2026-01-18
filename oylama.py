import streamlit as st
import pandas as pd
import time
import random

# --- 1. AYARLAR ---
st.set_page_config(page_title="YTÜ CİNGEN", layout="wide")

# CSS AYARLARI (Kısa ve Güvenli)
css_code = """
<style>
.main { background-color: #0e1117; color: white; }
.main-title { color: #e63946; text-align: center; font-size: 40px; font-weight: 900; margin: 20px; }
.jury-box { padding: 10px; margin: 5px; background: #1a1c24; border-left: 5px solid #e63946; font-weight: bold; }
.rank-balon { background: #e63946; color: white; padding: 15px; border-radius: 10px; text-align: center; font-size: 28px; margin-top: 15px; font-weight: 900; }
.stButton>button { width: 100%; background: #e63946; color: white; font-weight: bold; height: 3.5em; }
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

F1_POINTS = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

# --- 2. HAFIZA ---
if 'all_votes' not in st.session_state: st.session_state.all_votes = []
if 'competitor_data' not in st.session_state: st.session_state.competitor_data = {}

# --- 3. YAN PANEL ---
with st.sidebar:
    st.header("⚙️ ORGANİZASYON")
    s_name = st.text_input("YARIŞMACI ADI:", key="side_name")
    s_file = st.file_uploader("FOTOĞRAF:", type=['png','jpg','jpeg'], key="side_file")
    
    if st.button("EKLE") and s_name:
        st.session_state.competitor_data[s_name] = s_file
        st.success("EKLENDİ")
    
    st.divider()
    if st.button("SIFIRLA"):
        st.session_state.all_votes = []
        st.session_state.competitor_data = {}
        st.rerun()

# BAŞLIK
st.markdown('<div class="main-title">YTÜ CİNGEN DÜĞÜN ORGANİZASYONLARI EKİBİ OYLUYOR</div>', unsafe_allow_html=True)

# --- 4. OYLAMA ---
with st.expander("📝 JÜRİ GİRİŞİ (GİZLİ)"):
    j_name = st.text_input("JÜRİ ADI:", key="j_input")
    pool = list(st.session_state.competitor_data.keys())
    
    if pool:
        j_order = st.multiselect("SIRALAMA:", pool, default=pool, key="j_order")
        if st.button("KAYDET"):
            if j_name and len(j_order) == len(pool):
                st.session_state.all_votes.append({"voter": j_name, "order": j_order})
                st.success("KAYDEDİLDİ!")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("EKSİK BİLGİ GİRMEYİN")
    else:
        st.info("SOL TARAFTAN YARIŞMACI EKLEYİN")

# --- 5. SEREMONİ ---
if st.button("🚀 BAŞLAT"):
    if not st.session_state.all_votes:
        st.error("OY YOK!")
    elif not st.session_state.competitor_data:
        st.error("YARIŞMACI YOK!")
    else:
        reveal = list(st.session_state.competitor_data.keys())
        random.shuffle(reveal)
        board = []
        audit = [] 
        
        st.divider()
        area = st.empty()

        for item in reveal:
            tot = 0
            ranks = []
            logs = []
            
            for v in st.session_state.all_votes:
                if item in v['order']:
                    pos = v['order'].index(item) + 1
                    p = F1_POINTS.get(pos, 0)
                else:
                    pos, p = 99, 0
                
                tot += p
                ranks.append(pos)
                logs.append(f"{v['voter']}: +{p}")
                audit.append({"Isim": item, "Juri": v['voter'], "Puan": p})
            
            avg = sum(ranks) / len(ranks) if ranks else 99
            board.append({"ISIM": item, "PUAN": tot, "AVG": avg})
            
            # Tabloyu oluştur
            df = pd.DataFrame(board)
            df = df.sort_values(by=["PUAN", "AVG"], ascending=[False, True])
            df = df.reset_index(drop=True)
            df.index += 1
            
            # Anlık sıra
            now_rank = df[df['ISIM'] == item].index[0]

            with area.container():
                c1, c2, c3 = st.columns([1.5, 1, 1.5])
                with c1:
                    st.markdown(f'<div class="item-header">{item}</div>', unsafe
