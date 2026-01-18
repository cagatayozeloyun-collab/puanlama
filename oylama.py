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
        color: #e63946; text-align: center; font-family: 'Arial Black', sans-serif;
        font-size: 45px !important; font-weight: 900; margin-bottom: 20px;
        text-transform: uppercase; text-shadow: 2px 2px 8px rgba(230, 57, 70, 0.5);
    }

    /* Fotoğraf Boyutu Sınırlandırma */
    .competitor-img {
        max-height: 400px; object-fit: contain; border-radius: 15px;
        border: 2px solid #e63946; margin-bottom: 15px;
    }

    .item-header { 
        color: #e63946; font-size: 38px; font-weight: bold; 
        text-transform: uppercase; margin-bottom: 10px; border-bottom: 2px solid #e63946;
    }

    .rank-info-box { 
        background-color: #1a1c24; padding: 25px; border-radius: 20px; 
        text-align: center; border: 3px solid #e63946; 
        font-size: 30px; font-weight: 900; color: #ffffff;
        margin-top: 20px; box-shadow: 0 0 20px rgba(230, 57, 70, 0.5);
    }
    
    /* Tablo Fontları */
    .stTable { font-size: 20px !important; }
    th { background-color: #e63946 !important; color: white !important; font-size: 22px !important; }
    td { font-size: 19px !important; font-weight: bold; }

    .jury-score-box { 
        background-color: #1a1c24; padding: 15px; border-radius: 12px; 
        border-top: 4px solid #e63946; margin: 5px 0; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# F1 Puanlama Sistemi
F1_POINTS = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

# --- HAFIZA YÖNETİMİ ---
if 'all_votes' not in st.session_state: st.session_state.all_votes = []
if 'competitor_data' not in st.session_state: st.session_state.competitor_data = {}

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Ekip Paneli")
    new_item = st.text_input("Yarışmacı Adı:")
    new_photo = st.file_uploader("Fotoğraf Yükle:", type=['jpg', 'jpeg', 'png'])
    if st.button("Listeye Ekle") and new_item:
        st.session_state.competitor_data[new_item] = new_photo
        st.success(f"{new_item} eklendi!")
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
    order = st.multiselect("Sıralamanı Yap:", items, default=items)
    if st.button("Oyu Kaydet"):
        if voter and len(order) == len(items) > 0:
            st.session_state.all_votes.append({"voter": voter, "order": order})
            st.success("Kaydedildi!")
            time.sleep(1)
            st.rerun()

# --- 2. SEREMONİ (YENİ DÜZEN) ---
if st.button("🔥 SONUÇLARI AÇIKLA"):
    if not st.session_state.all_votes:
        st.error("Henüz oy yok!")
    else:
        reveal_order = list(st.session_state.competitor_data.keys())
        random.shuffle(reveal_order)
        leaderboard = []

        # Her yarışmacı için bir aşama
        for item in reveal_order:
            st.divider()
            
            # EKRANI İKİYE BÖLÜYORUZ
            left_col, right_col = st.columns([1.2, 1])
            
            with left_col:
                st.markdown(f'<div class="item-header">{item}</div>', unsafe_allow_html=True)
                # Fotoğrafı boyutlandırılmış olarak göster
                photo = st.session_state.competitor_data.get(item)
                if photo:
                    st.image(photo, width=450)
                
                # Jüri Puanları
                jury_cols = st.columns(3)
                total_p = 0
                ranks = []
                for i, vote in enumerate(st.session_state.all_votes):
                    r = vote['order'].index(item) + 1
                    p = F1_POINTS.get(r, 0)
                    total_p += p
                    ranks.append(r)
                    with jury_cols[i % 3]:
                        st.markdown(f'<div class="jury-score-box"><b>{vote["voter"]}</b><br><span style="color:#e63946; font-size:20px;">+{p}</span></div>', unsafe_allow_html=True)
                
                # Averaj ve Sıra Hesaplama
                avg_r = sum(ranks) / len(ranks)
                leaderboard.append({"İsim": item, "Puan": total_p, "Ort. Sıra": round(avg_r, 2)})
                
                # Bu yarışmacının anlık sıralamasını bul
                temp_df = pd.DataFrame(leaderboard).sort_values(by=["Puan", "Ort. Sıra"], ascending=[False, True]).reset_index(drop=True)
                temp_df.index += 1
                pos = temp_df[temp_df['İsim'] == item].index[0]
                
                st.markdown(f'<div class="rank-info-box">🏆 {pos}. SIRAYA YERLEŞTİ!</div>', unsafe_allow_html=True)

            with right_col:
                st.write("### 📊 CANLI PUAN DURUMU")
                st.table(temp_df)
            
            time.sleep(5) # Bir sonraki kişiye geçmeden önce 5 saniye bekle

        st.balloons()
        st.success("Tüm ekip oylamayı tamamladı!")
