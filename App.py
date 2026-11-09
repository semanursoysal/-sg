import streamlit as st
import pandas as pd
import numpy as np

def get_chemical_database():
    data = [
        {"Kimyasal": "n-Hekzan", "Kategori": "Solvent", "H_Kodlari": "H225, H304, H315, H336, H361f, H373", "Parlama_Noktasi": -22, "STEL_ppm": 50, "IDLH_ppm": 1100, "D_Skoru": 40},
        {"Kimyasal": "Toluen", "Kategori": "Solvent", "H_Kodlari": "H225, H304, H315, H336, H361d, H373", "Parlama_Noktasi": 4, "STEL_ppm": 150, "IDLH_ppm": 500, "D_Skoru": 40},
        {"Kimyasal": "Aseton", "Kategori": "Solvent", "H_Kodlari": "H225, H319, H336", "Parlama_Noktasi": -20, "STEL_ppm": 500, "IDLH_ppm": 2500, "D_Skoru": 15},
        {"Kimyasal": "Dietil Eter", "Kategori": "Solvent", "H_Kodlari": "H224, H302, H336, EUH019", "Parlama_Noktasi": -45, "STEL_ppm": 200, "IDLH_ppm": 1900, "D_Skoru": 40},
        {"Kimyasal": "Metanol", "Kategori": "Solvent", "H_Kodlari": "H225, H301, H311, H331, H370", "Parlama_Noktasi": 9.7, "STEL_ppm": 250, "IDLH_ppm": 6000, "D_Skoru": 70},
        {"Kimyasal": "Etanol", "Kategori": "Solvent", "H_Kodlari": "H225, H319", "Parlama_Noktasi": 13, "STEL_ppm": 1000, "IDLH_ppm": 3300, "D_Skoru": 7},
        {"Kimyasal": "Kloroform", "Kategori": "Solvent", "H_Kodlari": "H302, H315, H319, H331, H351, H361d, H372", "Parlama_Noktasi": None, "STEL_ppm": 50, "IDLH_ppm": 500, "D_Skoru": 70},
        {"Kimyasal": "Diklormetan (DCM)", "Kategori": "Solvent", "H_Kodlari": "H315, H319, H335, H336, H351", "Parlama_Noktasi": None, "STEL_ppm": 125, "IDLH_ppm": 2300, "D_Skoru": 40},
        {"Kimyasal": "Tetrahidrofuran (THF)", "Kategori": "Solvent", "H_Kodlari": "H225, H319, H335, H351, EUH019", "Parlama_Noktasi": -14.5, "STEL_ppm": 100, "IDLH_ppm": 2000, "D_Skoru": 40},
        {"Kimyasal": "Acetonitrile", "Kategori": "Solvent", "H_Kodlari": "H225, H302, H312, H319, H332", "Parlama_Noktasi": 2, "STEL_ppm": 60, "IDLH_ppm": 500, "D_Skoru": 40},
        {"Kimyasal": "Izopropanol (IPA)", "Kategori": "Solvent", "H_Kodlari": "H225, H319, H336", "Parlama_Noktasi": 12, "STEL_ppm": 400, "IDLH_ppm": 2000, "D_Skoru": 15},
        {"Kimyasal": "Ksilen", "Kategori": "Solvent", "H_Kodlari": "H226, H312, H315, H332", "Parlama_Noktasi": 25, "STEL_ppm": 150, "IDLH_ppm": 900, "D_Skoru": 15},
        {"Kimyasal": "DMF (Dimetilformamid)", "Kategori": "Solvent", "H_Kodlari": "H226, H312, H319, H332, H360D", "Parlama_Noktasi": 57, "STEL_ppm": 10, "IDLH_ppm": 500, "D_Skoru": 70},
        {"Kimyasal": "DMSO (Dimetilsülfoksit)", "Kategori": "Solvent", "H_Kodlari": "H315, H319", "Parlama_Noktasi": 87, "STEL_ppm": None, "IDLH_ppm": None, "D_Skoru": 7},
        {"Kimyasal": "Derişik Hidroklorik Asit (HCl %37)", "Kategori": "Asit/Baz", "H_Kodlari": "H290, H314, H335", "Parlama_Noktasi": None, "STEL_ppm": 5, "IDLH_ppm": 50, "D_Skoru": 40},
        {"Kimyasal": "Derişik Sülfürik Asit (H2SO4 %98)", "Kategori": "Asit/Baz", "H_Kodlari": "H290, H314", "Parlama_Noktasi": None, "STEL_ppm": 3, "IDLH_ppm": 15, "D_Skoru": 70},
        {"Kimyasal": "Derişik Nitrik Asit (HNO3 %65)", "Kategori": "Asit/Baz", "H_Kodlari": "H272, H290, H314, H331", "Parlama_Noktasi": None, "STEL_ppm": 4, "IDLH_ppm": 25, "D_Skoru": 70},
        {"Kimyasal": "Buzlu Asetik Asit", "Kategori": "Asit/Baz", "H_Kodlari": "H226, H314", "Parlama_Noktasi": 39, "STEL_ppm": 15, "IDLH_ppm": 50, "D_Skoru": 40},
        {"Kimyasal": "Sodyum Hidroksit (NaOH - Pelet/Çözelti)", "Kategori": "Asit/Baz", "H_Kodlari": "H290, H314", "Parlama_Noktasi": None, "STEL_ppm": None, "IDLH_ppm": 10, "D_Skoru": 40},
        {"Kimyasal": "Amonyum Hidroksit (NH4OH %28)", "Kategori": "Asit/Baz", "H_Kodlari": "H314, H335, H400", "Parlama_Noktasi": None, "STEL_ppm": 35, "IDLH_ppm": 300, "D_Skoru": 40},
        {"Kimyasal": "Hidroflorik Asit (HF %48)", "Kategori": "Asit/Baz", "H_Kodlari": "H300, H310, H330, H314", "Parlama_Noktasi": None, "STEL_ppm": 6, "IDLH_ppm": 30, "D_Skoru": 100},
        {"Kimyasal": "Hidrojen Peroksit (H2O2 %30)", "Kategori": "Reaktif", "H_Kodlari": "H302, H318, H332", "Parlama_Noktasi": None, "STEL_ppm": 1, "IDLH_ppm": 75, "D_Skoru": 40},
        {"Kimyasal": "Sodyum Siyanür (NaCN)", "Kategori": "Reaktif", "H_Kodlari": "H300, H310, H330, H410", "Parlama_Noktasi": None, "STEL_ppm": 4.7, "IDLH_ppm": 25, "D_Skoru": 100},
        {"Kimyasal": "Formaldehit (%37 Çözelti)", "Kategori": "Reaktif", "H_Kodlari": "H301, H311, H314, H317, H331, H341, H350", "Parlama_Noktasi": 64, "STEL_ppm": 2, "IDLH_ppm": 20, "D_Skoru": 70},
        {"Kimyasal": "Sodyum Azür (NaN3)", "Kategori": "Reaktif", "H_Kodlari": "H300, H310, H410, EUH032", "Parlama_Noktasi": None, "STEL_ppm": 0.11, "IDLH_ppm": 5, "D_Skoru": 100}
    ]
    return pd.DataFrame(data)

