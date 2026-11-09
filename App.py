import streamlit as st
import pandas as pd
import numpy as np

# Sayfa Yapılandırması
st.set_page_config(page_title="E Blok Bütüncül İSG Karar Destek Sistemi", layout="wide", page_icon="🏢")

# ==========================================
# 1. VERİ TABANI MODÜLÜ (E Blok Envanteri: Cihazlar, Fiziksel Ekipmanlar ve Kimyasallar)
# ==========================================
@st.cache_data
def get_building_inventory():
    data = [
        # --- FİZİKSEL / YANGIN / EKİPMAN TEHLİKELERİ ---
        {"Unsur": "Kuru Kimyevi Tozlu Yangın Söndürme Tüpü (6kg)", "Kategori": "Fiziksel/Yangın Ekipmanı", "Tehlike_Turu": "Sabitlenmeme/Devrilme, Basınç Kaybı, Erişilemezlik", "D_Skoru": 40},
        {"Unsur": "CO2 Yangın Söndürme Tüpü", "Kategori": "Fiziksel/Yangın Ekipmanı", "Tehlike_Turu": "Duvara/Zincire Bağlı Olmama, Boğulma Riski", "D_Skoru": 40},
        {"Unsur": "Göz ve Vücut Acil Durum Duşu", "Kategori": "Fiziksel/Yangın Ekipmanı", "Tehlike_Turu": "Su Debisi Yetersizliği, Tıkanıklık, Rutin Test Eksikliği", "D_Skoru": 70},
        {"Unsur": "Gaz Kaçak Detektörü ve Otomatik Selenoid Vana", "Kategori": "Fiziksel/Yangın Ekipmanı", "Tehlike_Turu": "Kalibrasyon Bozukluğu, Güç Kesintisi", "D_Skoru": 70},
        {"Unsur": "Acil Çıkış Kapısı ve Kaçış Yolu", "Kategori": "Fiziksel/Yangın Ekipmanı", "Tehlike_Turu": "Kilitli Olma, Malzeme İle Engellenme", "D_Skoru": 100},

        # --- PROSES CİHAZLARI VE KAZANLAR ---
        {"Unsur": "Buhar ve Reaksiyon Kazanı (Basınçlı Kap)", "Kategori": "Proses Cihazı / Kazan", "Tehlike_Turu": "Aşırı Basınç Patlaması, Emniyet Valfi Arızası, Yüksek Sıcaklık Yanığı", "D_Skoru": 100},
        {"Unsur": "Endüstriyel Kurutucu Fırın (Vakum / Etüv)", "Kategori": "Proses Cihazı / Isıtıcı", "Tehlike_Turu": "Yüksek Sıcaklık, Solvent Buharı Parlaması, Termostat Arızası", "D_Skoru": 70},
        {"Kimyasal": "Elektrikli Isıtıcı Mantolu Reaktör", "Unsur": "Isıtmalı Karıştırma Düzeneği", "Kategori": "Proses Cihazı / Isıtıcı", "Tehlike_Turu": "Aşırı Isınma, Kıvılcım/Statik Elektrikle Solvent Tutuşması", "D_Skoru": 40},
        {"Unsur": "Distilasyon Kolonu ve Isı Değiştirici", "Kategori": "Proses Cihazı / Separasyon", "Tehlike_Turu": "Kaçak/Sızıntı, Termal Yanık, Cam Aksam Kırılması", "D_Skoru": 40},
        {"Unsur": "Yüksek Basınçlı Gaz Silindiri / Tüpü (H2, N2, He)", "Kategori": "Proses Cihazı / Gas", "Tehlike_Turu": "Zincirle Bağlı Olmama, Devrilerek Roket Etkisi Yapması, Sızıntı", "D_Skoru": 100},

        # --- MİKRO-FABRİKA VE PİLOT TESİS SİMÜLASYONLARI ---
        {"Unsur": "Kesikli / Sürekli Pilot Akış Reaktör Ünitesi", "Kategori": "Pilot Tesis / Simülasyon", "Tehlike_Turu": "Kontrolsüz Ekzotermik Reaksiyon, Basınç Artışı, Hat Sızıntısı", "D_Skoru": 100},
        {"Unsur": "Mikro-Ölçekli Çözücü Geri Kazanım Ünitesi", "Kategori": "Pilot Tesis / Simülasyon", "Tehlike_Turu": "Uçucu Buhar Patlaması, Statik Yüklenme, Havalandırma Yetersizliği", "D_Skoru": 70},
        {"Unsur": "Akışkan Yataklı Kurutma Simülatörü", "Kategori": "Pilot Tesis / Simülasyon", "Tehlike_Turu": "Toz Patlaması, Yüksek Fan Gürültüsü, Statik Elektrik", "D_Skoru": 40},

        # --- KİMYASAL MADDELER (Doğan ve ark., 2026) ---
        {"Unsur": "n-Hekzan (Solvent)", "Kategori": "Kimyasal Madde", "Tehlike_Turu": "H225, H304, H315, H336, H361f, H373 - Kanserojen/Toksik Buhar", "D_Skoru": 40},
        {"Unsur": "Toluen (Solvent)", "Kategori": "Kimyasal Madde", "Tehlike_Turu": "H225, H304, H315, H336, H361d, H373 - Uçucu Çözücü", "D_Skoru": 40},
        {"Unsur": "Dietil Eter (Solvent)", "Kategori": "Kimyasal Madde", "Tehlike_Turu": "H224, H302, H336, EUH019 - Peroksit Oluşumu ve Patlama", "D_Skoru": 40},
        {"Unsur": "Derişik Sülfürik Asit (H2SO4 %98)", "Kategori": "Kimyasal Madde", "Tehlike_Turu": "H290, H314 - Korozif / Yanık", "D_Skoru": 70},
        {"Unsur": "Hidroflorik Asit (HF %48)", "Kategori": "Kimyasal Madde", "Tehlike_Turu": "H300, H310, H330, H314 - Ölümcül Kemik Dokusu Hasarı", "D_Skoru": 100}
    ]
    return pd.DataFrame(data)

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

