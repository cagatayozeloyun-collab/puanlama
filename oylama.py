import streamlit as st
import pandas as pd
import time
import random

# --- SAYFA AYARI ---
st.set_page_config(page_title="YTÜ OYLAMA", layout="wide")

# --- CSS ---
st.markdown("""
<style>
.main { background-color: #0e1117; color: white; }
.baslik { color: #e63946; text-align: center; font-size: 40px; font-weight: 900; }
.isim { color: #e63946; font-size: 30px; font-weight: bold; text-align: center; }
.juri { padding: 5px; margin: 5px; background: #1a1c24; border-left: 4px solid #e63946; }
.sira { background: #e63946; color: white; padding: 10px; border-radius: 10px; text-align: center; font-size: 25px; margin-top: 10px; }
.stButton>button { width: 100%; background: #e63946; color: white; height: 3em; }
</style>
""", unsafe_allow_html=True)

# --- PUANLAR ---
P = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

# --- HAFIZA (Session State) ---
if 'votes' not in st.session_state: st.session_state.votes = []
if 'comps' not in st.session_state: st.session_state.comps = {}
if 'durum' not in st.session_state: st.session_state.durum = 'hazirlik' # hazirlik, basladi, bitti

# --- SOL PANEL ---
with st.sidebar:
    st.header("PANEL")
    ad = st.text_input("ISIM:", key="s_ad")
    foto = st.file_uploader("FOTO:", type=['png','jpg','jpeg'], key="s_foto")
    
    if st.button("EKLE") and ad:
        st.session_state.comps[ad] = foto
        st.success("EKLENDİ")
    
    st.divider()
    # Bilgi Göstergesi
    st.write(f"**Aday Sayısı:** {len(st.session_state.comps)}")
    st.write(f"**Oy Sayısı:** {len(st.session_state.votes)}")
    
    st.divider()
    if st.button("SIFIRLA"):
        st.session_state.votes = []
        st.session_state.comps = {}
        st.session_state.durum = 'hazirlik'
        st.rerun()

# --- BAŞLIK ---
st.markdown('<div class="baslik">YTÜ CİNGEN DÜĞÜN ORGANİZASYONLARI EKİBİ OYLUYOR</div>', unsafe_allow_html=True)

# --- OYLAMA (Sadece hazırlık aşamasında görünür) ---
if st.session_state.durum == 'hazirlik':
    with st.expander("JÜRİ GİRİŞİ", expanded=True):
        j_ad = st.text_input("JÜRİ ADI:", key="j_ad")
        havuz = list(st.session_state.comps.keys())
        
        if havuz:
            secim = st.multiselect("SIRALAMA:", havuz, default=havuz, key="j_secim")
            if st.button("KAYDET"):
                if j_ad and len(secim) == len(havuz):
                    veri = {"voter": j_ad, "order": secim}
                    st.session_state.votes.append(veri)
                    st.success("KAYDEDİLDİ")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.warning("ADINIZI YAZIN VE HERKESİ SIRALAYIN")
        else:
            st.info("ÖNCE SOL TARAFTAN YARIŞMACI EKLEYİN")

# --- SEREMONİ BAŞLATMA BUTONU ---
if st.session_state.durum == 'hazirlik':
    if st.button("SEREMONİYİ BAŞLAT"):
        if not st.session_state.votes:
            st.error("HİÇ OY YOK! LÜTFEN ÖNCE OY KULLANIN.")
        elif not st.session_state.comps:
            st.error("HİÇ ADAY YOK!")
        else:
            st.session_state.durum = 'basladi'
            st.rerun()

# --- SEREMONİ EKRANI (Otomatik Çalışır) ---
if st.session_state.durum == 'basladi':
    liste = list(st.session_state.comps.keys())
    # Her seferinde aynı rastgelelik olsun diye seed kullanabiliriz ama şimdilik shuffle
    # Not: Streamlit rerun yaptığında shuffle değişebilir, bu yüzden
    # sıralamayı hafızaya almak en doğrusu ama basitlik için direkt akış yapıyoruz:
    
    # Animasyon döngüsü için placeholder
    kutu = st.empty()
    
    # Sonuçları hesapla
    tablo = []
    rapor = []
    
    # Sırayla göster
    shuffled_liste = sorted(liste, key=lambda x: random.random()) # Basit karıştırma
    
    for i, aday in enumerate(shuffled_liste):
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
            rapor.append({"Aday": aday, "Juri": v['voter'], "Puan": p})
        
        avg = sum(siralar) / len(siralar) if siralar else 99
        tablo.append({"ADAY": aday, "PUAN": puan, "AVG": avg})
        
        # DataFrame oluştur
        df = pd.DataFrame(tablo)
        df = df.sort_values(by=["PUAN", "AVG"], ascending=[False, True])
        df = df.reset_index(drop=True)
        df.index += 1
        
        suanki_sira = df[df['ADAY'] == aday].index[0]

        # EKRANI GÜNCELLE
        with kutu.container():
            c1, c2, c3 = st.columns([1.5, 1, 1.5])
            
            with c1:
                st.markdown(f'<div class="isim">{aday}</div>', unsafe_allow_html=True)
                img = st.session_state.comps.get(aday)
                if img: st.image(img, width=400)
            
            with c2:
                st.write("### PUANLAR")
                for l in loglar:
                    st.markdown(f'<div class="juri">{l}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="sira">{suanki_sira}. SIRADA</div>', unsafe_allow_html=True)
            
            with c3:
                st.write("### DURUM")
                st.table(df)
        
        time.sleep(5) # 5 Saniye bekle
    
    # Döngü bitince
    st.session_state.durum = 'bitti'
    st.session_state.sonuc_tablosu = df
    st.session_state.rapor_verisi = rapor
    st.rerun()

# --- BİTİŞ EKRANI ---
if st.session_state.durum == 'bitti':
    st.balloons()
    st.success("OYLAMA TAMAMLANDI!")
    
    # Son halini göster
    st.table(st.session_state.sonuc_tablosu)
    
    st.divider()
    if st.button("YENİDEN BAŞLAT"):
        st.session_state.durum = 'hazirlik'
        st.session_state.votes = []
        st.session_state.comps = {}
        st.rerun()

    # Rapor İndirme
    if 'rapor_verisi' in st.session_state:
        df_r = pd.DataFrame(st.session_state.rapor_verisi)
        pivot = df_r.pivot(index="Aday", columns="Juri", values="Puan").fillna(0)
        csv = pivot.to_csv().encode('utf-8')
        
        st.download_button(
            label="RAPORU İNDİR (CSV)",
            data=csv,
            file_name="sonuc.csv",
            mime="text/csv"
        )
