import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

# Sayfa Yapılandırması
st.set_page_config(page_title="E Blok Varlık & İSG Risk Analiz Sistemi", layout="wide", page_icon="🧪")

# ==========================================
# 1. BİNA VE LABORATUVAR TANIMLARI (23 LAB)
# ==========================================
LAB_LISTESI = [
    "1. Bilgisayar Laboratuvarı",
    "2. Kimya Mühendisliği Laboratuvarı",
    "3. Proses Kontrol Laboratuvarı",
    "4. Biyokimya Mühendisliği Laboratuvarı",
    "5. Süperkritik Akışkan Teknolojisi Laboratuvarı",
    "6. Endüstriyel Biyoteknoloji Laboratuvarı",
    "7. Metabolik ve Genetik Mühendisliği Laboratuvarı",
    "8. Parçacık Teknolojisi Laboratuvarı",
    "9. Sürdürülebilir Teknolojiler Laboratuvarı",
    "10. Çevre Araştırma Laboratuvarı",
    "11. Gözenekli Malzeme ve Membran Araştırma Laboratuvarı",
    "12. Kimyasal Elektrokimyasal Arıtım Laboratuvarı",
    "13. Biyoproses Araştırma Laboratuvarı",
    "14. Biyomalzeme Bilimi ve Mühendisliği Laboratuvarı",
    "15. Kontrol Reoloji ve Yakıt Pilleri Araştırma Laboratuvarı",
    "16. Biyopolimer Laboratuvarı",
    "17. Proses Simülasyon Laboratuvarı",
    "18. Süperkritik Akışkan ve Nanomalzeme Araştırma Laboratuvarı",
    "19. Çevre ve Proses Kontrol Laboratuvarı",
    "20. Hücre ve Doku Kültürü Laboratuvarı",
    "21. Nanobiyoteknoloji Laboratuvarı",
    "22. Atık Yakıt Teknolojileri Araştırma Laboratuvarı",
    "23. Enerji ve Malzeme Laboratuvarı"
]

LAB_EKIPMANLARI = {
    "Cihazlar": [
        "Süperkritik Akışkan Ekstraksiyon Hücresi (>300 Bar)",
        "Yüksek Sıcaklık Piroliz / Tüp Fırın (>800°C)",
        "Buharlı Sterilizatör / Yüksek Basınçlı Otoklav",
        "Hidrojen Yakıt Pili Test Düzeneği",
        "Biyogüvenlik Kabini (Class II Biohazard)",
        "Rotasyonel Reometre / Viskozimetre",
        "Ultrasonik Homojenizatör / Sonikatör",
        "Soğutmalı Santrifüj Cihazı",
        "Elektrokimyasal Arıtım & Kaplama Hücresi",
        "Yüksek Basınçlı Gaz Silindiri / Tüpü (H2, N2, CO2)",
        "Kuru Kimyevi Tozlu / CO2 Yangın Söndürme Tüpü",
        "Göz ve Vücut Acil Durum Duşu",
        "Kesintisiz Güç Kaynağı (UPS) & Akü Grubu"
    ],
    "Kimyasallar": [
        "n-Hekzan (Solvent)",
        "Toluen (Solvent)",
        "Dietil Eter (Solvent)",
        "Metanol (Solvent)",
        "Kloroform (Solvent)",
        "Derişik Sülfürik Asit (H2SO4 %98)",
        "Derişik Hidroklorik Asit (HCl %37)",
        "Hidroflorik Asit (HF %48)",
        "Sodyum Hidroksit (NaOH)",
        "Hidrojen Peroksit (H2O2 %30)",
        "Formaldehit (%37 Çözelti)",
        "Sodyum Azür (NaN3)"
    ]
}

# ==========================================
# 2. HESAPLAMA MOTORU (5x5 MATRİS & FINE-KINNEY)
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
    priority = "Öncelik 3 - Rutin Kontrol"

    if m_score < 15 and k_score >= 200:
        status = "UYARI: Frekans Kör Noktası! (Sürekli Kullanımda Kümülatif Yüksek Risk)"
        flag = 1
        priority = "Öncelik 1 - Acil Eylem"
    elif m_score >= 15 and k_score < 70 and S_matris >= 4:
        status = "UYARI: Şiddet Seyrelmesi Sapması! (Seyrek Yapılan Ama Ölümcül Risk)"
        flag = 2
        priority = "Öncelik 1 - Kritik Prosedür Şartı"
    else:
        if m_score >= 15 or k_score >= 320: priority = "Öncelik 1 - Acil Eylem"
        elif m_score >= 8 or k_score >= 70: priority = "Öncelik 2 - Önemli Risk"
        else: priority = "Öncelik 3 - Rutin Kontrol"

    return O_matris, S_matris, O_kinney, F_kinney, m_score, k_score, status, flag, priority