def calculate_probability_score(fiziksel_onlem_durumu, kkd_durumu, deneyim_durumu):
    """
    Ekipman zincirleme/sabitleme durumu, bakımlar ve KKD şartlarına göre olasılığı dinamik hesaplar.
    """
    base_prob = 3.0
    
    # Ekipman / Sabitleme / Bakım Şartları
    if fiziksel_onlem_durumu == "Tam (Zincire Bağlı / Bakımlı / Standartlara Uygun)":
        base_prob -= 1.0
    elif fiziksel_onlem_durumu == "Kısmen Uygun / Bakım Zamanı Gelmiş":
        base_prob += 0.5
    elif fiziksel_onlem_durumu == "Uygun Değil (Zincirsiz / Sabitlenmemiş / Arızalı)":
        base_prob += 1.5

    # KKD Etkisi
    if kkd_durumu == "Tam ve Standartlara Uygun":
        base_prob -= 0.5
    elif kkd_durumu == "Eksik veya Kullanılmıyor":
        base_prob += 1.0

    # Deneyim Etkisi
    if deneyim_durumu == "Deneyimli Personel / Uzman":
        base_prob -= 0.5
    elif deneyim_durumu == "Öğrenci / Eğitimsiz Acemi":
        base_prob += 0.5

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
        return "UYARI: Frekans Kör Noktası! (Sürekli Çalışmada Kümülatif Risk)", 1, "Öncelik 1 - Acil Eylem"
    elif matrix_score >= 15 and kinney_score < 70 and S_matris >= 4:
        return "UYARI: Şiddet Seyrelmesi Sapması! (Seyrek Kullanılan Ama Ölümcül Ekipman/Cihaz)", 2, "Öncelik 1 - Kritik Prosedür Şartı"
    else:
        if matrix_score >= 15 or kinney_score >= 320: return "Normal Uyum", 0, "Öncelik 1 - Acil Eylem"
        elif matrix_score >= 8 or kinney_score >= 70: return "Normal Uyum", 0, "Öncelik 2 - Önemli Risk"
        else: return "Normal Uyum", 0, "Öncelik 3 - Rutin Kontrol"

