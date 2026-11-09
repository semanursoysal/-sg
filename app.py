import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

st.set_page_config(page_title="E Blok Varlik ve ISG Risk Analiz Sistemi", layout="wide")

LAB_LISTESI = [
    "1. Bilgisayar Laboratuvari",
    "2. Kimya Muhendisligi Laboratuvari",
    "3. Proses Kontrol Laboratuvari",
    "4. Biyokimya Muhendisligi Laboratuvari",
    "5. Superkritik Akiskan Teknolojisi Laboratuvari",
    "6. Endustriyel Biyoteknoloji Laboratuvari",
    "7. Metabolik ve Genetik Muhendisligi Laboratuvari",
    "8. Parcacik Teknolojisi Laboratuvari",
    "9. Surdurulebilir Teknolojiler Laboratuvari",
    "10. Cevre Arastirma Laboratuvari",
    "11. Gozenekli Malzeme ve Membran Arastirma Laboratuvari",
    "12. Kimyasal Elektrokimyasal Aritim Laboratuvari",
    "13. Biyoproses Arastirma Laboratuvari",
    "14. Biyomalzeme Bilimi ve Muhendisligi Laboratuvari",
    "15. Kontrol Reoloji ve Yakit Pilleri Arastirma Laboratuvari",
    "16. Biyopolimer Laboratuvari",
    "17. Proses Simulasyon Laboratuvari",
    "18. Superkritik Akiskan ve Nanomalzeme Arastirma Laboratuvari",
    "19. Cevre ve Proses Kontrol Laboratuvari",
    "20. Hucre ve Doku Kulturu Laboratuvari",
    "21. Nanobiyoteknoloji Laboratuvari",
    "22. Atik Yakit Teknolojileri Arastirma Laboratuvari",
    "23. Enerji ve Malzeme Laboratuvari"
]

LAB_EKIPMANLARI = {
    "Cihazlar": [
        "Superkritik Akiskan Ekstraksiyon Hucreleri (>300 Bar)",
        "Yuksek Sicaklik Piroliz / Tup Firin (>800 C)",
        "Buharli Sterilizator / Yuksek Basincli Otoklav",
        "Hidrojen Yakit Pili Test Duzenegi",
        "Biyoguvenlik Kabini (Class II Biohazard)",
        "Rotasyonel Reometre / Viskozimetre",
        "Ultrasonik Homojenizator / Sonikator",
        "Sogutmali Santrifuj Cihazi",
        "Elektrokimyasal Aritim & Kaplama Hucresi",
        "Yuksek Basincli Gaz Silindiri / Tupu (H2, N2, CO2)",
        "Kuru Kimyevi Tozlu / CO2 Yangin Sondurme Tupu",
        "Goz ve Vucut Acil Durum Dusu",
        "Kesintisiz Guc Kaynagi (UPS) & Aku Grubu"
    ],
    "Kimyasallar": [
        "n-Hekzan (Solvent)",
        "Toluen (Solvent)",
        "Dietil Eter (Solvent)",
        "Metanol (Solvent)",
        "Kloroform (Solvent)",
        "Derisik Sulfurik Asit (H2SO4 %98)",
        "Derisik Hidroklorik Asit (HCl %37)",
        "Hidroflorik Asit (HF %48)",
        "Sodyum Hidroksit (NaOH)",
        "Hidrojen Peroksit (H2O2 %30)",
        "Formaldehit (%37 Cozelti)",
        "Sodyum Azur (NaN3)"
    ]
}

def calculate_fine_kinney_frequency(t_hours):
    if t_hours >= 30: return 10.0
    elif 10 <= t_hours < 30: return 6.0
    elif 3 <= t_hours < 10: return 3.0
    elif 1 <= t_hours < 3: return 2.0
    elif 0.25 <= t_hours < 1: return 1.0
    else: return 0.5

