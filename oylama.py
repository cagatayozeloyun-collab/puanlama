import streamlit as st
import pandas as pd
import time
import random

# --- GÜVENLİ RERUN ---
def safe_rerun():
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

# --- HATA YAKALAYICI ---
try:
    # --- AYARLAR ---
    st.set_page_config(page_title="YTÜ OYLAMA", layout="wide")

    # CSS
    css = """
    <style>
    .main { background-color: #0e1117; color: white; }
    .baslik { color: #e63946; text-align: center; font-size: 40px; font-weight: 900; }
    .isim { color: #e63946; font-size: 35px; font-weight: bold; text-align: center; }
    .juri { padding: 8px; margin: 5px; background: #1a1c24; border-left: 5px solid #e63946; font-weight: bold; }
    .aykiri { padding: 8px; margin: 5px; background: #3d0000; border-left: 5px solid #ff0000; font-weight: bold; color: #ff9999; }
    .sira-kutu { background: #e63946; color: white; padding: 15px; border-radius: 10px; text-align: center; font-size: 28px; font-weight: 900; margin-top: 15px; }
    .stButton>button { width: 100%; background: #e63946; color: white; height: 3.5em; font-weight: bold; font-size: 18px; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    F1 = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

    # --- HAFIZA ---
    if 'votes' not in st.session_state: st.session_state.votes = []
    if 'comps' not in st.session_state: st.session_state.comps = {}
    if 'stage' not in st.session_state: st.session_state.stage = 0 
    if 'step' not in st.session_state: st.session_state.step = 0
    if 'order' not in st.session_state: st.session_state.order = []
    if 'last_img' not in st.session_state: st.session_state.last_img = None

    # --- PANEL ---
    with st.sidebar:
        st.header("PANEL")
        s_img = st.file_uploader("FOTO:", type=['png','jpg','jpeg'], key="upl")
        
        # Oto İsim
        if s_img and s_img != st.session_state.last_img:
            st.session_state.last_img = s_img
            isim_temiz = s_img.name.rsplit('.', 1)[0]
            st.session_state.s_ad_key = isim_temiz
        
        s_ad = st.text_input("ISIM:", key="s_ad_key")
        
        if st.button("EKLE", key="btn_ekle") and s_ad:
            st.session_state.comps[s_ad] = s_img
            st.success("EKLENDİ")
        
        st.divider()
        if st.button("SIFIRLA", key="btn_sifirla"):
            for k in st.session_state.keys():
                del st.session_state[k]
            safe_rerun()

    # --- BAŞLIK ---
    st.markdown('<div class="baslik">YTÜ CİNGEN DÜĞÜN ORGANİZASYONLARI EKİBİ OYLUYOR</div>', unsafe_allow_html=True)

    # --- 1. OYLAMA ---
    if st.session_state.stage == 0:
        with st.expander("JÜRİ GİRİŞİ", expanded=True):
            j_ad = st.text_input("JÜRİ ADI:")
            pool = list(st.session_state.comps.keys())
            
            if pool:
                secim = st.multiselect("SIRALAMA:", pool, default=pool)
                # --- HATA DÜZELTME: LINE 75 İÇİN KEY EKLENDİ ---
                if st.button("OYU KAYDET", key="btn_oy_kaydet"):
                    if j_ad and len(secim) == len(pool):
                        ver = {"voter": j_ad, "order": secim}
                        st.session_state.votes.append(ver)
                        st.success("KAYDEDİLDİ")
                        time.sleep(0.5)
                        safe_rerun()
                    else:
                        st.warning("EKSİK BİLGİ")
            else:
                st.info("ADAY EKLEYİN")
        
        st.divider()
        if st.button("SEREMONİYİ BAŞLAT", key="btn_baslat"):
            if st.session_state.votes and st.session_state.comps:
                keys = list(st.session_state.comps.keys())
                random.shuffle(keys)
                st.session_state.order = keys
                st.session_state.stage = 1
                st.session_state.step = 0
                safe_rerun()
            else:
                st.error("OY YOK!")

    # --- 2. SEREMONİ ---
    elif st.session_state.stage == 1:
        idx = st.session_state.step
        target = st.session_state.order
        
        if idx >= len(target):
            st.session_state.stage = 2
            safe_rerun()
        
        curr = target[idx]
        
        # --- HESAPLAMALAR VE AYKIRI ANALİZİ ---
        temp_data = []
        ranks = []
        
        for v in st.session_state.votes:
            if curr in v['order']:
                s = v['order'].index(curr) + 1
                p = F1.get(s, 0)
            else:
                s, p = 99, 0
            temp_data.append({"voter": v['voter'], "rank": s, "points": p})
            ranks.append(s)
        
        avg = sum(ranks) / len(ranks) if ranks else 99
        
        # En uzak mesafeyi bul
        max_diff = 0
        if ranks:
            max_diff = max(abs(r - avg) for r in ranks)
            
        logs = []
        log_styles = []
        
        for d in temp_data:
            diff = abs(d['rank'] - avg)
            is_outlier = (diff == max_diff and max_diff > 1.5) # Biraz toleranslı olsun
            
            txt = f"{d['voter']}: +{d['points']}"
            if is_outlier:
                txt += f" ⚡ (Sıra: {d['rank']})"
                logs.append(txt)
                log_styles.append("aykiri")
            else:
                logs.append(txt)
                log_styles.append("juri")

        # Tablo
        visible = target[:idx+1]
        board = []
        for cand in visible:
            cp = 0
            cs = []
            for v in st.session_state.votes:
                if cand in v['order']:
                    r = v['order'].index(cand) + 1
                    pt = F1.get(r, 0)
                else:
                    pt = 0
                cp += pt
                cs.append(r)
            cavg = sum(cs) / len(cs) if cs else 99
            board.append({"ADAY": cand, "PUAN": cp, "AVG": cavg})
        
        if board:
            df = pd.DataFrame(board)
            df = df.sort_values(by=["PUAN", "AVG"], ascending=[False, True])
            df = df.reset_index(drop=True)
            df.index += 1
            try:
                now_rank = df[df['ADAY'] == curr].index[0]
            except:
                now_rank = "?"
        else:
            df = pd.DataFrame()
            now_rank = "?"

        # Ekran
        c1, c2, c3 = st.columns([1.5, 1, 1.5])
        
        with c1:
            st.markdown(f'<div class="isim">{curr}</div>', unsafe_allow_html=True)
            img = st.session_state.comps.get(curr)
            if img: st.image(img, width=450)
        
        with c2:
            st.write("### PUANLAR")
            for txt, style in zip(logs, log_styles):
                st.markdown(f'<div class="{style}">{txt}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="sira-kutu">{now_rank}. SIRADA!</div>', unsafe_allow_html=True)
        
        with c3:
            st.write("### DURUM")
            st.table(df)

        st.divider()
        
        if idx < len(target) - 1:
            btn_txt = "SONRAKİ ADAYI GÖSTER ->"
        else:
            btn_txt = "SONUÇLARI BİTİR ->"
            
        if st.button(btn_txt, type="primary", key="btn_ilerle"):
            st.session_state.step += 1
            safe_rerun()

    # --- 3. BİTİŞ ---
    elif st.session_state.stage == 2:
        st.balloons()
        st.success("OYLAMA TAMAMLANDI!")
        
        rep_data = []
        for c in st.session_state.comps.keys():
            for v in st.session_state.votes:
                if c in v['order']:
                    p = F1.get(v['order'].index(c) + 1, 0)
                else:
                    p = 0
                rep_data.append({"Aday": c, "Juri": v['voter'], "Puan": p})
        
        df_rep = pd.DataFrame(rep_data)
        
        if not df_rep.empty:
            df_rep = df_rep.drop_duplicates(subset=['Aday', 'Juri'], keep='last')
            
            st.divider()
            st.write("### 📊 KAOS İSTATİSTİKLERİ")
            juri_grp = df_rep.groupby("Juri")["Puan"].sum().sort_values(ascending=False)
            if not juri_grp.empty:
                bonkor = juri_grp.index[0]
                cimri = juri_grp.index[-1]
                k1, k2, k3 = st.columns(3)
                k1.metric("👑 ŞAMPİYON", st.session_state.order[0] if st.session_state.order else "-")
                k2.metric("💸 EN BONKÖR", f"{bonkor}")
                k3.metric("🥶 EN CİMRİ", f"{cimri}")
            
            st.divider()
            c_g1, c_g2 = st.columns([2, 1])
            with c_g1:
                st.write("### 📈 GRAFİK")
                aday_grp = df_rep.groupby("Aday")["Puan"].sum().sort_values(ascending=False)
                st.bar_chart(aday_grp, color="#e63946")
            
            with c_g2:
                st.write("### 📂 RAPOR")
                try:
                    piv = df_rep.pivot(index="Aday", columns="Juri", values="Puan").fillna(0)
                    st.dataframe(piv, height=300)
                    csv = piv.to_csv().encode('utf-8')
                    st.download_button("CSV İNDİR", csv, "sonuc.csv", "text/csv")
                except:
                    st.write("Hata oluştu")

        if st.button("YENİ OYLAMA BAŞLAT", key="btn_restart"):
            st.session_state.stage = 0
            st.session_state.votes = []
            st.session_state.comps = {}
            safe_rerun()

except Exception as e:
    st.error(f"HATA: {e}")
    if st.button("SİSTEMİ KURTAR", key="btn_rescue"):
        for k in st.session_state.keys():
            del st.session_state[k]
        safe_rerun()
