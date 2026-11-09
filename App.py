import streamlit as st
import pandas as pd
import numpy as np

# Sayfa Yapılandırması
st.set_page_config(page_title="E Blok İSG Karar Destek Sistemi", layout="wide", page_icon="🏢")

# ==========================================
# 1. VERİ TABANI & DETAYLI İSG PARAMETRE TANIMLARI
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

# ==========================================
# 2. ALGORİTMİK HESAPLAMA MOTORU
# ==========================================
def calculate_fine_kinney_frequency(t_hours):
    if t_hours >= 30: return 10.0
    elif 10 <= t_hours < 30: return 6.0
    elif 3 <= t_hours < 10: return 3.0
    elif 1 <= t_hours < 3: return 2.0
    elif 0.25 <= t_hours < 1: return 1.0
    else: return 0.5

def calculate_probability_score(onlem_puan, kkd_durum, deneyim_durum):
    """
    Saha önlemlerine, KKD ve deneyim şartlarına göre olasılık çarpanını dinamik hesaplar.
    """
    base_prob = 3.0 + onlem_puan
    
    if kkd_durum == "Tam ve Standartlara Uygun (EN Onaylı)": base_prob -= 0.5
    elif kkd_durum == "Eksik veya Standart Dışı": base_prob += 1.0

    if deneyim_durum == "Uzman / Deneyimli Araştırmacı": base_prob -= 0.5
    elif deneyim_durum == "Öğrenci / Eğitimsiz Acemi": base_prob += 0.5

    O_matris = int(np.clip(round(base_prob), 1, 5))
    matris_to_kinney_prob = {1: 0.5, 2: 1.0, 3: 3.0, 4: 6.0, 5: 10.0}
    O_kinney = matris_to_kinney_prob[O_matris]

    return O_matris, O_kinney

def calculate_matrix_severity(d_skoru):
    if d_skoru >= 100: return 5
    elif d_skoru >= 70: return 4
    elif d_skoru >= 40: return 3
    elif d_skoru >= 15: return 2
    else: return 1

def cross_validation_harmonization(matrix_score, kinney_score, S_matris):
    if matrix_score < 15 and kinney_score >= 200:
        return "UYARI: Frekans Kör Noktası! (Sürekli Kullanımda Kümülatif Risk)", 1, "Öncelik 1 - Acil Eylem"
    elif matrix_score >= 15 and kinney_score < 70 and S_matris >= 4:
        return "UYARI: Şiddet Seyrelmesi Sapması! (Seyrek Yapılan Ama Ölümcül Risk)", 2, "Öncelik 1 - Kritik Prosedür Şartı"
    else:
        if matrix_score >= 15 or kinney_score >= 320: return "Normal Uyum", 0, "Öncelik 1 - Acil Eylem"
        elif matrix_score >= 8 or kinney_score >= 70: return "Normal Uyum", 0, "Öncelik 2 - Önemli Risk"
        else: return "Normal Uyum", 0, "Öncelik 3 - Rutin Kontrol"

# Session State
if "bina_genel_envanteri" not in st.session_state:
    st.session_state.bina_genel_envanteri = []

