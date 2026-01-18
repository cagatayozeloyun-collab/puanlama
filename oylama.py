import streamlit as st
import pandas as pd
import time
import random

# --- AYARLAR ---
st.set_page_config(page_title="YTÜ OYLAMA", layout="wide")

# CSS (Kısa ve Güvenli)
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

F1 = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

# --- HAFIZA ---
if 'votes' not in st.session_state: st.session_state.votes = []
if 'comps' not in st.session_state: st.session_state.comps = {}
if 'stage' not in st.session_state: st.session_state.stage = 0 # 0: Hazırlık, 1: Başladı, 2: Bitti
if 'step' not in st.session_state: st.session_state.step = 0   # Hangi adaydayız
if 'order' not in st.session_state: st.session_state.order = [] # Rastgele sıra

# --- PANEL ---
with st.sidebar:
    st.header("PANEL")
    s_ad = st.text_input("ISIM:", key="s_ad")
    s_img = st.file_uploader("FOTO:", type=['png','jpg','jpeg'], key="s_img")
    
    if st.button("EKLE") and s_ad:
        st.session_state.comps[s_ad] = s_img
        st.success("OK")
    
    st.divider()
    if st.button("SIFIRLA"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

# --- BAŞLIK ---
st.markdown('<div class="baslik">YTÜ CİNGEN DÜĞÜN ORGANİZASYONLARI EKİBİ OYLUYOR</div>', unsafe_allow_html=True)

# --- 1. OYLAMA EKRANI ---
if st.session_state.stage == 0:
    with st.expander("JÜRİ GİRİŞİ", expanded=True):
        j_ad = st.text_input("JÜRİ ADI:")
        pool = list(st.session_state.comps.keys())
        
        if pool:
            secim = st.multiselect("SIRALAMA:", pool, default=pool)
            if st.button("KAYDET"):
                if j_ad and len(secim) == len(pool):
                    st.session_state.votes.append({"voter": j_ad, "order": secim})
                    st.success("KAYDEDİLDİ")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.warning("EKSİK BİLGİ")
        else:
            st.info("ADAY EKLEYİN")
    
    st.divider()
    if st.button("SEREMONİYİ BAŞLAT"):
        if st.session_state.votes and st.session_state.comps:
            # Sıralamayı bir kere belirle ve kaydet
            keys = list(st.session_state.comps.keys())
            random.shuffle(keys)
            st.session_state.order = keys
            st.session_state.stage = 1
            st.session_state.step = 0
            st.rerun()
        else:
            st.error("OY VEYA ADAY EKSİK")

# --- 2. SEREMONİ (MANUEL GEÇİŞ) ---
elif st.session_state.stage == 1:
    idx = st.session_state.step
    target_list = st.session_state.order
    
    # Eğer tüm adaylar bittiyse bitişe geç
    if idx >= len(target_list):
        st.session_state.stage = 2
        st.rerun()
    
    # Şu anki aday
    curr = target_list[idx]
    
    # Hesaplamalar
    puan_toplam = 0
    sira_listesi = []
    loglar = []
    rapor_data = [] # Tüm raporu her adımda hesapla ki tablo güncel olsun
    
    # Tüm oyları tara
    for v in st.session_state.votes:
        if curr in v['order']:
            s = v['order'].index(curr) + 1
            p = F1.get(s, 0)
        else:
            s, p = 99, 0
        
        puan_toplam += p
        sira_listesi.append(s)
        loglar.append(f"{v['voter']}: +{p}")

    avg = sum(sira_listesi) / len(sira_listesi) if sira_listesi else 99
    
    # GENEL TABLOYU HESAPLA (O ana kadar açıklananlar + şu anki)
    # Sadece şu ana kadar sırası gelmiş adayları tabloya ekleyelim mi? 
    # Hayır, heyecan olsun diye sadece şu anki ve geçmiştekileri gösterelim.
    visible_candidates = target_list[:idx+1]
    
    leaderboard = []
    for cand in visible_candidates:
        c_puan = 0
        c_sira = []
        for v in st.session_state.votes:
            if cand in v['order']:
                r = v['order'].index(cand) + 1
                pt = F1.get(r, 0)
            else:
                pt = 0
            c_puan += pt
            c_sira.append(r)
        
        c_avg = sum(c_sira) / len(c_sira) if c_sira else 99
        leaderboard.append({"ADAY": cand, "PUAN": c_puan, "AVG": c_avg})
    
    df = pd.DataFrame(leaderboard).sort_values(by=["PUAN", "AVG"], ascending=[False, True]).reset_index(drop=True)
    df.index += 1
    
    # Şu anki adayın sırası
    try:
        now_rank = df[df['ADAY'] == curr].index[0]
    except:
        now_rank = 1

    # --- EKRAN ---
    c1, c2, c3 = st.columns([1.5, 1, 1.5])
    
    with c1:
        h_html = f'<div class="isim">{curr}</div>'
        st.markdown(h_html, unsafe_allow_html=True)
        img = st.session_state.comps.get(curr)
        if img: st.image(img, width=450)
    
    with c2:
        st.write("### PUANLAR")
        for l in loglar:
            st.markdown(f'<div class="juri">{l}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sira-kutu">{now_rank}. SIRADA!</div>', unsafe_allow_html=True)
    
    with c3:
        st.write("### PUAN DURUMU")
        st.table(df)

    # İLERLEME BUTONU
    st.divider()
    btn_label = "SONRAKİ ADAYI GÖSTER ->" if idx < len(target_list) - 1 else "SONUÇLARI BİTİR VE RAPOR AL ->"
    if st.button(btn_label, type="primary"):
        st.session_state.step += 1
        st.rerun()

# --- 3. BİTİŞ VE RAPOR ---
elif st.session_state.stage == 2:
    st.balloons()
    st.success("OYLAMA TAMAMLANDI!")
    
    # Rapor Hazırlığı
    full_report = []
    for cand in st.session_state.comps.keys():
        for v in st.session_state.votes:
            if cand in v['order']:
                p = F1.get(v['order'].index(cand) + 1, 0)
            else:
                p = 0
            # Aynı jüri/aday çiftini tekilleştirmek için listeye ekle
            full_report.append({"Aday": cand, "Juri": v['voter'], "Puan": p})
    
    # HATA DÜZELTME: DataFrame oluştur ve duplicate sil
    df_rep = pd.DataFrame(full_report)
    
    if not df_rep.empty:
        # Aynı jüri aynı adaya 2 kere oy verdiyse sonuncusunu tut
        df_rep = df_rep.drop_duplicates(subset=['Aday', 'Juri'], keep='last')
        
        # Pivot (Hata veren yer burasıydı, artık temizlendi)
        try:
            pivot = df_rep.pivot(index="Aday", columns="Juri", values="Puan").fillna(0)
            
            st.write("### DETAYLI RAPOR")
            st.dataframe(pivot)
            
            csv = pivot.to_csv().encode('utf-8')
            st.download_button("RAPORU İNDİR (CSV)", csv, "sonuc.csv", "text/csv")
        except Exception as e:
            st.error(f"Rapor hatası: {e}")
            st.write(df_rep) # Hata olursa ham veriyi göster

    if st.button("YENİ OYLAMA BAŞLAT"):
        st.session_state.stage = 0
        st.session_state.votes = []
        st.session_state.comps = {}
        st.rerun()
