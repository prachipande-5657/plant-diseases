# 🌱 KrishiScan (PhytoScan): Fasal Rog Pehchan & Upchaar Salahkar

An intelligent, farmer-friendly plant leaf pathology and disease diagnosis web application built with **Python**, **Streamlit**, and **Google Gemini Vision AI** (with an offline smart botanical computer vision fallback engine).

---

## 🌟 New & Updated Features

1. **🌾 Crop / Plant Type Selection (Fasal Ka Chayan)**:
   - Dedicated dropdown to select common farming crops before analysis:
     - 🍅 **Tomato (Tamatar / टमाटर)**
     - 🥔 **Potato (Aaloo / आलू)**
     - 🌾 **Rice / Paddy (Dhan / धान)**
     - 🌾 **Wheat (Gehun / गेहूं)**
     - ☁️ **Cotton (Kapas / कपास)**
     - 🌶️ **Chili / Pepper (Mirch / मिर्च)**
     - 🌱 **Soybean (सोयाबीन)**
     - 🌽 **Corn / Maize (Makka / मक्का)**
     - 🍎 **Apple (Seb / सेब)**
     - 🌿 **Other Crop / General Plant (अन्य फसल / पौधा)**
   - The selected crop is passed directly into the AI analysis prompt and offline heuristic engine to deliver crop-accurate diagnoses.

2. **🗣️ Simplified, Farmer-Friendly Language (No Heavy Latin / Scientific Terms)**:
   - Replaced complex Latin nomenclature with familiar everyday terms:
     - Instead of *Alternaria solani* ➔ **Early Blight (Patton ke Bhoore Dhabbe / अगेती झुलसा)**
     - Instead of *Podosphaera xanthii* ➔ **Powdery Mildew (Safed Churni Fafund / सफेद चूर्ण फफूंद)**
     - Instead of *Puccinia sorghi* ➔ **Leaf Rust (Gerui / Ratuya Rog / गेरुआ-रतुआ)**
     - Instead of *Phytophthora infestans* ➔ **Late Blight (Pichheti Jhulsa / Kala Rog / पिछेती झुलसा)**
     - Instead of *Magnaporthe oryzae* ➔ **Rice Blast (Dhan ka Jhulsa / धान का झुलसा)**
   - Conversational explanations in easy Hinglish and simple English.

3. **📋 5 Clear Output Sections**:
   - **Section 1: 🌾 Crop Name (Fasal ka Naam)**
   - **Section 2: 🩺 Health Status (Paudhe ki Sthiti)** — High-contrast **🟢 Swasth (Healthy)** vs. **🔴 Bimar (Infected)** badge with confidence and severity level.
   - **Section 3: 🦠 Disease Name (Bimari ka Naam)** — Simple common name.
   - **Section 4: ❓ Why it Happened (Bimari Kyun Hui? - Reason)** — Plain-language conversational root cause explanation.
   - **Section 5: 💡 What to Do (Ab Kya Karein? - Easy Remedies)** — Tabbed layout:
     - 🌿 **Gharelu / Jaivik Upchaar (Organic Solutions)**: Actionable steps with exact kitchen/organic measurements (Neem oil, pruning bad leaves, sour buttermilk).
     - 🧪 **Dawai / Rasayanik Upchaar (Chemical Solutions)**: Affordable treatments available at Krishi Seva Kendra (Mancozeb, Saaf, Blitox, Tilt) with gram/litre instructions.
     - 🛡️ **Aage Ke Liye Bachav (Prevention Tips)**: Cultural practices (drip irrigation, row spacing).

4. **📥 Downloadable Advisory Slip (Kisan Parchi)**:
   - One-click export of a simple, formatted Markdown report.

---

## 📁 Project Structure

```
plant-disease-detector/
├── app.py                   # Streamlit web application & farmer-friendly UI
├── pdf_generator.py         # Beautiful PDF advisory slip generator (ReportLab)
├── disease_analyzer.py      # Dual-engine diagnostic pipeline (Gemini + Offline CV)
├── disease_database.py      # Knowledge base with simple terms & practical remedies
├── create_sample_leaves.py  # Script generating sample leaf images
├── requirements.txt         # Project dependencies
├── sample_images/           # Sample leaves for instant testing
│   ├── healthy_tomato_leaf.jpg
│   ├── early_blight_leaf.jpg
│   ├── powdery_mildew_leaf.jpg
│   └── common_rust_leaf.jpg
└── README.md                # Project documentation
```

---

## 🚀 How to Run the App

1. Navigate to the project directory:
   ```bash
   cd C:\Users\admin\.gemini\antigravity\scratch\plant-disease-detector
   ```
2. Start the Streamlit server:
   ```bash
   .\.venv\Scripts\streamlit.exe run app.py
   ```
3. Open `http://localhost:8501` in your browser.
