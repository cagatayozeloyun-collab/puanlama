import streamlit as st
import pandas as pd
import time
import random

# --- 1. AYARLAR ---
st.set_page_config(page_title="YTÜ CİNGEN OYLAMA", layout="wide")

# HATA RİSKİNİ YOK ETMEK İÇİN CSS'İ GÜVENLİ HALE GETİRDİM
st.markdown("""
<style>
.main { background-color: #0e1117; color: white; }
.main-title { color: #e63946; text-align: center; font-size: 40px; font-weight: 900; margin-bottom: 20px; }
.item-header { color: #e63946; font-size: 30px; font-weight: bold; text-align: center; margin-bottom: 10px; }
.jury-box { font-size: 18px; font-weight: bold; margin: 5px; border-left: 4px solid #e63946; padding-left: 10px; background: #1a1c24; }
.rank-balon { background: #e63946; color: white; padding: 15px; border-radius: 10px; text-align: center; font-size: 28px; font-weight: bold; margin-top: 15px; }
.stButton>button { width: 100%; background: #e63946; color: white; font-weight: bold; height: 3em; }
</style>
""", unsafe_allow_html=True)

F1_POINTS = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

# --- 2. HAFIZA ---
if 'all_votes' not in st.session_state: st.session_state.all_votes = []
if 'competitor_data' not in st.session_state: st.session_state.competitor_data = {}

# --- 3. YAN PANEL ---
with st.sidebar:
    st.header("⚙️ ORGANİZASYON")
    # Değişken isimlerini kısa ve net tuttuk
    s_name = st.text_input("YARIŞMACI ADI:", key="s_name")
    s_file = st.file_uploader("FOTOĞRAF:", type=['png','jpg','jpeg'], key="s_file")
    
    if st.button("EKLE") and s_name:
        st.session_state.competitor_data[s_name] = s_file
        st.success(f"{s_name} EKLENDİ")
    
    st.divider()
    if st.button("SIFIRLA"):
        st.session_state.all_votes = []
        st.session_state.competitor_data = {}
        st.rerun()

# ANA BAŞLIK
st.markdown('<div class="main-title">YTÜ CİNGEN DÜĞÜN ORGANİZASYONLARI EKİBİ OYLUYOR</div>', unsafe_allow_html=True)

# --- 4. OYLAMA GİRİŞİ ---
with st.expander("📝 JÜRİ GİRİŞİ (GİZLİ)"):
    j_name = st.text_input("JÜRİ ADI:", key="j_name")
    items = list(st.session_state.competitor_data.keys())
    
    if items:
        # Hata veren fonksiyonu düzelttik
        j_order = st.multiselect("SIRALAMA YAP:", items, default=items, key="j_order")
        if st.button("KAYDET"):
            if j_name and len(j_order) == len(items):
                st.session_state.all_votes.append({"voter": j_name, "order": j_order})
                st.success("KAYDEDİLDİ!")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("ADINIZI YAZIN VE HERKESİ SIRALAYIN")
    else:
        st.info("SOL TARAFTAN YARIŞMACI EKLEYİN")

# --- 5. SEREMONİ ---
if st.button("🚀 BAŞLAT"):
    if not st.session_state.all_votes:
        st.error("OY YOK!")
    elif not st.session_state.competitor_data:
        st.error("YARIŞMACI YOK!")
    else:
        pool = list(st.session_state.competitor_data.keys())
        random.shuffle(pool)
        leaderboard = []
        audit = [] 
        
        st.divider()
        stage = st.empty()

        for item in pool:
            total = 0
            ranks = []
            logs = []
            
            for v in st.session_state.all_votes:
                if item in v['order']:
                    pos = v['order'].index(item) + 1
                    p = F1_POINTS.get(pos, 0)
                else:
                    pos, p = 99, 0
                
                total += p
                ranks.append(pos)
                logs.append(f"{v['voter']}: +{p}")
                audit.append({"Isim": item, "Juri": v['voter'], "Puan": p})
            
            avg = sum(ranks) / len(ranks) if ranks else 99
            leaderboard.append({"ISIM": item, "PUAN": total, "AVG": avg})
            
            df = pd.DataFrame(leaderboard).sort_values(by=["PUAN", "AVG"], ascending=[False, True]).reset_index(drop=True)
            df.index += 1
            now_rank = df[df['ISIM'] == item].index[0]

            with stage.container():
                c1, c2, c3 = st.columns([1.5, 1, 1.5])
                with c1:
                    st.markdown(f'<div class="item-header">{item}</div>', unsafe_allow_html=True)
                    pic = st.session_state.competitor_data.get(item)
                    if pic: st.image(pic, width=400)
                with c2:
                    st.write("### PUANLAR")
                    for l in logs: st.markdown(f'<div class="jury-box">{l}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="rank-balon">{now_rank}. SIRADA</div>', unsafe_allow_html=True)
                with c3:
                    st.write("### TABLO")
                    st.table(df)
            
            time.sleep(6)

        st.balloons()
        st.success("BİTTİ!")

        # --- 6. RAPOR İNDİR ---
        st.divider()
        if audit:
            df_audit = pd.DataFrame(audit)
            pivot = df_audit.pivot(index="Isim", columns="Juri", values="Puan").fillna(0)
            csv = pivot.to_csv().encode('utf-8')
            
            st.download_button(
                label="RAPORU İNDİR (CSV)",
                data=csv,
                file_name="sonu