def generate_action_plan(unsur_row, priority, flag, fiziksel_durum):
    actions = []
    
    # 1. Mühendislik ve Fiziksel Sabitleme Adımları
    if "Tüpü" in unsur_row["Unsur"] or "Silindiri" in unsur_row["Unsur"]:
        if fiziksel_durum != "Tam (Zincire Bağlı / Bakımlı / Standartlara Uygun)":
            actions.append("🛠️ **Mühendislik Önlemi (ACİL):** Yangın söndürme tüpleri ve basınçlı gaz silindirleri çift noktadan kelepçe/zincir ile duvara sağlam bir şekilde sabitlenmelidir (Binaların Yangından Korunması Hk. Yönetmelik).")
        else:
            actions.append("🛠️ **Mühendislik Önlemi:** Ekipman sabitleme zincirleri ve manometre basınç göstergeleri aylık periyotlarla kontrol edilmelidir.")

    if "Kazan" in unsur_row["Unsur"] or "Kurutucu" in unsur_row["Unsur"] or "Isıtıcı" in unsur_row["Unsur"]:
        actions.append("🔥 **Proses Güvenliği:** Basınçlı kap ve fırınların emniyet valfleri, termostat kalibrasyonları ve otomatik durdurma sistemleri periyodik testten geçirilmelidir.")

    # 2. İdari Kontroller
    if flag == 1:
        actions.append("📋 **İdari Önlem (Frekans Kör Noktası):** Yüksek çalışma süreleri kısıtlanmalı, personel rotasyonu sağlanmalı ve ortam fiziksel denetimi sıklaştırılmalıdır.")
    elif flag == 2:
        actions.append("📋 **İdari Önlem (Seyrek Ama Ölümcül Risk):** İşlem/Cihaz çalıştırılmadan önce 'Çok Tehlikeli İş İzin Formu' doldurulmalı, gözetmensiz çalıştırma yapılmamalıdır.")

    # 3. KKD ve Genel Güvenlik
    actions.append("🛡️ **KKD ve Operasyonel Şart:** Çalışma ortamında standart önlük, onaylı koruyucu gözlük ve cihaz riskine uygun kişisel koruyucu kullanılmalıdır.")

    return actions

# Session State
if "bina_genel_envanteri" not in st.session_state:
    st.session_state.bina_genel_envanteri = []

