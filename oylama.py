import streamlit as st
import pandas as pd
import time
import random

# --- SAYFA AYARLARI VE GELİŞMİŞ CSS ---
st.set_page_config(page_title="YTÜ Cingen Oylama", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    
    .main-title {
        color: #e63946;
        text-align: center;
        font-family: 'Arial Black', sans-serif;
        font-size: 55px !important;
        font-weight: 900;
        margin-bottom: 30px;
        text-transform: uppercase;
        text-shadow: 3px 3px 10px rgba(230, 57, 70, 0.5);
    }

    .stButton>button { 
        width: 100%; border-radius: 12px; background-color: #e63946; 
        color: white; border: none; font-weight: bold; height: 3.8em; 
        font-size: 20px; transition: 0.3s;
    }

    .item-header { 
        color: #e63946; font-size: 55px; text-align: center; 
        font-weight: bold; text-transform: uppercase; margin: 25px 0; 
        border-bottom: 4px solid #e63946; letter-spacing: 3px;
    }

    .rank-info { 
        background-color: #1a1c24; padding: 40px; border-radius: 25px; 
        text-align: center; border: 3px solid #e63946; 
        font-size: 42px; font-weight: 900; color: #ffffff;
        margin: 30px 0; box-shadow: 0 0 30px rgba(230, 57, 70, 0.6);
        text-transform: uppercase;
    }
    
    .stTable { font-size: 26px !important; }
    th { background-color: #e63946 !important; color: white !important; font-size: 28px !important; }
    td { font-size: 24px !important; font-weight: bold; }

    .jury-score-box { 
        background-color: #1a1c24; padding: 25px; border-radius: 15px; 
        border-top: 5px solid #e63946; margin: 10px 0; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# F1 Puanlama Sistemi
F1_POINTS = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

# --- HAFIZA YÖNETİMİ ---
if 'all_votes' not in st.session_state: st.session_state.all_votes = []
if 'competitor_data' not in st.session_state:
    st.session_state.competitor_data = {}

# --- SIDEBAR: CİHAZDAN YÜKLEME ---
with st.sidebar:
    st.header("⚙️ Ekip Paneli")
    new_item = st.text_input("Yarışmacı/Öğe Adı:")
    
    # Cihazdan fotoğraf yükleme aracı
    new_photo_file = st.file_uploader("Fotoğraf Yükle (JPG/PNG):", type=['jpg', 'jpeg', 'png'])
    
    if st.button("Listeye Ekle") and new_item:
        # Fotoğrafı hafızaya kaydet (yoksa boş bırak)
        st.session_state.competitor_data[new_item] = new_photo_file if new_photo_file else None
        st.success(f"{new_item} başarıyla eklendi!")
    
    st.divider()
    if st.button("Hafızayı Temizle"):
        st.session_state.all_votes = []
        st.session_state.competitor_data = {}
        st.rerun()

# DEV ANA BAŞLIK
st.markdown('<div class="main-title">YTÜ CİNGEN DÜĞÜN ORGANİZASYONLARI EKİBİ OYLUYOR</div>', unsafe_allow_html=True)

# --- 1. OYLAMA ---
with st.expander("📝 Gizli Oylama Girişi"):
    voter = st.text_input("Jüri Adı:")
    items = list(st.session_state.competitor_data.keys())
    order = st.multiselect("Favoriden Sona Doğru Sırala:", items, default=items)
    
    if st.button("Oyu Mahzene Gönder"):
        if voter and len(order) == len(items) and len(items) > 0:
            st.session_state.all_votes.append({"voter": voter, "order": order})
            st.success("Oyunuz başarıyla kaydedildi!")
            time.sleep(1)
            st.rerun()
        else:
            st.warning("Lütfen adınızı girin ve herkesi sıralayın.")

# --- 2. SEREMONİ ---
if st.button("🔥 SONUÇLARI GÖSTER"):
    if not st.session_state.all_votes:
        st.error("Henüz oy kullanılmadı!")
    else:
        reveal_order = list(st.session_state.competitor_data.keys())
        random.shuffle(reveal_order)
        leaderboard = []

        for item in reveal_order:
            st.markdown(f'<div class="item-header">{item}</div>', unsafe_allow_html=True)
            
            # Cihazdan yüklenen fotoğrafı göster
            photo_data = st.session_state.competitor_data.get(item)
            if photo_data:
                st.image(photo_data, use_container_width=True)
            
            cols = st.columns(len(st.session_state.all_votes))
            total_p = 0
            ranks = []
            
            for i, vote in enumerate(st.session_state.all_votes):
                r = vote['order'].index(item) + 1
                p = F1_POINTS.get(r, 0)
                total_p += p
                ranks.append(r)
                with cols[i]:
                    st.markdown(f'<div class="jury-score-box"><b style="font-size:22px;">{vote["voter"]}</b><br><span style="font-size:28px; color:#e63946;">+{p}</span></div>', unsafe_allow_html=True)
            
            # Ortalama Sıra (Tie-Breaker)
            avg_r = sum(ranks) / len(ranks)
            leaderboard.append({"İsim": item, "Toplam Puan": total_p, "Ort. Sıra": round(avg_r, 2)})
            
            df = pd.DataFrame(leaderboard).sort_values(by=["Toplam Puan", "Ort. Sıra"], ascending=[False, True]).reset_index(drop=True)
            df.index += 1
            pos = df[df['İsim'] == item].index[0]
            
            # DEV SIRALAMA BALONU
            st.markdown(f'<div class="rank-info">🏆 {item} ŞU AN {pos}. SIRADA!</div>', unsafe_allow_html=True)
            
            st.write("### 📊 GÜNCEL PUAN DURUMU")
            st.table(df)
            st.divider()
            time.sleep(4)
        
        st.balloons()
