import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

# 1. Sayfa Yapılandırması (En başta olmalıdır)
st.set_page_config(page_title="E Blok Varlık ve İSG Risk Analiz Sistemi", layout="wide")

# Session State Başlatma (Güvenli Alan)
if "analiz_veritabani" not in st.session_state:
    st.session_state["analiz_veritabani"] = []

# ==========================================
# 2. VERİ TABANI TANIMLARI (23 LAB & VARLIKLAR)
# ==========================================
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

# ==========================================
# 3. HESAPLAMA MOTORU
# ==========================================
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

# ==========================================
# 4. STREAMLIT ARAYÜZÜ (MAIN)
# ==========================================
def main():
    st.title("🏢 E Blok Laboratuvar Varlik ve ISG Risk Analiz Sistemi")
    st.caption("Literatur Tabanli Cihaz ve Kimyasal ISG Parametreleri Ile Karar Destek Prototipi")
    st.markdown("---")

    st.sidebar.header("📍 1. Konum ve Inceleme Turu")
    secilen_lab = st.sidebar.selectbox("Laboratuvar Secin (23 Lab):", LAB_LISTESI)
    inceleme_turu = st.sidebar.radio("Incelenecek Varlik Turu:", ["Cihaz / Ekipman Incelemesi", "Kimyasal Madde Incelemesi"])

    st.sidebar.markdown("---")
    st.sidebar.header("⚙️ 2. Parametre Girisi")

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

        if st.sidebar.button("💾 Cihaz Analizini Sistem Kayitlarina Ekle"):
            O_m, S_m, O_k, F_k, m_sc, k_sc, stat, flg, prio = calculate_risk_scores(puan_artisi, d_skoru, t_hours)
            st.session_state["analiz_veritabani"].append({
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
            st.sidebar.success(f"{secilen_cihaz} analizi eklendi!")

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
        t_hours = st.sidebar.slider("Haftalik Maruziyet Suresi (Saat/Hafta):", 0.1, 40.0, 15.0, 0.5)
        kkd_uygunluk = st.sidebar.selectbox("KKD Kullanimi:", ["Tam", "Eksik / Yok"])
        deneyim = st.sidebar.selectbox("Arastirmaci Deneyimi:", ["Uzman", "Ogrenci / Acemi"])

        if sds_durumu == "Yok": puan_artisi += 0.5
        if depolama_dolabi == "Acik Rafta": puan_artisi += 1.0
        if sekonder_kap == "Yok": puan_artisi += 0.5
        if uyumsuzluk_depo == "Yan Yana": puan_artisi += 1.5
        if ceker_ocak == "Dusuk / Yetersiz": puan_artisi += 1.0
        elif ceker_ocak == "Ceker Ocak Yok": puan_artisi += 2.0
        if kkd_uygunluk == "Eksik / Yok": puan_artisi += 1.0
        if deneyim == "Ogrenci / Acemi": puan_artisi += 0.5

        if "HF" in secilen_kimyasal or idlh_ppm < 50: d_skoru = 100
        elif "H314" in h_kodlari or parlama_noktasi < 0 or stel_ppm < 100: d_skoru = 70
        else: d_skoru = 40

        if st.sidebar.button("💾 Kimyasal Analizini Sistem Kayitlarina Ekle"):
            O_m, S_m, O_k, F_k, m_sc, k_sc, stat, flg, prio = calculate_risk_scores(puan_artisi, d_skoru, t_hours)
            st.session_state["analiz_veritabani"].append({
                "Mekan": secilen_lab,
                "Tur": "Kimyasal Madde",
                "Varlik Adi": secilen_kimyasal,
                "Parlama Noktasi": f"{parlama_noktasi}C",
                "H-Kodlari": h_kodlari,
                "STEL / IDLH (ppm)": f"{stel_ppm} / {idlh_ppm}",
                "Sekonder Kap": sekonder_kap,
                "Ceker Ocak": ceker_ocak,
                "Sure (sa/hf)": t_hours,
                "5x5 Matris Skoru": m_sc,
                "Fine-Kinney Skoru": round(k_sc, 1),
                "Capraz Dogrulama Uyarisi": stat,
                "Nihai Risk Onceligi": prio
            })
            st.sidebar.success(f"{secilen_kimyasal} analizi eklendi!")

    # TABLAR
    tab1, tab2 = st.tabs(["📊 E Blok Genel Varlik ve ISG Risk Tablosu", "🔍 Anlik Secilen Varlik Analiz Raporu"])

    with tab1:
        st.subheader("E Blok Tum Laboratuvarlar ISG Risk ve Varlik Envanteri")
        
        if len(st.session_state["analiz_veritabani"]) == 0:
            st.info("Henuz kaydedilmis bir analiz yok. Sol taraftaki menuden parametreleri secip 'Sistem Kayitlarina Ekle' butonuna basin.")
        else:
            df_analiz = pd.DataFrame(st.session_state["analiz_veritabani"])
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Toplam Analiz Edilen Varlik", len(df_analiz))
            c2.metric("Acil Eylem (Oncelik 1) Sayisi", len(df_analiz[df_analiz["Nihai Risk Onceligi"].str.contains("Oncelik 1")]))
            c3.metric("Yontemsel Sapma / Kor Nokta Uyarisi", len(df_analiz[df_analiz["Capraz Dogrulama Uyarisi"].str.contains("UYARI")]))

            st.dataframe(df_analiz, use_container_width=True)

            csv_data = df_analiz.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 TUBITAK Proje Raporu Icin Tum Varlik Risk Tablosunu (CSV) Indir", data=csv_data, file_name="E_Blok_ISG_Risk_Analizi.csv", mime="text/csv")
            
            if st.button("🗑️ Tum Kayitlari Temizle"):
                st.session_state["analiz_veritabani"] = []
                st.rerun()

    with tab2:
        st.subheader(f"Konum: {secilen_lab}")
        O_m, S_m, O_k, F_k, m_sc, k_sc, stat, flg, prio = calculate_risk_scores(puan_artisi, d_skoru, t_hours)

        if inceleme_turu == "Cihaz / Ekipman Incelemesi":
            st.write(f"**Incelenen Cihaz:** `{secilen_cihaz}`")
            st.write(f"**Proses Parametreleri:** Sicaklik: `{calisma_sicakligi} C` | Basinc: `{calisma_basinci} Bar` | Doner Aksam: `{doner_aksam}`")
            st.write(f"**Bakim Takibi:** Son Bakim: `{son_bakim_tarihi}` | Gelecek Kontrol: `{sonraki_bakim_tarihi}` | Muayene: `{bakim_durumu}`")
        else:
            st.write(f"**Incelenen Kimyasal:** `{secilen_kimyasal}`")
            st.write(f"**Tehlike Kodlari:** `{h_kodlari}` | Parlama Noktasi: `{parlama_noktasi} C` | STEL: `{stel_ppm} ppm` | IDLH: `{idlh_ppm} ppm`")
            st.write(f"**Depolama Sartlari:** Sekonder Kap: `{sekonder_kap}` | Emniyet Dolabi: `{depolama_dolabi}` | Uyumsuzluk: `{uyumsuzluk_depo}`")

        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        col1.metric("5x5 Matris Risk Skoru (R = O x S)", f"{m_sc} / 25")
        col2.metric("Fine-Kinney Risk Skoru (R = O x F x D)", f"{k_sc:.1f}")
        col3.metric("Nihai Karar Destek Seviyesi", prio)

        st.markdown("---")
        st.subheader("Yontemsel Capraz Dogrulama Katmani")
        if flg > 0:
            st.error(f"SISTEM TESPITI: {stat}")
        else:
            st.success(f"SISTEM TESPITI: {stat}")

        st.subheader("6331 SK Uyarinca Otomatik Aksiyon Plani")
        
        if inceleme_turu == "Cihaz / Ekipman Incelemesi":
            if bakim_durumu != "Guncel ve Onayli":
                st.warning("1. Bakim/Kalibrasyon Adimi (ACIL): Cihazin periyodik bakimi veya kalibrasyon tarihi gecmis. Muayene tamamlanana kadar cihaz kullanima kapatilmalidir.")
            if sabitleme_durumu != "Tam Sabitlenmis":
                st.warning("2. Muhendislik Onlemi: Ekipman/Tup cift noktadan kelepce veya zincirle sabitlenmelidir.")
            if emniyet_valfi == "Yok / Tikali":
                st.error("3. Basinc Guvenligi: Yuksek basinc hattinda asiri basinc koruma valfi/burst disk tikali veya eksik.")
        else:
            if ceker_ocak != "Standart":
                st.warning("1. Muhendislik Onlemi: Ucutu/Toksik cozucu calismalari mutlak suretle aktif ceker ocak altinda yurutulmelidir.")
            if uyumsuzluk_depo == "Yan Yana":
                st.error("2. Kimyasal Depolama: Uyumsuz kimyasallar (asitler ve organik cozuculer) derhal ayristirilmali ve havalandirmali emniyet dolaplarina aktarilmalidir.")

if __name__ == "__main__":
    main()