# ==========================================
# 3. KULLANICI ARAYÜZÜ (STREAMLIT)
# ==========================================
def main():
    st.title("🏢 Ankara Üniversitesi Kimya Mühendisliği Bölümü (E Blok)")
    st.subheader("Bina Geneli Bütüncül Karar Destek Sistemi (Fiziksel Ekipman, Yangın, Kazan, Isıtıcı, Pilot Tesis & Kimyasallar)")
    st.markdown("---")

    df_inv = get_building_inventory()

    # SOL PANEL
    st.sidebar.header("📍 E Blok Mekân ve Unsur Seçim Paneli")

    lab_adi = st.sidebar.selectbox("1. E Blok Bölüm / Mekân Seçin:", [
        "E-101 Fizikokimya Eğitim Lab.",
        "E-102 Organik Kimya Araştırma Lab.",
        "E-103 Temel İşlemler & Pilot Tesis Simülasyon Lab.",
        "E-201 Analitik Kimya Lab.",
        "E-202 Polimer & Malzeme Lab.",
        "E-203 Biyomühendislik & Proses Lab.",
        "E-301 Genel Kimya Öğrenci Lab.",
        "E-Zemin Kazan Dairesi & Gaz Deposu"
    ])

    kategori_filtre = st.sidebar.selectbox("2. İncelemek İstediğiniz Unsur Kategorisi:", [
        "Tüm Kategoriler",
        "Fiziksel/Yangın Ekipmanı",
        "Proses Cihazı / Kazan",
        "Proses Cihazı / Isıtıcı",
        "Pilot Tesis / Simülasyon",
        "Kimyasal Madde"
    ])

    if kategori_filtre != "Tüm Kategoriler":
        filtered_items = df_inv[df_inv["Kategori"] == kategori_filtre]["Unsur"].unique()
    else:
        filtered_items = df_inv["Unsur"].unique()

    secilen_unsurlar = st.sidebar.multiselect(
        "3. Mekândaki Ekipman / Cihaz / Kimyasal Seçimi (Çoklu Seçim):",
        options=filtered_items,
        default=[filtered_items[0]] if len(filtered_items) > 0 else []
    )

    t_hours = st.sidebar.slider("4. Ekipman/Cihaz Kullanım veya Maruziyet Sıklığı (Saat/Hafta):", 0.1, 40.0, 10.0, 0.5)
    fiziksel_durum = st.sidebar.radio("5. Ekipman / Sabitleme / Bakım Durumu:", [
        "Tam (Zincire Bağlı / Bakımlı / Standartlara Uygun)",
        "Kısmen Uygun / Bakım Zamanı Gelmiş",
        "Uygun Değil (Zincirsiz / Sabitlenmemiş / Arızalı)"
    ])
    kkd_durumu = st.sidebar.radio("6. KKD Kullanım Durumu:", ["Tam ve Standartlara Uygun", "Eksik veya Kullanılmıyor"])
    deneyim_durumu = st.sidebar.radio("7. Operatör / Kullanıcı Deneyimi:", ["Deneyimli Personel / Uzman", "Öğrenci / Eğitimsiz Acemi"])

    # EKLE BUTONU
    if st.sidebar.button("➕ Seçilen Unsur Analizlerini Bina Listesine Ekle"):
        if not secilen_unsurlar:
            st.sidebar.error("Lütfen en az bir unsur veya ekipman seçin!")
        else:
            for item in secilen_unsurlar:
                item_info = df_inv[df_inv["Unsur"] == item].iloc[0]
                O_matris, O_kinney = calculate_probability_score(fiziksel_durum, kkd_durumu, deneyim_durumu)
                S_matris = calculate_matrix_severity(item_info["D_Skoru"])
                F_kinney = calculate_fine_kinney_frequency(t_hours)
                D_kinney = item_info["D_Skoru"]

                m_score = O_matris * S_matris
                k_score = O_kinney * F_kinney * D_kinney
                status, flag, priority = cross_validation_harmonization(m_score, k_score, S_matris)

                st.session_state.bina_genel_envanteri.append({
                    "Mekân / Lab": lab_adi,
                    "Incelenen Unsur / Ekipman": item,
                    "Kategori": item_info["Kategori"],
                    "Tehlike Tanımı": item_info["Tehlike_Turu"],
                    "Sabitleme/Bakım Durumu": fiziksel_durum,
                    "Kullanım (sa/hf)": t_hours,
                    "5x5 Matris Skoru": m_score,
                    "Fine-Kinney Skoru": round(k_score, 1),
                    "Çapraz Doğrulama Uyarısı": status,
                    "Nihai Risk Önceliği": priority
                })
            st.sidebar.success(f"{len(secilen_unsurlar)} adet unsur bina listesine başarıyla eklendi!")

    # SEKMELER
    tab1, tab2 = st.tabs(["📊 E Blok Genel Risk Envanteri & Raporlama", "🔍 Anlık Ekipman & Cihaz Analiz Detayı"])

    with tab1:
        st.subheader("🏢 E Blok Tüm Bina İSG Risk Haritası")
        
        if len(st.session_state.bina_genel_envanteri) == 0:
            st.info("Bina listesinde henüz kayıtlı unsur yok. Sol taraftaki menüyü kullanarak bina ekipmanlarını (yangın tüpleri, kazanlar, kurutucular vb.) seçip ekleyin.")
        else:
            df_bina = pd.DataFrame(st.session_state.bina_genel_envanteri)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Toplam Değerlendirilen Ekipman/Unsur", len(df_bina))
            c2.metric("Acil Eylem Gerektiren Riskler (Öncelik 1)", len(df_bina[df_bina["Nihai Risk Önceliği"].str.contains("Öncelik 1")]))
            c3.metric("Yöntemsel Sapma / Kör Nokta Uyarısı", len(df_bina[df_bina["Çapraz Doğrulama Uyarısı"].str.contains("UYARI")]))

            st.dataframe(df_bina, use_container_width=True)

            csv_data = df_bina.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 E Blok Tüm Bina İSG Risk Analizi Raporunu CSV Olarak İndir", data=csv_data, file_name="E_Blok_Tum_Bina_İSG_Risk_Analizi.csv", mime="text/csv")
            
            if st.button("🗑️ Tüm Kayıtları Sıfırla"):
                st.session_state.bina_genel_envanteri = []
                st.rerun()

    with tab2:
        st.subheader(f"📍 Seçilen Mekân: {lab_adi}")
        if secilen_unsurlar:
            for item_name in secilen_unsurlar:
                item_info = df_inv[df_inv["Unsur"] == item_name].iloc[0]
                O_matris, O_kinney = calculate_probability_score(fiziksel_durum, kkd_durumu, deneyim_durumu)
                S_matris = calculate_matrix_severity(item_info["D_Skoru"])
                F_kinney = calculate_fine_kinney_frequency(t_hours)
                D_kinney = item_info["D_Skoru"]

                m_score = O_matris * S_matris
                k_score = O_kinney * F_kinney * D_kinney
                status, flag, priority = cross_validation_harmonization(m_score, k_score, S_matris)

                with st.expander(f"⚙️ **{item_name}** ({item_info['Kategori']}) - Risk Önceliği: {priority}", expanded=True):
                    st.write(f"**Tehlike Tanımı:** {item_info['Tehlike_Turu']}")
                    
                    col1, col2 = st.columns(2)
                    col1.metric("5x5 Matris Risk Skoru (R=O×Ş)", f"{m_score} / 25")
                    col2.metric("Fine-Kinney Risk Skoru (R=O×F×D)", f"{k_score:.1f}")

                    if flag > 0:
                        st.error(f"⚠️ {status}")
                    else:
                        st.success(f"✅ {status}")

                    st.markdown("**🛡️ Tavsiye Edilen Risk Kontrol Önlem Planı:**")
                    actions = generate_action_plan(item_info, priority, flag, fiziksel_durum)
                    for act in actions:
                        st.write(act)

if __name__ == "__main__":
    main()
