"""
PDF Advisory Report Generator for KrishiScan / PhytoScan
Generates beautifully formatted, printable PDF diagnostic slips (Parchi)
with font fallbacks, clean tables, and multilingual Hindi/English support.
"""

import io
import os
import re
from datetime import datetime
from typing import Dict, Any, List

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def _register_best_font() -> tuple[str, str]:
    """
    Register Unicode TrueType fonts supporting Hindi (Devanagari) & English.
    Falls back gracefully if specific system fonts are unavailable.
    """
    font_regular = "Helvetica"
    font_bold = "Helvetica-Bold"

    candidate_fonts = [
        ("C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/segoeuib.ttf"),
        ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
        ("C:/Windows/Fonts/Nirmala.ttc", "C:/Windows/Fonts/Nirmala.ttc"),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ("/usr/share/fonts/truetype/freefont/FreeSans.ttf", "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"),
    ]

    for reg_path, bold_path in candidate_fonts:
        if os.path.exists(reg_path):
            try:
                # Handle .ttc fonts with subfontIndex if needed
                if reg_path.lower().endswith(".ttc"):
                    pdfmetrics.registerFont(TTFont("KrishiFont", reg_path, subfontIndex=0))
                else:
                    pdfmetrics.registerFont(TTFont("KrishiFont", reg_path))
                font_regular = "KrishiFont"

                if bold_path and os.path.exists(bold_path) and not bold_path.lower().endswith(".ttc"):
                    pdfmetrics.registerFont(TTFont("KrishiFont-Bold", bold_path))
                    font_bold = "KrishiFont-Bold"
                else:
                    font_bold = "KrishiFont"
                break
            except Exception:
                continue

    return font_regular, font_bold


# Cache font registration once
FONT_REGULAR, FONT_BOLD = _register_best_font()


def _clean_text_for_pdf(text: Any) -> str:
    """Safely format and escape text for ReportLab Paragraphs."""
    if text is None:
        return ""
    s = str(text)
    # XML entity escaping for ReportLab
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return s.strip()