# Session State
if "analiz_veritabani" not in st.session_state:
    st.session_state.analiz_veritabani = []

# ==========================================
# 3. KULLANICI ARAYÜZÜ (STREAMLIT)
# ==========================================
def main():
    st.title("🏢 E Blok Laboratuvar Varlık & İSG Risk Analiz Sistemi")
    st.caption("Literatür Tabanlı Cihaz ve Kimyasal İSG Parametreleri İle Hibrit Karar Destek Prototipi")
    st.markdown("---")

    st.sidebar.header("📍 1. Konum ve İnceleme Türü")
    secilen_lab = st.sidebar.selectbox("Laboratuvar Seçin (23 Lab):", LAB_LISTESI)
    inceleme_turu = st.sidebar.radio("İncelenecek Varlık Türü:", ["Cihaz / Ekipman İncelemesi", "Kimyasal Madde İncelemesi"])

    st.sidebar.markdown("---")
    st.sidebar.header("⚙️ 2. Literatör Tabanlı Parametre Girişi")

    puan_artisi = 0.0
    d_skoru = 40

    # ---------------------------------------------------------
    # MODÜL A: CİHAZ / EKİPMAN İNCELEMESİ (LİTERATÜR PARAMETRELERİ)
    # ---------------------------------------------------------
    if inceleme_turu == "Cihaz / Ekipman İncelemesi":
        secilen_cihaz = st.sidebar.selectbox("İncelenecek Cihaz / Ekipmanı Seçin:", LAB_EKIPMANLARI["Cihazlar"])
        
        st.sidebar.subheader("🌡️ 1. Proses ve Operasyonel Limitler")
        calisma_sicakligi = st.sidebar.number_input("Çalışma Sıcaklığı (°C):", min_value=-80, max_value=1200, value=25)
        calisma_basinci = st.sidebar.number_input("Çalışma Basıncı (Bar):", min_value=0.0, max_value=500.0, value=1.0)
        doner_aksam = st.sidebar.selectbox("Döner Aksam / Kapma Noktası (Pinch-Point Guards):", ["Korumalı / Sıkışma Koruması Var", "Korumasız / Döner Aksam Açıkta"])
        
        st.sidebar.subheader("📅 2. Yaşam Döngüsü ve Kalibrasyon")
        son_bakim_tarihi = st.sidebar.date_input("Son Periyodik Bakım / Kalibrasyon Tarihi:", date(2025, 1, 15))
        sonraki_bakim_tarihi = st.sidebar.date_input("Bir Sonraki Rutin Kontrol Tarihi:", date(2026, 6, 15))
        bakim_durumu = st.sidebar.selectbox("Periyodik Muayene & Kalibrasyon Durumu:", ["Güncel ve Onaylı Sertifikalı", "Zamanı Geçmiş / Bakımsız", "Hiç Yapılmamış"])
        
        st.sidebar.subheader("🛡️ 3. Mekanik Emniyet ve Koruma")
        sabitleme_durumu = st.sidebar.selectbox("Duvar / Tezgah Sabitleme (Çift Zincir/Kelepçe):", ["Tam Sabitlenmiş", "Kısmen Bağlı / Tek Zincir", "Sabitlenmemiş / Devrilme Riski"])
        emniyet_valfi = st.sidebar.selectbox("Aşırı Basınç Valfi / Patlama Diski (Burst Disk):", ["Var ve Tahliyesi Güvenli Alana Açık", "Yok / Tahliye Tıkalı", "Uygulanamaz (Basınçsız)"])
        acil_stop = st.sidebar.selectbox("Acil Durum Stop Butonu & Interlock Kilit Sistemleri:", ["Var ve Çalışıyor", "Eksik / Arızalı"])
        
        st.sidebar.subheader("👤 4. İdari ve Operatör Şartları")
        t_hours = st.sidebar.slider("Haftalık Operasyon Süresi (Saat/Hafta):", 0.1, 40.0, 10.0, 0.5)
        sop_durum = st.sidebar.selectbox("Standart Çalışma Prosedürü (SÖP) Asılı mı?:", ["Evet (Cihaz Üzerinde Asılı)", "Hayır / Eksik"])
        yalniz_calisma = st.sidebar.selectbox("Yalnız Çalışma (Working Alone) İzni:", ["Prosedürlü / Denetimli", "Prosedürsüz / Tek Başına Çalışılıyor"])
        kullanici_yetkinlik = st.sidebar.selectbox("Operatör Yetkinliği:", ["Uzman / Sertifikalı Personel", "Öğrenci / Eğitimsiz Acemi"])
        kkd_uygunluk = st.sidebar.selectbox("KKD Kullanımı:", ["Tam ve Standartlara Uygun", "Eksik veya Yok"])

        # Literatür Puanlama
        if bakim_durumu == "Zamanı Geçmiş / Bakımsız": puan_artisi += 1.0
        elif bakim_durumu == "Hiç Yapılmamış": puan_artisi += 1.5
        if sabitleme_durumu != "Tam Sabitlenmiş": puan_artisi += 1.0
        if emniyet_valfi == "Yok / Tahliye Tıkalı": puan_artisi += 1.5
        if acil_stop == "Eksik / Arızalı": puan_artisi += 0.5
        if doner_aksam == "Korumasız / Döner Aksam Açıkta": puan_artisi += 1.0
        if sop_durum == "Hayır / Eksik": puan_artisi += 0.5
        if yalniz_calisma == "Prosedürsüz / Tek Başına Çalışılıyor": puan_artisi += 0.5
        if kullanici_yetkinlik == "Öğrenci / Eğitimsiz Acemi": puan_artisi += 0.5
        if kkd_uygunluk == "Eksik veya Yok": puan_artisi += 0.5

        if calisma_basinci > 100 or calisma_sicakligi > 500: d_skoru = 100
        elif calisma_basinci > 10 or calisma_sicakligi > 100: d_skoru = 70
        else: d_skoru = 40

        if st.sidebar.button("💾 Cihaz Analizini Sistem Kayıtlarına Ekle"):
            O_m, S_m, O_k, F_k, m_sc, k_sc, stat, flg, prio = calculate_risk_scores(puan_artisi, d_skoru, t_hours)
            st.session_state.analiz_veritabani.append({
                "Mekân": secilen_lab,
                "Tür": "Cihaz / Ekipman",
                "Varlık Adı": secilen_cihaz,
                "Sıcaklık (°C)": calisma_sicakligi,
                "Basınç (Bar)": calisma_basinci,
                "Son Bakım": str(son_bakim_tarihi),
                "Gelecek Kontrol": str(sonraki_bakim_tarihi),
                "Bakım Durumu": bakim_durumu,
                "Sabitleme": sabitleme_durumu,
                "Süre (sa/hf)": t_hours,
                "5x5 Matris Skoru": m_sc,
                "Fine-Kinney Skoru": round(k_sc, 1),
                "Çapraz Doğrulama Uyarısı": stat,
                "Nihai Risk Önceliği": prio
            })
            st.sidebar.success(f"{secilen_cihaz} analizi başarıyla eklendi!")

    # ---------------------------------------------------------
    # MODÜL B: KİMYASAL MADDE İNCELEMESİ (LİTERATÜR PARAMETRELERİ)
    # ---------------------------------------------------------
    else:
        secilen_kimyasal = st.sidebar.selectbox("İncelenecek Kimyasal Maddeyi Seçin:", LAB_EKIPMANLARI["Kimyasallar"])
        
        st.sidebar.subheader("☣️ 1. Tehlike Sınıfı ve Eşik Değerler")
        parlama_noktasi = st.sidebar.number_input("Parlama Noktası (°C):", min_value=-50, max_value=100, value=-22)
        h_kodlari = st.sidebar.text_input("GHS H-Kodları (Örn: H225, H314, H330):", "H225, H304, H315, H336")
        stel_ppm = st.sidebar.number_input("STEL Değeri (ppm - 15 dk Maruziyet):", min_value=0, max_value=5000, value=50)
        idlh_ppm = st.sidebar.number_input("IDLH Değeri (ppm - Anında Ölümcül Sınır):", min_value=0, max_value=10000, value=1100)
        sds_durumu = st.sidebar.selectbox("Güncel 16 Maddelik SDS / GBF Formu Varlığı:", ["Var ve Ulaşılabilir", "Yok / Eksik"])

        st.sidebar.subheader("📦 2. Depolama ve Sekonder Koruma")
        depolama_dolabi = st.sidebar.selectbox("EN 14470-1 Emniyet Dolabı:", ["Ex-proof Havalandırmalı Dolapta", "Açık Rafta / Standart Dolapta"])
        sekonder_kap = st.sidebar.selectbox("Sekonder Kap (Sızıntı Tavası / %110 Hacim):", ["Var (Dökülme Tavası Mevcut)", "Yok"])
        uyumsuzluk_depo = st.sidebar.selectbox("Uyumsuz Kimyasal Depolaması (Asit-Baz Ayrımı):", ["Tam Ayrıştırılmış", "Aynı Dolapta Yan Yana"])

        st.sidebar.subheader("🌬
