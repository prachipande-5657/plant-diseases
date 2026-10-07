"""
Plant Leaf Disease Detection & Diagnosis Platform (KrishiScan / PhytoScan)
Farmer-friendly AI diagnostics with crop selection, simplified language,
and robust advisory report generation & download.
"""

import os
import io
import time
import re
from datetime import datetime
from PIL import Image
import streamlit as st

from disease_analyzer import diagnose_leaf, PlantAnalysisOutput
from disease_database import COMMON_CROPS, list_known_diseases
from pdf_generator import build_advisory_pdf

# Page configuration
st.set_page_config(
    page_title="KrishiScan | Fasal Rog Pehchan (Crop Disease Detector)",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for modern green / farmer-friendly nature theme
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;1,600&display=swap');

    :root {
        --primary-green: #15803d;
        --accent-emerald: #10b981;
        --light-sage: #f0fdf4;
        --leaf-dark: #14532d;
        --border-green: #bbf7d0;
        --card-shadow: 0 4px 18px rgba(22, 101, 52, 0.08);
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1220px;
    }

    /* Hero Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, #14532d 0%, #15803d 50%, #16a34a 100%);
        color: #ffffff;
        padding: 2rem 2.2rem;
        border-radius: 18px;
        margin-bottom: 1.8rem;
        box-shadow: 0 8px 25px rgba(20, 83, 45, 0.2);
        position: relative;
        overflow: hidden;
    }

    .hero-banner::after {
        content: "🌾";
        position: absolute;
        right: 25px;
        bottom: -15px;
        font-size: 100px;
        opacity: 0.18;
        pointer-events: none;
    }

    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
        color: #ffffff !important;
        letter-spacing: -0.5px;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #dcfce7;
        max-width: 820px;
        line-height: 1.5;
        margin: 0;
    }

    /* Section Step Header */
    .step-header {
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--leaf-dark);
        margin-top: 0.4rem;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Feature Cards */
    .feature-card {
        background: #ffffff;
        border: 1px solid var(--border-green);
        border-radius: 16px;
        padding: 1.4rem;
        box-shadow: var(--card-shadow);
        margin-bottom: 1rem;
    }

    /* Report Download Box */
    .download-card {
        background: #f8fafc;
        border: 2px dashed #86efac;
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    /* Status Badges */
    .status-badge-healthy {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: white;
        padding: 0.8rem 1.4rem;
        border-radius: 14px;
        font-weight: 700;
        font-size: 1.25rem;
        display: inline-flex;
        align-items: center;
        gap: 0.6rem;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35);
    }

    .status-badge-infected {
        background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
        color: white;
        padding: 0.8rem 1.4rem;
        border-radius: 14px;
        font-weight: 700;
        font-size: 1.25rem;
        display: inline-flex;
        align-items: center;
        gap: 0.6rem;
        box-shadow: 0 4px 14px rgba(239, 68, 68, 0.35);
    }

    /* Step items */
    .step-item-org {
        background: #f0fdf4;
        border-left: 5px solid #16a34a;
        padding: 0.85rem 1.1rem;
        border-radius: 0 12px 12px 0;
        margin-bottom: 0.7rem;
        font-size: 0.98rem;
        line-height: 1.5;
        color: #14532d;
    }

    .step-item-chem {
        background: #eff6ff;
        border-left: 5px solid #2563eb;
        padding: 0.85rem 1.1rem;
        border-radius: 0 12px 12px 0;
        margin-bottom: 0.7rem;
        font-size: 0.98rem;
        line-height: 1.5;
        color: #1e3a8a;
    }

    .step-item-prev {
        background: #fffbeb;
        border-left: 5px solid #d97706;
        padding: 0.85rem 1.1rem;
        border-radius: 0 12px 12px 0;
        margin-bottom: 0.7rem;
        font-size: 0.98rem;
        line-height: 1.5;
        color: #78350f;
    }

    /* Crop Tag Pill */
    .crop-tag-pill {
        display: inline-block;
        background: #dcfce7;
        color: #166534;
        border: 1px solid #86efac;
        padding: 0.35rem 0.9rem;
        border-radius: 30px;
        font-size: 0.95rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    /* Sidebar Tip Box */
    .sidebar-tip-box {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    .sidebar-tip-title {
        font-weight: 700;
        color: #166534;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }

    .tip-bullet {
        font-size: 0.86rem;
        color: #374151;
        line-height: 1.5;
        margin-bottom: 0.4rem;
    }

    .pill-tag {
        display: inline-block;
        background: #f3f4f6;
        color: #374151;
        border: 1px solid #d1d5db;
        padding: 0.25rem 0.7rem;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
    }

    .stButton>button {
        border-radius: 12px;
        font-weight: 700;
        padding: 0.65rem 1.3rem;
        font-size: 1.05rem;
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ---------------- REPORT FORMATTING UTILITIES ----------------
def extract_report_dict(result) -> dict:
    """Safely convert result object (Pydantic model, dict, or generic object) to dictionary."""
    if hasattr(result, "to_report_dict"):
        try:
            return result.to_report_dict()
        except Exception:
            pass

    if hasattr(result, "model_dump"):
        try:
            data = result.model_dump()
        except Exception:
            data = {}
    elif isinstance(result, dict):
        data = dict(result)
    else:
        data = {}

    if not data:
        data = {
            "crop_name": getattr(result, "crop_name", "Fasal (Crop)"),
            "health_status": getattr(result, "health_status", "Infected"),
            "disease_name": getattr(result, "disease_name", "Crop Leaf Issue"),
            "confidence": getattr(result, "confidence", 0.9),
            "severity": getattr(result, "severity", "Moderate"),
            "symptoms_observed": getattr(result, "symptoms_observed", []),
            "root_cause": getattr(result, "root_cause", ""),
            "organic_remedies": getattr(result, "organic_remedies", []),
            "chemical_remedies": getattr(result, "chemical_remedies", []),
            "preventive_measures": getattr(result, "preventive_measures", []),
            "engine_used": getattr(result, "engine_used", "AI"),
        }

    conf = data.get("confidence", 0.9)
    if isinstance(conf, float) and conf <= 1.0:
        conf = int(conf * 100)

    return {
        "crop_name": data.get("crop_name") or "Fasal (Crop)",
        "health_status": data.get("health_status") or "Infected",
        "disease_name": data.get("disease_name") or "Crop Leaf Issue",
        "confidence": conf,
        "severity": data.get("severity") or "Moderate",
        "symptoms_observed": list(data.get("symptoms_observed") or []),
        "root_cause": data.get("root_cause") or "Karan darj nahi hai.",
        "organic_remedies": list(data.get("organic_remedies") or []),
        "chemical_remedies": list(data.get("chemical_remedies") or []),
        "preventive_measures": list(data.get("preventive_measures") or []),
        "engine_used": data.get("engine_used") or "KrishiScan AI",
        "timestamp": datetime.now().strftime("%d-%m-%Y %I:%M %p")
    }


def generate_advisory_report_txt(data: dict) -> str:

    """Generate a clean, printable ASCII/Unicode advisory slip (.txt)."""
    ts = data.get("timestamp", datetime.now().strftime("%d-%m-%Y %I:%M %p"))
    crop = data.get("crop_name", "N/A")
    status = data.get("health_status", "N/A")
    disease = data.get("disease_name", "N/A")
    conf = data.get("confidence", 90)
    sev = data.get("severity", "N/A")
    engine = data.get("engine_used", "KrishiScan AI")
    cause = data.get("root_cause", "Karan darj nahi hai.")

    symptoms = [str(s) for s in data.get("symptoms_observed", []) if s]
    organic = [str(r) for r in data.get("organic_remedies", []) if r]
    chemical = [str(c) for c in data.get("chemical_remedies", []) if c]
    prev = [str(p) for p in data.get("preventive_measures", []) if p]

    border = "=" * 70
    sub_border = "-" * 70

    lines = [
        border,
        "          KRISHISCAN - FASAL ROG SALAH PARCHI (ADVISORY SLIP)          ",
        "          Plant Health Diagnosis & Farmer Recommendation Slip          ",
        border,
        f" Taarikh / Date        : {ts}",
        f" Fasal / Crop Name     : {crop}",
        f" Sthiti / Health Status: {status}",
        f" Rog / Disease Name    : {disease}",
        f" Vishwasniyata / Conf  : {conf}%",
        f" Gambhirta / Severity  : {sev}",
        f" AI Engine Used        : {engine}",
        sub_border,
        "",
        " [1] BIMARI KYUN HUI? (WHY IT HAPPENED / REASON):",
        "-" * 49,
        f" {cause}",
        "",
    ]

    if symptoms:
        lines.append(" [2] PATTE PAR DIKHNE WALE LAKSHAN (OBSERVED SYMPTOMS):")
        lines.append("-" * 55)
        for s in symptoms:
            lines.append(f"  * {s}")
        lines.append("")

    lines.append(" [3] GHARELU / JAIVIK UPCHAAR (ORGANIC & BIOLOGICAL REMEDIES):")
    lines.append("-" * 62)
    if organic:
        for i, r in enumerate(organic, 1):
            lines.append(f"  {i}. {r}")
    else:
        lines.append("  * Fasal swasth hai, kisi upchaar ki aavashyakta nahi hai.")
    lines.append("")

    lines.append(" [4] DAWAI / RASAYANIK UPCHAAR (CHEMICAL REMEDIES & SPRAYS):")
    lines.append("-" * 60)
    if chemical:
        for i, c in enumerate(chemical, 1):
            lines.append(f"  {i}. {c}")
        lines.append("  NOTE: Chhidkaav karte samay muh par mask/gamchha lagayein.")
        lines.append("        Phal todne se 7-10 din pehle chhidkaav band karein.")
    else:
        lines.append("  * Fasal swasth hai, kisi chemical dawai ki zaroorat nahi hai.")
    lines.append("")

    lines.append(" [5] BHAVISHYA ME BACHAV KE NIYAM (PREVENTIVE MEASURES):")
    lines.append("-" * 56)
    if prev:
        for i, p in enumerate(prev, 1):
            lines.append(f"  {i}. {p}")
    else:
        lines.append("  * Niyamit roop se fasal ki dekhbhal karein.")
    lines.append("")

    lines.extend([
        border,
        " KrishiScan AI Platform • Kisan Sahayak (Farmer Advisory)",
        " Sujhav: Gambhir sthiti me najdeeki Krishi Vigyan Kendra (KVK) se sampark karein.",
        border,
    ])

    return "\n".join(lines)


def generate_advisory_report_md(data: dict) -> str:
    """Generate a clean Markdown advisory report (.md)."""
    ts = data.get("timestamp", datetime.now().strftime("%d-%m-%Y %I:%M %p"))
    crop = data.get("crop_name", "N/A")
    status = data.get("health_status", "N/A")
    disease = data.get("disease_name", "N/A")
    conf = data.get("confidence", 90)
    sev = data.get("severity", "N/A")
    engine = data.get("engine_used", "KrishiScan AI")
    cause = data.get("root_cause", "Karan darj nahi hai.")

    symptoms = [str(s) for s in data.get("symptoms_observed", []) if s]
    organic = [str(r) for r in data.get("organic_remedies", []) if r]
    chemical = [str(c) for c in data.get("chemical_remedies", []) if c]
    prev = [str(p) for p in data.get("preventive_measures", []) if p]

    md_lines = [
        "# 🌾 KrishiScan: Fasal Rog Salah Parchi (Advisory Slip)",
        f"**Taarikh (Date):** {ts}  ",
        f"**Fasal (Crop):** {crop}  ",
        f"**Sthiti (Health Status):** {status}  ",
        f"**Bimari Ka Naam (Disease Name):** {disease}  ",
        f"**Vishwasniyata (Confidence):** {conf}% | **Gambhirta (Severity):** {sev}  ",
        f"**Engine Used:** {engine}  ",
        "",
        "---",
        "",
        "## ❓ 1. Bimari Kyun Hui? (Why It Happened / Reason)",
        cause,
        "",
    ]

    if symptoms:
        md_lines.append("## 🔎 2. Patte Par Dikhne Wale Lakshan (Symptoms)")
        for s in symptoms:
            md_lines.append(f"- {s}")
        md_lines.append("")

    md_lines.append("## 🌿 3. Gharelu / Jaivik Upchaar (Organic Remedies)")
    if organic:
        for i, r in enumerate(organic, 1):
            md_lines.append(f"{i}. {r}")
    else:
        md_lines.append("- Fasal swasth hai, kisi upchaar ki aavashyakta nahi hai.")
    md_lines.append("")

    md_lines.append("## 🧪 4. Dawai / Rasayanik Upchaar (Chemical Remedies)")
    if chemical:
        for i, c in enumerate(chemical, 1):
            md_lines.append(f"{i}. {c}")
        md_lines.append("\n> ⚠️ *Chhidkaav karte samay muh par mask lagayein aur sahi matra ka dhyan rakhein.*")
    else:
        md_lines.append("- Fasal swasth hai, kisi chemical spray ki zaroorat nahi hai.")
    md_lines.append("")

    md_lines.append("## 🛡️ 5. Bachav Ke Niyam (Prevention Tips)")
    if prev:
        for i, p in enumerate(prev, 1):
            md_lines.append(f"{i}. {p}")
    else:
        md_lines.append("- Niyamit roop se fasal ki niraai-gudaai karein aur paani sahi tarike se dein.")
    md_lines.append("")

    md_lines.extend([
        "---",
        "*KrishiScan AI Platform • Apki Fasal, Hamari Dekhbhal*",
        "*Sujhav: Badi matra me dawai dalne se pehle Krishi Adhikari se salah zaroor lein.*"
    ])

    return "\n".join(md_lines)


# ---------------- INITIALIZE SESSION STATE ----------------
# Storing all report fields safely in session state so re-runs never lose state
if "report_data" not in st.session_state:
    st.session_state["report_data"] = None
if "report_pdf_bytes" not in st.session_state:
    st.session_state["report_pdf_bytes"] = None
if "report_txt" not in st.session_state:
    st.session_state["report_txt"] = ""
if "report_md" not in st.session_state:
    st.session_state["report_md"] = ""
if "report_filename_base" not in st.session_state:
    st.session_state["report_filename_base"] = "kisan_salah"
if "active_image" not in st.session_state:
    st.session_state["active_image"] = None
if "selected_sample_label" not in st.session_state:
    st.session_state["selected_sample_label"] = None


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("### 🌱 KrishiScan (कृषिसकैन)")
    st.caption("Fasal Rog Pehchan & Upchaar Salahkar (Crop Disease Doctor)")
    
    st.divider()

    # AI Engine Controls
    st.markdown("#### ⚙️ AI Engine Settings")
    env_key = os.environ.get("GEMINI_API_KEY", "")
    api_key_input = st.text_input(
        "Google Gemini API Key (Optional)",
        value=env_key,
        type="password",
        help="Agar aapke paas Gemini API Key hai toh daalein. Khali chhodne par bhi offline computer vision engine kaam karega.",
        placeholder="AIzaSy..."
    )

    model_choice = st.selectbox(
        "Gemini Vision Model",
        options=["gemini-3.8-flash", "gemini-3.5-flash-lite"],
        index=0,
        help="gemini-3.8-flash: Tezi se aur sahi jaanch ke liye sabse behtar model."
    )

    force_offline = st.checkbox(
        "Offline Mode me chalayein (No API calls)",
        value=False if api_key_input else True,
        help="Tick karne par bina internet / bina API key ke local computer vision engine se jaanch hogi."
    )

    if not force_offline and api_key_input.strip():
        st.success("⚡ Active: Google Gemini Vision AI (Cloud)")
    else:
        st.info("🔬 Active: Smart Offline Krishi Engine (Local)")

    st.divider()

    # Photography Guide in Simple Hindi/Hinglish
    st.markdown("#### 📸 Achhi Photo Kaise Khinchein?")
    st.markdown(
        """
        <div class="sidebar-tip-box">
            <div class="sidebar-tip-title">🎯 Sahi Natije Ke Liye 5 Zaroori Baatein:</div>
            <div class="tip-bullet"><b>1. Saaf Dhoop:</b> Photo hamesha achhi roshni me lein taaki patte ka asli rang dikhe.</div>
            <div class="tip-bullet"><b>2. Dhabbe par Focus:</b> Phone camera ko dhabbe ya fafund ke paas le jakar saaf focus karein.</div>
            <div class="tip-bullet"><b>3. Ek Akela Patta:</b> Koshish karein ki photo me sirf ek patta saaf dikhe, peeche mitti ya ghaas zyada na ho.</div>
            <div class="tip-bullet"><b>4. Poori Patti:</b> Patte ke kinaray aur nok (tip) photo me poori tarah aani chahiye.</div>
            <div class="tip-bullet"><b>5. Patti ka Nichla Hissa:</b> Zang (rust) ya fafund ke liye patte ke peeche ki photo bhi le sakte hain.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Simple Disease Guide in Sidebar
    with st.expander("📚 Mukhya Bimariyon Ki List", expanded=False):
        st.write("KrishiScan in mukhya bimariyon ko pehchanta hai:")
        diseases = list_known_diseases()
        for d in diseases:
            st.markdown(f"- **{d['simple_name']}**")

    st.divider()
    st.caption("🌾 KrishiScan v2.6 • Saral Kisan Salahkar")
    st.caption("Sujhav: Badi matra me khet me dawai chhidakne se pehle najdeeki Krishi Vigyan Kendra (KVK) se salah lein.")


# ---------------- MAIN HERO BANNER ----------------
st.markdown(
    """
    <div class="hero-banner">
        <div class="hero-title">🌱 Fasal Rog Pehchan & Upchaar</div>
        <div class="hero-subtitle">
            Apni fasal chunein aur patte ki photo upload karein. Hamara AI turant saral bhasha me batayega ki fasal ko <b>kaun si bimari hai</b>, <b>kyun hui hai</b>, aur uske <b>gharelu (organic) aur chemical upchaar</b> kya hain.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------- WORKSPACE: 2 COLUMNS ----------------
col_left, col_right = st.columns([1.1, 0.9], gap="large")

SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "sample_images")
SAMPLE_OPTIONS = {
    "-- Test karne ke liye sample chunein --": None,
    "🍅 Tomato Early Blight (Tamatar me Bhoore Dhabbe)": ("tomato", "early_blight_leaf.jpg"),
    "🍅 Healthy Tomato Leaf (Swasth Tamatar ka Patta)": ("tomato", "healthy_tomato_leaf.jpg"),
    "🥒 Powdery Mildew (Safed Churni Fafund)": ("general", "powdery_mildew_leaf.jpg"),
    "🌽 Corn Leaf Rust (Makka me Gerua/Zang Rog)": ("corn", "common_rust_leaf.jpg"),
}

with col_left:
    # 1. CROP SELECTION
    st.markdown('<div class="step-header">🌾 1. Fasal Chunein (Select Crop Type)</div>', unsafe_allow_html=True)
    
    crop_options = [c["name"] for c in COMMON_CROPS]
    selected_crop_name = st.selectbox(
        "Fasal ka Chayan Karein (Select Your Crop):",
        options=crop_options,
        index=0,
        help="Apni fasal chunein taaki AI aur behtar jaanch kar sake."
    )

    st.markdown('<div class="step-header" style="margin-top:1.2rem;">📤 2. Patte Ki Photo Dalein (Upload Leaf)</div>', unsafe_allow_html=True)

    # 1-Click Sample Selector
    sample_choice = st.selectbox(
        "⚡ Ya bana-banaya sample patta test karein:",
        options=list(SAMPLE_OPTIONS.keys()),
        index=0,
        help="Bina photo upload kiye turant check karne ke liye sample chunein."
    )

    st.markdown("<p style='text-align:center; color:#6b7280; font-size:0.9rem; margin:0.4rem 0;'>— YA APNE KHET KE PATTE KI PHOTO UPLOAD KAREIN —</p>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Patte ki photo chunein ya yahan kheencher layein (JPG, JPEG, PNG)",
        type=["jpg", "jpeg", "png"],
        key="leaf_uploader_widget"
    )

    current_image = None
    image_label = ""

    if uploaded_file is not None:
        try:
            current_image = Image.open(uploaded_file).convert("RGB")
            image_label = f"Uploaded Photo: {uploaded_file.name} ({current_image.size[0]}×{current_image.size[1]} px)"
            st.session_state["active_image"] = current_image
            st.session_state["selected_sample_label"] = None
        except Exception as e:
            st.error(f"Photo load karne me dikkat hui: {e}")
    elif sample_choice != "-- Test karne ke liye sample chunein --":
        sample_info = SAMPLE_OPTIONS[sample_choice]
        if sample_info is not None:
            crop_hint, sample_filename = sample_info
            sample_path = os.path.join(SAMPLE_DIR, sample_filename)
            if os.path.exists(sample_path):
                current_image = Image.open(sample_path).convert("RGB")
                image_label = f"Sample Leaf: {sample_choice}"
                st.session_state["active_image"] = current_image
                st.session_state["selected_sample_label"] = sample_choice
    elif st.session_state.get("active_image") is not None:
        current_image = st.session_state["active_image"]
        image_label = "Current active specimen"

    # Action Buttons
    st.markdown("<br>", unsafe_allow_html=True)
    btn_disabled = current_image is None
    
    col_act1, col_act2 = st.columns([2, 1])
    with col_act1:
        analyze_clicked = st.button(
            "🌿 Bimari Ki Jaanch Karein (Analyze Leaf)",
            type="primary",
            use_container_width=True,
            disabled=btn_disabled,
            help="Patte ki bimari pehchanne ke liye click karein."
        )
    with col_act2:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state["report_data"] = None
            st.session_state["report_pdf_bytes"] = None
            st.session_state["report_txt"] = ""
            st.session_state["report_md"] = ""
            st.session_state["active_image"] = None
            st.session_state["selected_sample_label"] = None
            st.rerun()


with col_right:
    st.markdown('<div class="step-header">👁️ Patte Ka Preview (Selected Leaf)</div>', unsafe_allow_html=True)
    if current_image is not None:
        st.image(
            current_image,
            caption=image_label,
            use_container_width=True
        )
        st.caption(f"Selected Crop: {selected_crop_name} | Size: {current_image.size[0]}×{current_image.size[1]} px")
    else:
        st.info("👆 Kripya upar se apni fasal chunein aur patte ki photo upload karein ya sample chunein.")


# ---------------- EXECUTE ANALYSIS & STORE IN SESSION STATE ----------------
if analyze_clicked and current_image is not None:
    with st.spinner(f"🔍 {selected_crop_name} ke patte ki jaanch ho rahi hai, kripya intezar karein..."):
        time.sleep(0.3)
        result: PlantAnalysisOutput = diagnose_leaf(
            image=current_image,
            crop_type=selected_crop_name,
            api_key=api_key_input if not force_offline else None,
            model_name=model_choice,
            force_offline=force_offline
        )

        # 1. Store complete result securely in st.session_state as both object and clean dictionary
        report_dict = extract_report_dict(result)
        st.session_state["report_data"] = report_dict

        # 2. Pre-generate report PDF, text and filename immediately to avoid any rerun bugs
        clean_crop = re.sub(r'[^a-zA-Z0-9_]', '', report_dict['crop_name'].split('(')[0].strip().lower())
        timestamp_slug = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_base = f"kisan_salah_{clean_crop}_{timestamp_slug}"

        st.session_state["report_filename_base"] = filename_base
        try:
            st.session_state["report_pdf_bytes"] = build_advisory_pdf(report_dict)
        except Exception:
            st.session_state["report_pdf_bytes"] = None
        st.session_state["report_txt"] = generate_advisory_report_txt(report_dict)
        st.session_state["report_md"] = generate_advisory_report_md(report_dict)


# ---------------- RESULTS PRESENTATION: 5 CLEAR SECTIONS ----------------
report_data: dict = st.session_state.get("report_data")

if report_data is not None and isinstance(report_data, dict):
    st.divider()
    st.markdown('<div class="step-header" style="font-size: 1.55rem; color:#14532d;">📋 Fasal Rog Jaanch Report (Diagnosis Report)</div>', unsafe_allow_html=True)

    # 1. CROP NAME & 2. HEALTH STATUS HEADER
    st.markdown(f'<div class="crop-tag-pill">🌾 Fasal (Crop): {report_data.get("crop_name", "N/A")}</div>', unsafe_allow_html=True)

    header_col1, header_col2, header_col3 = st.columns([1.5, 1, 1], gap="medium")
    
    with header_col1:
        # SECTION 2: HEALTH STATUS
        status_str = str(report_data.get("health_status", "")).lower()
        is_healthy = "healthy" in status_str or "स्वस्थ" in status_str
        if is_healthy:
            st.markdown(
                """
                <div class="status-badge-healthy">
                    <span style="font-size:1.6rem;">🟢</span>
                    <div>
                        <div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; opacity:0.9;">Health Status (Sthiti)</div>
                        <div>SWASTH FOLIAGE (स्वस्थ फसल)</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div class="status-badge-infected">
                    <span style="font-size:1.6rem;">🔴</span>
                    <div>
                        <div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; opacity:0.9;">Health Status (Sthiti)</div>
                        <div>BIMAR / ROGGRAST (बीमार पत्ता)</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with header_col2:
        st.metric(
            label="Jaanch Ki Vishwasniyata (Confidence)",
            value=f"{report_data.get('confidence', 90)}%",
            delta=f"Severity: {report_data.get('severity', 'N/A')}"
        )

    with header_col3:
        eng_short = str(report_data.get("engine_used", "AI")).split("(")[0].strip()
        sev_short = str(report_data.get("severity", "Moderate")).split("(")[0].strip()
        st.metric(
            label="Rog Ki Gambhirta (Severity)",
            value=sev_short,
            delta=eng_short
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # SECTION 3: DISEASE NAME & SECTION 4: WHY IT HAPPENED (REASON)
    disease_display = report_data.get("disease_name", "N/A")
    crop_display = report_data.get("crop_name", "N/A")
    sev_display = report_data.get("severity", "N/A")
    cause_display = report_data.get("root_cause", "Karan darj nahi hai.")

    st.markdown(
        f"""
        <div class="feature-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:10px;">
                <div>
                    <div style="font-size:0.85rem; color:#15803d; font-weight:700; text-transform:uppercase; letter-spacing:0.5px;">
                        🦠 3. Bimari Ka Naam (Disease Name):
                    </div>
                    <h2 style="margin:0.2rem 0; color:#14532d; font-size:1.75rem;">
                        {disease_display}
                    </h2>
                </div>
                <div>
                    <span class="pill-tag">🌾 {crop_display}</span>
                    <span class="pill-tag">⚠️ {sev_display}</span>
                </div>
            </div>
            
            <hr style="margin:0.9rem 0; border:0; border-top:1px solid #e2e8f0;">
            
            <div>
                <div style="font-size:1.1rem; color:#166534; font-weight:700; margin-bottom:0.4rem;">
                    ❓ 4. Yeh Bimari Kyun Hui? (Why It Happened / Reason):
                </div>
                <p style="color:#27272a; line-height:1.65; font-size:1.02rem; margin:0; background:#f9fafb; padding:0.9rem 1.1rem; border-radius:10px; border-left:4px solid #16a34a;">
                    {cause_display}
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Symptoms spotted
    symptoms_list = report_data.get("symptoms_observed", [])
    if symptoms_list:
        with st.expander("🔎 Patte Par Dikhne Wale Mukhya Lakshan (Observed Symptoms)", expanded=True):
            for symptom in symptoms_list:
                st.markdown(f"- **{symptom}**")

    # SECTION 5: WHAT TO DO (EASY ORGANIC & CHEMICAL SOLUTIONS)
    st.markdown('<div class="step-header" style="font-size:1.35rem; margin-top:1.2rem;">💡 5. Ab Kya Karein? (What To Do - Easy Solutions & Remedies)</div>', unsafe_allow_html=True)
    
    tab_organic, tab_chemical, tab_preventive = st.tabs([
        "🌿 Gharelu / Jaivik Upchaar (Organic Solutions)",
        "🧪 Dawai / Rasayanik Upchaar (Chemical Solutions)",
        "🛡️ Aage Ke Liye Bachav (Prevention Tips)"
    ])

    with tab_organic:
        st.markdown("#### 🌿 Gharelu, Saste aur Surakshit Upchaar (Safe for Food & Soil)")
        st.caption("Yeh tarike khet ke mitr keedo ko nuksan nahi pahunchate aur fasal ko swasth banate hain:")
        organic_list = report_data.get("organic_remedies", [])
        if organic_list:
            for i, rem in enumerate(organic_list, 1):
                st.markdown(f'<div class="step-item-org"><b>Niyam {i}:</b> {rem}</div>', unsafe_allow_html=True)
        else:
            st.info("Paudha swasth hai, kisi upchaar ki zaroorat nahi hai.")

    with tab_chemical:
        st.markdown("#### 🧪 Krishi Kendra Par Milne Wali Asardaar Dawaiyan (Fungicides / Sprays)")
        st.caption("Agar bimari zyada fail rahi ho toh in dawaiyo ka sahi matra me chhidkaav karein:")
        chem_list = report_data.get("chemical_remedies", [])
        if chem_list:
            for i, chem in enumerate(chem_list, 1):
                st.markdown(f'<div class="step-item-chem"><b>Dawai Option {i}:</b> {chem}</div>', unsafe_allow_html=True)
            st.warning("⚠️ Chhidkaav karte samay muh par gamchha/mask lagayein aur hawa ki disha me hi spray karein. Phal todne se 7-10 din pehle chhidkaav na karein.")
        else:
            st.info("Fasal bilkul swasth hai, kisi chemical spray ki aavashyakta nahi hai.")

    with tab_preventive:
        st.markdown("#### 🛡️ Aane Wale Dino Me Bimari Se Bachne Ke Mukhya Niyam")
        st.caption("In aasan bato ka dhyan rakhkar aap aage hone wale nuksan se bach sakte hain:")
        prev_list = report_data.get("preventive_measures", [])
        if prev_list:
            for i, prev in enumerate(prev_list, 1):
                st.markdown(f'<div class="step-item-prev"><b>Salah {i}:</b> {prev}</div>', unsafe_allow_html=True)
        else:
            st.write("- Samay par niraai-gudaai karein aur paani theek se dein.")

    # ---------------- 6. ADVISORY REPORT DOWNLOAD SECTION ----------------
    st.markdown('<div class="step-header" style="font-size:1.35rem; margin-top:1.4rem;">📥 6. Salah Parchi Download Karein (Download Advisory Report)</div>', unsafe_allow_html=True)

    # Ensure report PDF bytes and text are ready from session state
    report_pdf_bytes = st.session_state.get("report_pdf_bytes")
    filename_base = st.session_state.get("report_filename_base", "kisan_salah")

    if not report_pdf_bytes:
        try:
            report_pdf_bytes = build_advisory_pdf(report_data)
            st.session_state["report_pdf_bytes"] = report_pdf_bytes
        except Exception as e_pdf:
            st.error(f"PDF create karne me dikkat hui: {e_pdf}")
            report_pdf_bytes = None

    report_txt_content = st.session_state.get("report_txt", "")
    if not report_txt_content:
        report_txt_content = generate_advisory_report_txt(report_data)
        st.session_state["report_txt"] = report_txt_content

    st.markdown(
        """
        <div class="download-card">
            <h4 style="margin:0 0 0.4rem 0; color:#15803d;">📄 Kisan Salah Parchi (Advisory Report PDF) Taiyar Hai!</h4>
            <p style="margin:0 0 0.8rem 0; color:#475569; font-size:0.95rem;">
                Aap is sundar format kiye gaye PDF report ko download karke apne phone me save kar sakte hain ya print nikaal kar Krishi Seva Kendra par dawai lene ke liye le ja sakte hain.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    down_col1, down_col2 = st.columns([1.6, 1], gap="medium")
    
    with down_col1:
        if report_pdf_bytes:
            st.download_button(
                label="📥 Download Advisory Report (PDF)",
                data=report_pdf_bytes,
                file_name=f"{filename_base}.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="btn_download_report_pdf",
                help="Sundar format kiya gaya PDF document jise aap apne phone me save ya print kar sakte hain."
            )
        else:
            st.error("PDF tayar nahi ho saki. Kripya daayein taraf se Text file download karein.")

    with down_col2:
        st.download_button(
            label="📄 Download Text File (.txt)",
            data=report_txt_content.encode("utf-8"),
            file_name=f"{filename_base}.txt",
            mime="text/plain; charset=utf-8",
            use_container_width=True,
            key="btn_download_report_txt",
            help="Saaf text format jo kisi bhi mobile phone ya computer par aasaani se khulta hai."
        )

    # Optional Expandable Preview of Report
    with st.expander("👀 Parchi Ka Text Preview Dekhein (Preview Advisory Slip)", expanded=False):
        st.text(report_txt_content)