def calculate_fine_kinney_frequency(t_hours):
    if t_hours >= 30: return 10.0
    elif 10 <= t_hours < 30: return 6.0
    elif 3 <= t_hours < 10: return 3.0
    elif 1 <= t_hours < 3: return 2.0
    elif 0.25 <= t_hours < 1: return 1.0
    else: return 0.5

def calculate_probability_score(fume_hood, kkd_level, experience_level):
    base_prob = 3.0
    if fume_hood == "Aktif / Çalışıyor": base_prob -= 1.0
    elif fume_hood == "Yok / Pasif": base_prob += 1.0
    if kkd_level == "Tam (Gözlük, Önlük, Kimyasal Eldiven, Maske)": base_prob -= 0.5
    elif kkd_level == "Eksik / Standarda Uygun Değil": base_prob += 1.0
    if experience_level == "Deneyimli Araştırmacı / Personel": base_prob -= 0.5
    elif experience_level == "Lisans Öğrencisi / Acemi": base_prob += 0.5

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

def cross_validation_harmonization(matrix_score, kinney_score, S_matris, F_kinney):
    status = "Normal Uyum"
    flag_code = 0
    final_priority = "Öncelik 3 - Rutin Kontrol"

    if matrix_score < 15 and kinney_score >= 200:
        status = "UYARI: Frekans Kör Noktası Yakalandı! (Kümülatif Maruziyet Yüksek)"
        flag_code = 1
        final_priority = "Öncelik 1 - Acil Eylem Gerektirir"
    elif matrix_score >= 15 and kinney_score < 70 and S_matris >= 4:
        status = "UYARI: Şiddet Seyrelmesi Sapması Yakalandı! (Seyrek Ama Ölümcül Tehlike)"
        flag_code = 2
        final_priority = "Öncelik 1 - Kritik Prosedür Şartı"
    else:
        if matrix_score >= 15 or kinney_score >= 320: final_priority = "Öncelik 1 - Acil Eylem"
        elif matrix_score >= 8 or kinney_score >= 70: final_priority = "Öncelik 2 - Önemli Risk"
        else: final_priority = "Öncelik 3 - Rutin Kontrol"

    return status, flag_code, final_priority