# ==========================================
# 3. KULLANICI ARAYÜZÜ (STREAMLIT)
# ==========================================
def main():
    st.title("🏢 E Blok İSG Uzmanı Karar Destek Sistemi")
    st.caption("Kimya Mühendisliği Bölümü 23 Laboratuvarının Bütüncül ve Dinamik Saha Risk Analiz Prototipi")
    st.markdown("---")

    # SOL PANEL - LABORATUVAR SEÇİMİ VE SAHA DENETİM FORMU
    st.sidebar.header("📋 İSG Saha Denetim Paneli")
    secilen_lab = st.sidebar.selectbox("1. Denetlenecek Laboratuvarı Seçin:", LAB_LISTESI)

    st.sidebar.markdown("---")
    st.sidebar.subheader("🔎 Ortak Saha Denetim Parametreleri")

    # Ortak Parametreler
    tup_durum = st.sidebar.radio("• Yangın Tüpleri & Basınçlı Gaz Silindirleri:", 
                                ["Tam Sabitlenmiş (Çift Zincirli/Kelepçeli)", "Kısmen Bağlı / Tek Zincir", "Sabitlenmemiş / Devrilme Riski Var"])
    ceker_ocak_durum = st.sidebar.radio("• Havalandırma / Çeker Ocak Emişi (0.3-0.5 m/s):", 
                                       ["Standartlara Uygun & Periyodik Ölçülmüş", "Emiş Hızı Düşük / Yetersiz", "Çeker Ocak Yok / Çalışmıyor"])
    yalniz_calisma = st.sidebar.radio("• Yalnız Çalışma (Working Alone) Protokolü:", 
                                     ["İzin Prosedürüne Uygun / Denetimli", "Prosedürsüz / Tek Başına Çalışılıyor"])
    
    kkd_durum = st.sidebar.selectbox("• KKD Kullanım Durumu:", ["Tam ve Standartlara Uygun (EN Onaylı)", "Eksik veya Standart Dışı"])
    deneyim_durum = st.sidebar.selectbox("• Operatör / Araştırmacı Deneyimi:", ["Uzman / Deneyimli Araştırmacı", "Öğrenci / Eğitimsiz Acemi"])
    t_hours = st.sidebar.slider("• Haftalık Operasyon Süresi (Saat/Hafta):", 0.1, 40.0, 15.0, 0.5)

    st.sidebar.markdown("---")
    st.sidebar.subheader("⚠️ Laboratuvara Özel İSG Parametreleri")

    # LABORATUVARA ÖZEL PARAMETRELERİ BELİRLEME
    onlem_puan = 0
    d_skoru = 40
    tehlike_tanimi = ""
    spesifik_params = {}

    # A. SÜPERKRİTİK & NANOMALZEME & PARÇACIK
    if any(k in secilen_lab for k in ["Süperkritik", "Parçacık", "Nanomalzeme", "Gözenekli"]):
        d_skoru = 100
        tehlike_tanimi = "Ekstrem Yüksek Basınç (>300 Bar), Partikül Aerosol Solunumu ve Sonikatör Gürültüsü"
        basinc_onlem = st.sidebar.radio("• Yüksek Basınç Hücresi Emniyet Diski / Valf Tahliyesi:", ["Var ve Dışarıya Açık", "Yok veya Tıkalı"])
        hepa_onlem = st.sidebar.radio("• Partikül/Toz İle Çalışmada HEPA Emiş / Glovebox:", ["Aktif Var", "Yok / Açık Tezgah"])
        
        if basinc_onlem == "Yok veya Tıkalı": onlem_puan += 1.5
        if hepa_onlem == "Yok / Açık Tezgah": onlem_puan += 1.0
        spesifik_params = {"Emniyet Diski": basinc_onlem, "HEPA Emiş": hepa_onlem}

    # B. HÜCRE KÜLTÜRÜ, BİYOKİMYA & BİYOTEKNOLOJİ
    elif any(k in secilen_lab for k in ["Hücre", "Biyokimya", "Biyoteknoloji", "Biyoproses", "Genetik", "Biyomalzeme", "Biyopolimer"]):
        d_skoru = 70
        tehlike_tanimi = "Biyolojik Bulaş (Class II), CO2 Boğulma Riski, Otoklav Yüksek Sıcaklık Yanığı"
        kabin_durum = st.sidebar.radio("• Biyogüvenlik Kabini (Class II) Validasyonu:", ["Validasyonlu & Valid Filtreli", "Filtre Dolu / Bakımsız", "Kabin Yok"])
        otoklav_durum = st.sidebar.radio("• Otoklav Kapak Emniyet Kilidi ve Basınç Tahliyesi:", ["Çalışıyor / Standart", "Arızalı / Riskli"])
        co2_sensordurum = st.sidebar.radio("• CO2 Ortam Kaçak Sensörü:", ["Var ve Çalışıyor", "Yok"])

        if kabin_durum != "Validasyonlu & Valid Filtreli": onlem_puan += 1.5
        if otoklav_durum == "Arızalı / Riskli": onlem_puan += 1.0
        if co2_sensordurum == "Yok": onlem_puan += 0.5
        spesifik_params = {"Biyogüvenlik Kabini": kabin_durum, "Otoklav Emniyeti": otoklav_durum, "CO2 Sensörü": co2_sensordurum}

    # C. ATIK YAKIT, YAKIT PİLLERİ, REOLOJİ & ENERJİ
    elif any(k in secilen_lab for k in ["Yakıt", "Atık", "Reoloji", "Enerji", "Sürdürülebilir"]):
        d_skoru = 100
        tehlike_tanimi = "Yüksek Sıcaklık Fırını (>800°C), H2/Sentez Gazı Patlaması, Statik Elektrik"
        gaz_sensor = st.sidebar.radio("• H2 / Yanıcı Gaz ATEX Ex-proof Detektör ve Selenoid Vana:", ["Var ve Aktif", "Yok / Arızalı"])
        topraklama = st.sidebar.radio("• Anti-Statik Topraklama Hattı:", ["Var", "Yok"])
        firin_yalitim = st.sidebar.radio("• Yüksek Sıcaklık Fırın İzolasyonu ve Yanık Koruması:", ["Tam Uygun", "Korumasız / Açık Isıtıcı"])

        if gaz_sensor == "Yok / Arızalı": onlem_puan += 2.0
        if topraklama == "Yok": onlem_puan += 1.0
        if firin_yalitim == "Korumasız / Açık Isıtıcı": onlem_puan += 1.0
        spesifik_params = {"ATEX Gaz Sensörü": gaz_sensor, "Topraklama": topraklama, "Fırın İzolasyonu": firin_yalitim}

    # D. BİLGİSAYAR & PROSES SİMÜLASYONU
    elif any(k in secilen_lab for k in ["Bilgisayar", "Simülasyon", "Proses Kontrol"]):
        d_skoru = 40
        tehlike_tanimi = "UPS Akü Gazı Çıkışı, Elektrik Tesisatı Aşırı Yüklenmesi, Ergonomik Riskler"
        ups_havalandirma = st.sidebar.radio("• UPS / Akü Odası Asit/Gaz Tahliye Havalandırması:", ["Var", "Yok"])
        kablo_duzen = st.sidebar.radio("• Zemin Kablo Kanalları ve Yük Dağılımı:", ["Düzenli / Kanallı", "Açıkta Kablo / Takılma Riski"])

        if ups_havalandirma == "Yok": onlem_puan += 1.5
        if kablo_duzen == "Açıkta Kablo / Takılma Riski": onlem_puan += 0.5
        spesifik_params = {"UPS Havalandırma": ups_havalandirma, "Kablo Düzeni": kablo_duzen}

    # E. KİMYA, ÇEVRE, ELEKTROKİMYA & MALZEME LABLARI
    else:
        d_skoru = 70
        tehlike_tanimi = "Solvent Buharları, Korozif Asit Banyo Sıçramaları, Islak Zemin Elektrik Kaçağı"
        gfci_durum = st.sidebar.radio("• Islak Ortam Kaçak Akım Rölesi (30mA / GFCI) & IP65 Priz:", ["Var", "Yok"])
        depolama_durum = st.sidebar.radio("• Uyumsuz Kimyasal Depolama (Asit-Baz Ayrımı):", ["Havalandırmalı Ayrı Dolaplarda", "Aynı Dolapta / Düzensiz"])

        if gfci_durum == "Yok": onlem_puan += 1.0
        if depolama_durum == "Aynı Dolapta / Düzensiz": onlem_puan += 1.5
        spesifik_params = {"Kaçak Akım Rölesi": gfci_durum, "Kimyasal Depolama": depolama_durum}

    # Genel Ortak Önlem Puanlama Katkısı
    if tup_durum != "Tam Sabitlenmiş (Çift Zincirli/Kelepçeli)": onlem_puan += 1.0
    if ceker_ocak_durum != "Standartlara Uygun & Periyodik Ölçülmüş": onlem_puan += 1.0
    if yalniz_calisma == "Prosedürsüz / Tek Başına Çalışılıyor": onlem_puan += 0.5

    # ANALİZ EKLE BUTONU
    if st.sidebar.button("➕ Bu Laboratuvar Denetimini Bina Raporuna Ekle"):
        O_matris, O_kinney = calculate_probability_score(onlem_puan, kkd_durum, deneyim_durum)
        S_matris = calculate_matrix_severity(d_skoru)
        F_kinney = calculate_fine_kinney_frequency(t_hours)

        m_score = O_matris * S_matris
        k_score = O_kinney * F_kinney * d_skoru
        status, flag, priority = cross_validation_harmonization(m_score, k_score, S_matris)

        st.session_state.bina_genel_envanteri.append({
            "Laboratuvar": secilen_lab,
            "Tehlike Profili": tehlike_tanimi,
            "Tüp Sabitleme": tup_durum,
            "Çeker Ocak": ceker_ocak_durum,
            "Yalnız Çalışma": yalniz_calisma,
            "Haftalık Süre (sa)": t_hours,
            "5x5 Matris Skoru": m_score,
            "Fine-Kinney Skoru": round(k_score, 1),
            "Çapraz Doğrulama Uyarısı": status,
            "Nihai Risk Önceliği": priority
        })
        st.sidebar.success(f"{secilen_lab} denetim sonucu bina risk raporuna eklendi!")

    # MAIN PANELS - SEKMELER
    tab1, tab2 = st.tabs(["📊 E Blok Tüm Bina İSG Risk Tablosu", "🔍 Laboratuvar Detaylı İSG Denetim Raporu"])

    with tab1:
        st.subheader("🏢 E Blok Bina Geneli İSG Risk Envanteri ve Sınıflandırması")
        
        if len(st.session_state.bina_genel_envanteri) == 0:
            st.info("Henüz eklenmiş bir laboratuvar denetim kaydı yok. Sol taraftaki İSG paneli üzerinden denetim parametrelerini seçip **'Bina Raporuna Ekle'** butonuna basın.")
        else:
            df_bina = pd.DataFrame(st.session_state.bina_genel_envanteri)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Denetlenen Laboratuvar Sayısı", len(df_bina))
            c2.metric("Acil Eylem Gerektiren Riskler (Öncelik 1)", len(df_bina[df_bina["Nihai Risk Önceliği"].str.contains("Öncelik 1")]))
            c3.metric("Yöntemsel Sapma / Kör Nokta Uyarısı", len(df_bina[df_bina["Çapraz Doğrulama Uyarısı"].str.contains("UYARI")]))

            st.dataframe(df_bina, use_container_width=True)

            csv_data = df_bina.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 TÜBİTAK Proje Raporu İçin Tüm Bina Risk Tablosunu (CSV) İndir", data=csv_data, file_name="E_Blok_23_Lab_İSG_Risk_Analizi.csv", mime="text/csv")
            
            if st.button("🗑️ Tüm Denetim Kayıtlarını Sıfırla"):
                st.session_state.bina_genel_envanteri = []
                st.rerun()

    with tab2:
        st.subheader(f"📍 Anlık Denetim Konumu: {secilen_lab}")
        st.write(f"**Baskın Tehlike Profili:** {tehlike_tanimi}")
        st.markdown("---")

        O_matris, O_kinney = calculate_probability_score(onlem_puan, kkd_durum, deneyim_durum)
        S_matris = calculate_matrix_severity(d_skoru)
        F_kinney = calculate_fine_kinney_frequency(t_hours)

        m_score = O_matris * S_matris
        k_score = O_kinney * F_kinney * d_skoru
        status, flag, priority = cross_validation_harmonization(m_score, k_score, S_matris)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("5x5 Matris Skoru (R = O × Ş)", f"{m_score} / 25")
            st.write(f"Olasılık: {O_matris} | Şiddet: {S_matris}")
        with col2:
            st.metric("Fine-Kinney Skoru (R = O × F × D)", f"{k_score:.1f}")
            st.write(f"Olasılık: {O_kinney} | Frekans: {F_kinney} | Zarar: {d_skoru}")
        with col3:
            st.metric("Nihai Risk Seviyesi", priority)

        st.markdown("---")
        st.subheader("🔄 Yöntemsel Çapraz Doğrulama & Kör Nokta Tespiti")
        if flag > 0:
            st.error(f"⚠️ **SİSTEM TESPİTİ:** {status}")
        else:
            st.success(f"✅ **SİSTEM TESPİTİ:** {status}")

        st.subheader("🛡️ 6331 Sayılı Kanun Uyarınca İSG Uzmanı Önlem Planı")
        
        if tup_durum != "Tam Sabitlenmiş (Çift Zincirli/Kelepçeli)":
            st.warning("1. **Mühendislik Önlemi (ACİL):** Yangın tüpleri ve gaz silindirleri duvara çift kelepçe/zincir ile sabitlenmelidir (Binaların Yangından Korunması Hk. Yönetmelik).")
        if ceker_ocak_durum != "Standartlara Uygun & Periyodik Ölçülmüş":
            st.warning("2. **Mühendislik Önlemi:** Çeker ocak emiş hızı 0.3 - 0.5 m/s aralığına getirilmeli ve periyodik debi kontrolü yapılmalıdır.")
        if yalniz_calisma == "Prosedürsüz / Tek Başına Çalışılıyor":
            st.info("3. **İdari Kontrol:** Tehlikeli süreçlerde tek başına çalışma engellenmeli, İş İzin Formu ve nöbetçi araştırmacı sistemi uygulanmalıdır.")
        
        for k, v in spesifik_params.items():
            st.write(f"• **{k} Durumu:** `{v}`")

if __name__ == "__main__":
    main()