def calculate_risk_scores(puan_artisi, d_skoru, t_hours):
    base_prob = 3.0 + puan_artisi
    O_matris = int(np.clip(round(base_prob), 1, 5))
    matris_to_kinney_prob = {1: 0.5, 2: 1.0, 3: 3.0, 4: 6.0, 5: 10.0}
    O_kinney = matris_to_kinney_prob[O_matris]
    F_kinney = calculate_fine_kinney_frequency(t_hours)
    
    if d_skoru >= 100: S_matris = 5
    elif d_skoru >= 70: S_matris = 4
    elif d_skoru >= 40: S_matris = 3
    elif d_skoru >= 15: S_matris = 2
    else: S_matris = 1

    m_score = O_matris * S_matris
    k_score = O_kinney * F_kinney * d_skoru

    status = "Normal Uyum"
    flag = 0
    priority = "Oncelik 3 - Rutin Kontrol"

    if m_score < 15 and k_score >= 200:
        status = "UYARI: Frekans Kor Noktasi! (Kumulatif Yuksek Risk)"
        flag = 1
        priority = "Oncelik 1 - Acil Eylem"
    elif m_score >= 15 and k_score < 70 and S_matris >= 4:
        status = "UYARI: Siddet Seyrelmesi Sapmasi! (Olumcul Risk)"
        flag = 2
        priority = "Oncelik 1 - Kritik Prosedur Sarti"
    else:
        if m_score >= 15 or k_score >= 320: priority = "Oncelik 1 - Acil Eylem"
        elif m_score >= 8 or k_score >= 70: priority = "Oncelik 2 - Onemli Risk"
        else: priority = "Oncelik 3 - Rutin Kontrol"

    return O_matris, S_matris, O_kinney, F_kinney, m_score, k_score, status, flag, priority

if "analiz_veritabani" not in st.session_state:
    st.session_state.analiz_veritabani = []