def build_advisory_pdf(data: Dict[str, Any]) -> bytes:
    """
    Generate a beautifully styled, print-ready PDF advisory slip from diagnostic data.
    Returns the raw PDF bytes.
    """
    buffer = io.BytesIO()

    # Document setup: A4 with 0.5 inch margins (36 pt)
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=32,
        bottomMargin=32,
    )

    # Palette
    c_primary = colors.HexColor("#14532d")     # Deep forest green
    c_header_bg = colors.HexColor("#15803d")   # Vibrant emerald
    c_sub_bg = colors.HexColor("#f0fdf4")      # Soft sage
    c_card_border = colors.HexColor("#bbf7d0") # Pale green border
    c_text_dark = colors.HexColor("#1e293b")   # Slate dark
    c_text_muted = colors.HexColor("#475569")  # Slate gray
    c_danger = colors.HexColor("#dc2626")      # Red for infected
    c_success = colors.HexColor("#16a34a")     # Green for healthy
    c_blue_bg = colors.HexColor("#eff6ff")     # Light blue
    c_blue_border = colors.HexColor("#bfdbfe") # Blue border
    c_amber_bg = colors.HexColor("#fffbeb")    # Amber light
    c_amber_border = colors.HexColor("#fde68a")

    # Typography styles
    styles = getSampleStyleSheet()

    style_header_title = ParagraphStyle(
        "HeaderTitle",
        fontName=FONT_BOLD,
        fontSize=17,
        leading=21,
        textColor=colors.white,
    )
    style_header_sub = ParagraphStyle(
        "HeaderSub",
        fontName=FONT_REGULAR,
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#dcfce7"),
    )
    style_header_meta = ParagraphStyle(
        "HeaderMeta",
        fontName=FONT_REGULAR,
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#f0fdf4"),
        alignment=2,  # Right aligned
    )

    style_section_title = ParagraphStyle(
        "SectionTitle",
        fontName=FONT_BOLD,
        fontSize=11.5,
        leading=15,
        textColor=c_primary,
    )
    style_body = ParagraphStyle(
        "BodyText",
        fontName=FONT_REGULAR,
        fontSize=9.5,
        leading=13.5,
        textColor=c_text_dark,
    )
    style_body_bold = ParagraphStyle(
        "BodyTextBold",
        fontName=FONT_BOLD,
        fontSize=9.5,
        leading=13.5,
        textColor=c_text_dark,
    )
    style_list_item = ParagraphStyle(
        "ListItem",
        fontName=FONT_REGULAR,
        fontSize=9,
        leading=13,
        textColor=c_text_dark,
    )

    story = []

    # 1. HEADER BANNER
    ts = data.get("timestamp", datetime.now().strftime("%d-%m-%Y %I:%M %p"))
    header_content = [
        [
            Paragraph(
                "<b>KRISHISCAN : FASAL ROG SALAH PARCHI</b><br/>"
                "<i>AI Plant Leaf Disease Diagnosis &amp; Farmer Advisory Slip</i>",
                style_header_title,
            ),
            Paragraph(
                f"<b>Taarikh / Date:</b> {ts}<br/>"
                f"<b>Portal:</b> KrishiScan Kisan Seva<br/>"
                f"<b>Engine:</b> {_clean_text_for_pdf(data.get('engine_used', 'KrishiScan AI'))}",
                style_header_meta,
            ),
        ]
    ]

    header_table = Table(header_content, colWidths=[360, 163])
    header_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), c_header_bg),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ])
    )
    story.append(header_table)
    story.append(Spacer(1, 10))

    # 2. KEY METRICS GRID (Crop, Status, Disease, Severity, Confidence)
    crop_name = _clean_text_for_pdf(data.get("crop_name", "N/A"))
    health_status = _clean_text_for_pdf(data.get("health_status", "N/A"))
    disease_name = _clean_text_for_pdf(data.get("disease_name", "N/A"))
    conf = data.get("confidence", 90)
    sev = _clean_text_for_pdf(data.get("severity", "Moderate"))

    is_healthy = "healthy" in health_status.lower() or "स्वस्थ" in health_status
    status_color_hex = "#16a34a" if is_healthy else "#dc2626"
    status_icon = "[OK] SWASTH" if is_healthy else "[!] ROGGRAST / BIMAR"

    meta_rows = [
        [
            Paragraph("<b>Fasal (Crop):</b>", style_body_bold),
            Paragraph(f"<b>{crop_name}</b>", style_body),
            Paragraph("<b>Sthiti (Health Status):</b>", style_body_bold),
            Paragraph(f"<font color='{status_color_hex}'><b>{health_status}</b></font>", style_body),
        ],
        [
            Paragraph("<b>Bimari (Disease):</b>", style_body_bold),
            Paragraph(f"<b>{disease_name}</b>", style_body),
            Paragraph("<b>Vishwasniyata (Conf):</b>", style_body_bold),
            Paragraph(f"{conf}% (Severity: {sev})", style_body),
        ],
    ]

    meta_table = Table(meta_rows, colWidths=[90, 175, 115, 143])
    meta_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), c_sub_bg),
            ("BOX", (0, 0), (-1, -1), 1, c_card_border),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ])
    )
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # 3. SECTION 1: WHY IT HAPPENED (ROOT CAUSE / REASON)
    cause_text = _clean_text_for_pdf(data.get("root_cause", "Karan darj nahi hai."))
    cause_card = [
        [Paragraph("<b>[?] 1. BIMARI KYUN HUI? (WHY IT HAPPENED / REASON)</b>", style_section_title)],
        [Paragraph(cause_text, style_body)],
    ]
    cause_table = Table(cause_card, colWidths=[523])
    cause_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8faf8")),
            ("BOX", (0, 0), (-1, -1), 1, c_card_border),
            ("LINELEFT", (0, 0), (0, -1), 3.5, c_primary),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ])
    )
    story.append(cause_table)
    story.append(Spacer(1, 9))

    # 4. SECTION 2: OBSERVED SYMPTOMS (LAKSHAN)
    symptoms = [_clean_text_for_pdf(s) for s in data.get("symptoms_observed", []) if s]
    if symptoms:
        sym_content = [
            [Paragraph("<b>[*] 2. PATTE PAR DIKHNE WALE LAKSHAN (OBSERVED SYMPTOMS)</b>", style_section_title)],
        ]
        for s in symptoms:
            sym_content.append([Paragraph(f"• {s}", style_list_item)])

        sym_table = Table(sym_content, colWidths=[523])
        sym_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fafafa")),
                ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#e5e7eb")),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ])
        )
        story.append(sym_table)
        story.append(Spacer(1, 9))

    # 5. SECTION 3: ORGANIC & BIOLOGICAL REMEDIES (GHARELU / JAIVIK UPCHAAR)
    organic_list = [_clean_text_for_pdf(r) for r in data.get("organic_remedies", []) if r]
    org_content = [
        [Paragraph("<b>[+] 3. GHARELU / JAIVIK UPCHAAR (ORGANIC &amp; BIOLOGICAL REMEDIES)</b>", style_section_title)],
        [Paragraph("<i>Khet ke mitr keedo ko nuksan nahi pahunchane wale surakshit tarike:</i>", style_header_sub)]
    ]
    if organic_list:
        for i, item in enumerate(organic_list, 1):
            org_content.append([Paragraph(f"<b>Niyam {i}:</b> {item}", style_list_item)])
    else:
        org_content.append([Paragraph("Fasal swasth hai, kisi gharelu upchaar ki zaroorat nahi hai.", style_list_item)])

    org_table = Table(org_content, colWidths=[523])
    org_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), c_sub_bg),
            ("BOX", (0, 0), (-1, -1), 1, c_card_border),
            ("LINELEFT", (0, 0), (0, -1), 3.5, c_success),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ])
    )
    story.append(org_table)
    story.append(Spacer(1, 9))

    # 6. SECTION 4: CHEMICAL REMEDIES (DAWAI / RASAYANIK UPCHAAR)
    chem_list = [_clean_text_for_pdf(c) for c in data.get("chemical_remedies", []) if c]
    chem_content = [
        [Paragraph("<b>[!] 4. DAWAI / RASAYANIK UPCHAAR (CHEMICAL REMEDIES &amp; SPRAYS)</b>", ParagraphStyle("ChemTitle", parent=style_section_title, textColor=colors.HexColor("#1e3a8a")))],
        [Paragraph("<i>Bimari zyada failne par Krishi Kendra par milne wali asardaar dawaiyan:</i>", ParagraphStyle("ChemSub", parent=style_header_sub, textColor=colors.HexColor("#3b82f6")))]
    ]
    if chem_list:
        for i, item in enumerate(chem_list, 1):
            chem_content.append([Paragraph(f"<b>Option {i}:</b> {item}", style_list_item)])
        chem_content.append([
            Paragraph("<b>Savdhani:</b> Chhidkaav karte samay muh par mask/gamchha lagayein aur sahi matra ka dhyan rakhein.", ParagraphStyle("Alert", parent=style_list_item, textColor=colors.HexColor("#991b1b"), fontName=FONT_BOLD))
        ])
    else:
        chem_content.append([Paragraph("Fasal swasth hai, kisi chemical spray ki aavashyakta nahi hai.", style_list_item)])

    chem_table = Table(chem_content, colWidths=[523])
    chem_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), c_blue_bg),
            ("BOX", (0, 0), (-1, -1), 1, c_blue_border),
            ("LINELEFT", (0, 0), (0, -1), 3.5, colors.HexColor("#2563eb")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ])
    )
    story.append(chem_table)
    story.append(Spacer(1, 9))

    # 7. SECTION 5: PREVENTIVE PRACTICES (BACHAV KE NIYAM)
    prev_list = [_clean_text_for_pdf(p) for p in data.get("preventive_measures", []) if p]
    prev_content = [
        [Paragraph("<b>[i] 5. AAGE KE LIYE BACHAV (PREVENTIVE FARMING PRACTICES)</b>", ParagraphStyle("PrevTitle", parent=style_section_title, textColor=colors.HexColor("#92400e")))],
    ]
    if prev_list:
        for i, item in enumerate(prev_list, 1):
            prev_content.append([Paragraph(f"<b>Salah {i}:</b> {item}", style_list_item)])
    else:
        prev_content.append([Paragraph("Niyamit roop se fasal ki niraai-gudaai karein aur paani sahi tarike se dein.", style_list_item)])

    prev_table = Table(prev_content, colWidths=[523])
    prev_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), c_amber_bg),
            ("BOX", (0, 0), (-1, -1), 1, c_amber_border),
            ("LINELEFT", (0, 0), (0, -1), 3.5, colors.HexColor("#d97706")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ])
    )
    story.append(prev_table)
    story.append(Spacer(1, 10))

    # 8. FOOTER NOTE
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=6))
    footer_p1 = Paragraph(
        "<b>KrishiScan AI Platform • Apki Fasal, Hamari Dekhbhal</b> | "
        "<i>Sujhav: Badi matra me dawai daalne se pehle najdeeki Krishi Vigyan Kendra (KVK) se salah lein.</i>",
        ParagraphStyle("Footer", fontName=FONT_REGULAR, fontSize=8, leading=11, textColor=c_text_muted, alignment=1)
    )
    story.append(footer_p1)

    # Build PDF document
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