def generate_risk_control_actions(chem_row, final_priority, flag_code, fume_hood, kkd_level):
    actions = []
    if "H350" in chem_row['H_Kodlari'] or "H341" in chem_row['H_Kodlari'] or final_priority.startswith("Öncelik 1"):
        actions.append(f"**1. İkame Adımı:** {chem_row['Kimyasal']} yüksek risk taşımaktadır. Mümkünse daha az tehlikeli bir muadili ile ikame edilmelidir (6331 SK / Kimyasal Maddeler Yön. Md. 7).")
    if fume_hood == "Yok / Pasif" or (chem_row['Parlama_Noktasi'] is not None and chem_row['Parlama_Noktasi'] < 21):
        actions.append(f"**2. Mühendislik Önlemi:** Çalışma mutlak suretle **aktif lokal cebri havalandırmalı (çektiricili) Çeker Ocak** altında yürütülmelidir.")
    else:
        actions.append("**2. Mühendislik Önlemi:** Çeker ocak emiş hızı ve havalandırma debisi periyodik olarak doğrulanmalıdır.")
    if flag_code == 1:
        actions.append("**3. İdari Önlem (Kümülatif Maruziyet):** Haftalık çalışma süresi kısıtlanmalı, araştırmacılar arasında rotasyon uygulanmalıdır.")
    elif flag_code == 2:
        actions.append("**3. İdari Önlem (Kritik Prosedür):** İşlem öncesi 'Çok Tehlikeli İş İzin Formu' doldurulmalı ve denetçi gözetiminde çalışılmalıdır.")
    else:
        actions.append("**3. İdari Önlem:** Standart Çalışma Prosedürleri (SÖP) ve SDS formları çalışma alanında görünür kılınmalıdır.")
    if kkd_level != "Tam (Gözlük, Önlük, Kimyasal Eldiven, Maske)":
        actions.append(f"**4. KKD Standardı:** {chem_row['Kimyasal']} için standart önlüğe ek olarak EN 374 onaylı kimyasal eldiven ve organik buhar filtreli maske zorunludur.")
    else:
        actions.append("**4. KKD Standardı:** Mevcut KKD kullanımı uygundur.")
    return actions

def main():
    st.set_page_config(page_title="İSG Hibrit KDS Prototipi", layout="wide", page_icon="🧪")
    st.title("🧪 Ankara Üniversitesi Kimya Mühendisliği Bölümü (E Blok)")
    st.caption("Hibrit Risk Analizi (5x5 Matris / Fine-Kinney) Tabanlı Dinamik Karar Destek Sistemi")
    st.markdown("---")

    df_chem = get_chemical_database()
    st.sidebar.header("📋 Senaryo Parametreleri")
    selected_chem_name = st.sidebar.selectbox("1. Kimyasal Madde Seçimi:", df_chem["Kimyasal"].unique())
    chem_info = df_chem[df_chem["Kimyasal"] == selected_chem_name].iloc[0]

    t_hours = st.sidebar.slider("2. Haftalık Kullanım Süresi (Saat/Hafta):", min_value=0.1, max_value=40.0, value=8.0, step=0.5)
    fume_hood = st.sidebar.radio("3. Çeker Ocak Durumu:", ["Aktif / Çalışıyor", "Yok / Pasif"])
    kkd_level = st.sidebar.radio("4. KKD Kullanım Düzeyi:", ["Tam (Gözlük, Önlük, Kimyasal Eldiven, Maske)", "Eksik / Standarda Uygun Değil"])
    experience_level = st.sidebar.radio("5. Operatör Denetim/Deneyim Düzeyi:", ["Deneyimli Araştırmacı / Personel", "Lisans Öğrencisi / Acemi"])

    O_matris, O_kinney = calculate_probability_score(fume_hood, kkd_level, experience_level)
    S_matris = calculate_matrix_severity(chem_info["D_Skoru"])
    F_kinney = calculate_fine_kinney_frequency(t_hours)
    D_kinney = chem_info["D_Skoru"]

    matrix_score = O_matris * S_matris
    kinney_score = O_kinney * F_kinney * D_kinney
    status, flag_code, final_priority = cross_validation_harmonization(matrix_score, kinney_score, S_matris, F_kinney)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.subheader("📌 Seçilen Kimyasal")
        st.write(f"**Kimyasal:** {chem_info['Kimyasal']} ({chem_info['Kategori']})")
        st.write(f"**H-Kodları:** `{chem_info['H_Kodlari']}`")
        st.write(f"**STEL:** {chem_info['STEL_ppm']} ppm | **IDLH:** {chem_info['IDLH_ppm']} ppm")
    with col2:
        st.subheader("📊 5x5 Matris Sonucu")
        st.metric(label="Matris Skoru", value=f"{matrix_score} / 25")
    with col3:
        st.subheader("📈 Fine-Kinney Sonucu")
        st.metric(label="Kinney Skoru", value=f"{kinney_score:.1f}")

    st.markdown("---")
    st.subheader("🔄 Çapraz Doğrulama & Harmonizasyon")
    if flag_code > 0: st.error(f"⚠️ **SİSTEM TESPİTİ:** {status}")
    else: st.success(f"✅ **SİSTEM TESPİTİ:** {status}")

    st.info(f"🎯 **Nihai Karar Destek Seviyesi:** **{final_priority}**")
    st.subheader("🛡️ 6331 Sayılı İSG Kanunu Uygun Önlem Planı")
    actions = generate_risk_control_actions(chem_info, final_priority, flag_code, fume_hood, kkd_level)
    for act in actions: st.write(act)

if __name__ == "__main__":
    main()