def main():
    st.title("E Blok Laboratuvar Varlik ve ISG Risk Analiz Sistemi")
    st.caption("Literatur Tabanli Cihaz ve Kimyasal ISG Parametreleri Ile Hibrit Karar Destek Prototipi")
    st.markdown("---")

    st.sidebar.header("1. Konum ve Inceleme Turu")
    secilen_lab = st.sidebar.selectbox("Laboratuvar Secin (23 Lab):", LAB_LISTESI)
    inceleme_turu = st.sidebar.radio("Incelenecek Varlik Turu:", ["Cihaz / Ekipman Incelemesi", "Kimyasal Madde Incelemesi"])

    st.sidebar.markdown("---")
    st.sidebar.header("2. Parametre Girisi")

    puan_artisi = 0.0
    d_skoru = 40

    if inceleme_turu == "Cihaz / Ekipman Incelemesi":
        secilen_cihaz = st.sidebar.selectbox("Incelenecek Cihaz / Ekipmani Secin:", LAB_EKIPMANLARI["Cihazlar"])
        
        st.sidebar.subheader("1. Proses ve Operasyonel Limitler")
        calisma_sicakligi = st.sidebar.number_input("Calisma Sicakligi (C):", min_value=-80, max_value=1200, value=25)
        calisma_basinci = st.sidebar.number_input("Calisma Basinci (Bar):", min_value=0.0, max_value=500.0, value=1.0)
        doner_aksam = st.sidebar.selectbox("Doner Aksam / Kapma Noktasi:", ["Korumali", "Korumasiz"])
        
        st.sidebar.subheader("2. Yasam Dongusu ve Kalibrasyon")
        son_bakim_tarihi = st.sidebar.date_input("Son Periyodik Bakim Tarihi:", date(2025, 1, 15))
        sonraki_bakim_tarihi = st.sidebar.date_input("Gelecek Kontrol Tarihi:", date(2026, 6, 15))
        bakim_durumu = st.sidebar.selectbox("Muayene Durumu:", ["Guncel ve Onayli", "Zamani Gecmis", "Hic Yapilmamis"])
        
        st.sidebar.subheader("3. Mekanik Emniyet ve Koruma")
        sabitleme_durumu = st.sidebar.selectbox("Tezgah Sabitleme:", ["Tam Sabitlenmis", "Kismen Bagli", "Sabitlenmemis"])
        emniyet_valfi = st.sidebar.selectbox("Asiri Basinc Valfi / Burst Disk:", ["Var ve Aktif", "Yok / Tikali", "Uygulanamaz"])
        acil_stop = st.sidebar.selectbox("Acil Durum Stop Butonu:", ["Var ve Calisiyor", "Eksik / Arizali"])
        
        st.sidebar.subheader("4. Idari ve Operator Sartlari")
        t_hours = st.sidebar.slider("Haftalik Operasyon Suresi (Saat/Hafta):", 0.1, 40.0, 10.0, 0.5)
        sop_durum = st.sidebar.selectbox("SOP Asili mi?:", ["Evet", "Hayir"])
        yalniz_calisma = st.sidebar.selectbox("Yalniz Calisma Izni:", ["Prosedurlu", "Prosedursuz"])
        kullanici_yetkinlik = st.sidebar.selectbox("Operator Yetkinligi:", ["Uzman", "Ogrenci / Acemi"])
        kkd_uygunluk = st.sidebar.selectbox("KKD Kullanimi:", ["Tam", "Eksik / Yok"])

        if bakim_durumu == "Zamani Gecmis": puan_artisi += 1.0
        elif bakim_durumu == "Hic Yapilmamis": puan_artisi += 1.5
        if sabitleme_durumu != "Tam Sabitlenmis": puan_artisi += 1.0
        if emniyet_valfi == "Yok / Tikali": puan_artisi += 1.5
        if acil_stop == "Eksik / Arizali": puan_artisi += 0.5
        if doner_aksam == "Korumasiz": puan_artisi += 1.0
        if sop_durum == "Hayir": puan_artisi += 0.5
        if yalniz_calisma == "Prosedursuz": puan_artisi += 0.5
        if kullanici_yetkinlik == "Ogrenci / Acemi": puan_artisi += 0.5
        if kkd_uygunluk == "Eksik / Yok": puan_artisi += 0.5

        if calisma_basinci > 100 or calisma_sicakligi > 500: d_skoru = 100
        elif calisma_basinci > 10 or calisma_sicakligi > 100: d_skoru = 70
        else: d_skoru = 40

        if st.sidebar.button("Cihaz Analizini Sistem Kayitlarina Ekle"):
            O_m, S_m, O_k, F_k, m_sc, k_sc, stat, flg, prio = calculate_risk_scores(puan_artisi, d_skoru, t_hours)
            st.session_state.analiz_veritabani.append({
                "Mekan": secilen_lab,
                "Tur": "Cihaz / Ekipman",
                "Varlik Adi": secilen_cihaz,
                "Sicaklik (C)": calisma_sicakligi,
                "Basinc (Bar)": calisma_basinci,
                "Son Bakim": str(son_bakim_tarihi),
                "Gelecek Kontrol": str(sonraki_bakim_tarihi),
                "Bakim Durumu": bakim_durumu,
                "Sabitleme": sabitleme_durumu,
                "Sure (sa/hf)": t_hours,
                "5x5 Matris Skoru": m_sc,
                "Fine-Kinney Skoru": round(k_sc, 1),
                "Capraz Dogrulama Uyarisi": stat,
                "Nihai Risk Onceligi": prio
            })
            st.sidebar.success(f"{secilen_cihaz} analizi basariyla eklendi!")

    else:
        secilen_kimyasal = st.sidebar.selectbox("Incelenecek Kimyasal Maddeyi Secin:", LAB_EKIPMANLARI["Kimyasallar"])
        
        st.sidebar.subheader("1. Tehlike Sinifi ve Esik Degerler")
        parlama_noktasi = st.sidebar.number_input("Parlama Noktasi (C):", min_value=-50, max_value=100, value=-22)
        h_kodlari = st.sidebar.text_input("GHS H-Kodlari:", "H225, H304, H315, H336")
        stel_ppm = st.sidebar.number_input("STEL Degeri (ppm):", min_value=0, max_value=5000, value=50)
        idlh_ppm = st.sidebar.number_input("IDLH Degeri (ppm):", min_value=0, max_value=10000, value=1100)
        sds_durumu = st.sidebar.selectbox("SDS / GBF Formu Varligi:", ["Var", "Yok"])

        st.sidebar.subheader("2. Depolama ve Sekonder Koruma")
        depolama_dolabi = st.sidebar.selectbox("Emniyet Dolabi:", ["Havalandirmali", "Acik Rafta"])
        sekonder_kap = st.sidebar.selectbox("Sekonder Kap (Dokulme Tavasi):", ["Var", "Yok"])
        uyumsuzluk_depo = st.sidebar.selectbox("Kimyasal Ayrimi:", ["Ayristirilmis", "Yan Yana"])

        st.sidebar.subheader("3. Havalandirma ve Operator Maruziyeti")
        ceker_ocak = st.sidebar.selectbox("Ceker Ocak Emis Hizi:", ["Standart", "Dusuk / Yetersiz", "Ceker Ocak Yok"])
        t_hours = st.sidebar.slider("Haftalik Maruziyet Suresi (Saat/Hafta):", 0.
