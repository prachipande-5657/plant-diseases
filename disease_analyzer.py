"""
Plant Leaf Disease Analysis Pipeline
Supports dual-engine diagnostics:
1. Google Gemini Multimodal Vision AI (via google-genai) with Crop Context & Simple Language
2. Smart Botanical Computer Vision Heuristic Engine (Offline / Fallback)
"""

import base64
import io
import json
import logging
from typing import Dict, Any, List, Optional
import numpy as np
from PIL import Image
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

from disease_database import DISEASE_PROFILES, get_disease_profile

logger = logging.getLogger(__name__)

class PlantAnalysisOutput(BaseModel):
    crop_name: str = Field(default="Tomato (Tamatar / टमाटर)", description="Selected or detected crop name")
    health_status: str = Field(description="'Healthy (स्वस्थ)' or 'Infected (बीमार)'")
    disease_name: str = Field(description="Simple, farmer-friendly disease name without Latin terms")
    confidence: float = Field(default=0.92, description="Confidence score between 0.0 and 1.0")
    severity: str = Field(default="Moderate (मध्यम)", description="Severity level in simple terms")
    symptoms_observed: List[str] = Field(default_factory=list, description="Simple visual symptoms spotted on the leaf")
    root_cause: str = Field(description="Why it happened - explained in simple, conversational language / Hinglish")
    organic_remedies: List[str] = Field(default_factory=list, description="Easy step-by-step organic / home remedies with simple dosages")
    chemical_remedies: List[str] = Field(default_factory=list, description="Practical chemical treatments with common names and simple dosages")
    preventive_measures: List[str] = Field(default_factory=list, description="Simple tips to prevent this disease in the future")
    engine_used: str = Field(default="Google Gemini Vision AI", description="The analysis engine used")

    @field_validator("symptoms_observed", "organic_remedies", "chemical_remedies", "preventive_measures", mode="before")
    @classmethod
    def sanitize_list(cls, v):
        if v is None:
            return []
        if isinstance(v, list):
            return [str(item) for item in v if item is not None and str(item).strip()]
        return [str(v)]

    def to_report_dict(self) -> Dict[str, Any]:
        """Convert analysis output to a clean, serializable dictionary for session state and reporting."""
        return {
            "crop_name": self.crop_name or "Fasal (Crop)",
            "health_status": self.health_status or "Infected",
            "disease_name": self.disease_name or "Crop Leaf Issue",
            "confidence": int(self.confidence * 100),
            "severity": self.severity or "Moderate",
            "symptoms_observed": list(self.symptoms_observed or []),
            "root_cause": self.root_cause or "Karan darj nahi hai.",
            "organic_remedies": list(self.organic_remedies or []),
            "chemical_remedies": list(self.chemical_remedies or []),
            "preventive_measures": list(self.preventive_measures or []),
            "engine_used": self.engine_used or "KrishiScan AI",
            "timestamp": datetime.now().strftime("%d-%m-%Y %I:%M %p")
        }



GEMINI_PROMPT_TEMPLATE = """You are a helpful, practical agricultural expert and plant doctor for farmers and home gardeners.
The user has provided an image of a leaf from the crop: **{crop_type}**.

Analyze this leaf image carefully and provide advice in simple, easy-to-understand conversational language (simple English or conversational Hinglish that any farmer can easily follow).

CRITICAL INSTRUCTIONS:
1. NO HEAVY SCIENTIFIC OR LATIN NAMES:
   - Do NOT use complex Latin taxonomy (do NOT write things like "Alternaria solani" or "Puccinia sorghi" or "biotrophic oomycetes").
   - Instead, use simple, common terms familiar to farmers (e.g., "Early Blight (Patton ke Bhoore Dhabbe / अगेती झुलसा)", "Leaf Curl (Patte Mudna)", "Powdery Mildew (Safed Churni Fafund)", "Rice Blast (Dhan ka Jhulsa)", "Healthy Leaf (Swasth Patta)").
2. CROP CONTEXT:
   - Base your diagnosis specifically on known issues for this crop: {crop_type}.
3. CLEAR SECTIONS:
   - Crop Name: "{crop_type}"
   - Health Status: Either 'Healthy (स्वस्थ)' or 'Infected (बीमार)'.
   - Disease Name: Simple common name in English + Hindi/Hinglish in brackets.
   - Confidence: Number from 0.75 to 0.99.
   - Severity: 'None (कोई नहीं)', 'Mild (हल्की)', 'Moderate (मध्यम)', or 'Severe (गंभीर)'.
   - Symptoms Observed: 2-3 simple bullet points in easy words.
   - Why it happened (Root Cause): Explain in simple, conversational words WHY this happened (e.g. fungus, weather humidity, rain splash, moisture on leaves, or pest bite).
   - What to do (Remedies):
     - Organic Remedies (Gharelu/Jaivik Upchaar): Practical steps with exact everyday quantities (e.g. 5ml Neem oil in 1L water, removing bad leaves, sour buttermilk spray).
     - Chemical Remedies (Dawai/Rasayanik Upchaar): Easily accessible medicines at Krishi Kendra (e.g. Mancozeb, Saaf, Blitox, Tilt) with exact dosages (e.g. 2 gram per litre water).
     - Preventive Measures: 2-3 easy tips to prevent it in the future.

Respond strictly adhering to the JSON schema.
"""


def _image_to_base64_and_mime(image: Image.Image) -> tuple[str, str]:
    """Convert PIL Image to base64 string and determine mime type."""
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG", quality=90)
    img_bytes = buffered.getvalue()
    b64_str = base64.b64encode(img_bytes).decode("utf-8")
    return b64_str, "image/jpeg"


def analyze_with_gemini(
    image: Image.Image,
    crop_type: str,
    api_key: str,
    model_name: str = "gemini-3.8-flash"
) -> PlantAnalysisOutput:
    """
    Call Google Gemini Vision API using the official google-genai SDK.
    Tailors the diagnosis to the user-selected crop and outputs simple, farmer-friendly advice.
    """
    try:
        from google import genai
    except ImportError as e:
        raise RuntimeError("The 'google-genai' package is not installed. Please install it.") from e

    client = genai.Client(api_key=api_key)
    b64_data, mime_type = _image_to_base64_and_mime(image)
    prompt_text = GEMINI_PROMPT_TEMPLATE.format(crop_type=crop_type)

    # Attempt 1: Modern google-genai interactions.create with structured schema
    try:
        interaction = client.interactions.create(
            model=model_name,
            input=[
                {"type": "text", "text": prompt_text + "\nAnalyze this leaf image and return the structured diagnostic JSON."},
                {
                    "type": "image",
                    "data": b64_data,
                    "mime_type": mime_type
                }
            ],
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": PlantAnalysisOutput.model_json_schema()
            }
        )
        
        output_json = interaction.output_text
        if output_json:
            data = json.loads(output_json)
            data["crop_name"] = crop_type
            data["engine_used"] = f"Google Gemini Vision AI ({model_name})"
            return PlantAnalysisOutput(**data)
    except Exception as e_interact:
        logger.info("interactions.create endpoint fallback: %s", e_interact)
        
        # Attempt 2: client.models.generate_content
        try:
            from google.genai import types
            
            response = client.models.generate_content(
                model=model_name,
                contents=[
                    types.Part.from_bytes(
                        data=base64.b64decode(b64_data),
                        mime_type=mime_type,
                    ),
                    prompt_text,
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=PlantAnalysisOutput,
                    temperature=0.2,
                ),
            )
            
            cleaned_text = response.text.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]
            data = json.loads(cleaned_text.strip())
            data["crop_name"] = crop_type
            data["engine_used"] = f"Google Gemini Vision AI ({model_name})"
            return PlantAnalysisOutput(**data)
        except Exception as e_gen:
            logger.error("generate_content failed: %s", e_gen)
            raise RuntimeError(f"Gemini API analysis failed: {e_gen}") from e_gen


def analyze_with_heuristic_engine(image: Image.Image, crop_type: str = "Tomato") -> PlantAnalysisOutput:
    """
    Intelligent Computer Vision & Botanical Heuristic Engine.
    Uses numpy & PIL for background segmentation, color space deconstruction,
    and crop-aware disease matching in simple language.
    """
    img_rgb = image.convert("RGB")
    img_std = img_rgb.resize((300, 300))
    arr = np.array(img_std, dtype=np.float32)

    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]
    brightness = (r + g + b) / 3.0

    # 1. Background segmentation: identify and filter out neutral white/light-gray background
    is_bg = (brightness > 230) & (np.abs(r - g) < 20) & (np.abs(g - b) < 20)
    fg_mask = ~is_bg
    total_fg = int(np.sum(fg_mask))

    if total_fg < 1000:
        fg_mask = np.ones((300, 300), dtype=bool)
        total_fg = 90000

    r_fg = r[fg_mask]
    g_fg = g[fg_mask]
    b_fg = b[fg_mask]
    br_fg = brightness[fg_mask]

    # 2. Extract pathology spectral signatures on leaf foreground
    # Powdery Mildew: ash/white coating
    powdery_pixels = np.sum((r_fg > 90) & (b_fg > 75) & (g_fg > 90))
    powdery_ratio = float(powdery_pixels) / total_fg

    # Rust: cinnamon/reddish-orange raised pustules (R high, R > G*1.25, B low)
    rust_pixels = np.sum((r_fg > 165) & (r_fg > g_fg * 1.25) & (b_fg < 95))
    rust_ratio = float(rust_pixels) / total_fg

    # Brown / Dark Necrotic Lesions (Early Blight / Leaf Spot / Rice Blast)
    brown_pixels = np.sum((r_fg > 55) & (r_fg > g_fg) & (b_fg < 95) & (r_fg < 165))
    brown_ratio = float(brown_pixels) / total_fg

    # Water-soaked black decay / Late Blight rot
    dark_decay_pixels = np.sum((br_fg < 45) & (r_fg + g_fg + b_fg > 15))
    dark_decay_ratio = float(dark_decay_pixels) / total_fg

    # Yellow Chlorosis
    yellow_pixels = np.sum((r_fg > 150) & (g_fg > 140) & (b_fg < 115) & (np.abs(r_fg - g_fg) < 60))
    yellow_ratio = float(yellow_pixels) / total_fg

    # Healthy Green
    green_pixels = np.sum((g_fg > r_fg * 1.05) & (g_fg > b_fg * 1.05) & (g_fg > 50))
    green_ratio = float(green_pixels) / total_fg

    crop_lower = crop_type.lower()

    # 3. Crop-aware decision logic in simple terms
    if powdery_ratio > 0.15:
        profile_key = "powdery_mildew"
        confidence = min(0.97, 0.86 + (powdery_ratio * 0.15))
        severity = "Severe (गंभीर)" if powdery_ratio > 0.45 else "Moderate (मध्यम)"
        observed = [
            f"Patton par lagbhag {int(powdery_ratio * 100)}% safed powder/churni fafund ki parat dikh rahi hai",
            "Patton ka hara rang safed fafund ke neeche dab gaya hai",
            "Patti ki dhoop sokhne ki kshamta kamzor ho rahi hai"
        ]
    elif rust_ratio > 0.015:
        profile_key = "common_rust"
        confidence = min(0.96, 0.88 + (rust_ratio * 2.5))
        severity = "Severe (गंभीर)" if rust_ratio > 0.05 else "Moderate (मध्यम)"
        crop_spec = "Dhan/Gehun/Makka" if any(c in crop_lower for c in ["rice", "wheat", "corn"]) else "Fasal"
        observed = [
            f"{crop_spec} ki patti par laal-narangi aur bhoore rang ke ubhre hue daane (~{int(rust_ratio * 100)}% hissa)",
            "Ungli lagane par zang jaisa powder chooth sakta hai",
            "Daano ke aas-paas peela ghera ban gaya hai"
        ]
    elif brown_ratio > 0.15:
        # Check if rice or cotton or tomato/potato
        if "rice" in crop_lower or "paddy" in crop_lower or "dhan" in crop_lower:
            profile_key = "rice_blast"
            confidence = min(0.96, 0.86 + (brown_ratio * 0.2))
            severity = "Severe (गंभीर)" if brown_ratio > 0.30 else "Moderate (मध्यम)"
            observed = [
                f"Dhan ki patti par naav/aankh ke aakar ke bhoore dhabbe (~{int(brown_ratio * 100)}% hissa)",
                "Dhabbo ke beech ka hissa raakh jaisa aur kinare laal-bhoore hain",
                "Tezi se failne wala Dhan ka jhulsa rog ke lakshan"
            ]
        elif "potato" in crop_lower or "aaloo" in crop_lower:
            profile_key = "early_blight"
            confidence = 0.94
            severity = "Moderate to Severe (मध्यम से गंभीर)"
            observed = [
                f"Aaloo ke patton par gol chhalle jaise bhoore-kaale dhabbe (~{int(brown_ratio * 100)}% hissa)",
                "Dhabbo ke chaaron taraf patti peeli pad rahi hai",
                "Aaloo ka ageti jhulsa (Early Blight) rog"
            ]
        elif brown_ratio > 0.20 or yellow_ratio > 0.10:
            profile_key = "early_blight"
            confidence = min(0.97, 0.88 + (brown_ratio * 0.25))
            severity = "Severe (गंभीर)" if brown_ratio > 0.35 else "Moderate (मध्यम)"
            observed = [
                f"Patton par gol chhalle jaise bhoore-kaale dhabbe (Target-rings, lagbhag {int(brown_ratio * 100)}% hissa)",
                f"Dhabbo ke aas-paas peela ghera (~{int(yellow_ratio * 100)}% peela hissa)",
                "Patti sookhne aur girne ki aashanka"
            ]
        else:
            profile_key = "leaf_spot"
            confidence = 0.90
            severity = "Moderate (मध्यम)"
            observed = [
                f"Patton par chhote-chhote bhoore dhabbe (~{int(brown_ratio * 100)}% hissa)",
                "Fafundi sankraman ke shuruati dhabbe",
                "Nami ke karan badhne wale dhabbe"
            ]
    elif dark_decay_ratio > 0.10:
        profile_key = "late_blight"
        confidence = min(0.95, 0.83 + (dark_decay_ratio * 0.8))
        severity = "Severe (गंभीर / तुरंत इलाज चाहिए)"
        observed = [
            f"Patton par paani bheege jaise kaale-bhoore sadan wale dhabbe (~{int(dark_decay_ratio * 100)}% hissa)",
            "Patti aur daali tezi se kaali padkar sad rahi hai",
            "Pichheti jhulsa (Late Blight) ke aakramak lakshan"
        ]
    elif yellow_ratio > 0.20 and brown_ratio < 0.08:
        profile_key = "nutrient_deficiency"
        confidence = 0.89
        severity = "Mild to Moderate (हल्की से मध्यम)"
        observed = [
            f"Patton ka lagbhag {int(yellow_ratio * 100)}% hissa peela pad raha hai",
            "Koi fafund ya kido ke kaate hue dhabbe nahi dikh rahe hain",
            "Mitti me khad (Nitrogen/Iron/Magnesium) ki kami ke lakshan"
        ]
    elif green_ratio > 0.80 and brown_ratio < 0.05 and powdery_ratio < 0.08 and rust_ratio < 0.01:
        profile_key = "healthy"
        confidence = min(0.99, 0.92 + (green_ratio * 0.06))
        severity = "None (कोई बीमारी नहीं)"
        observed = [
            f"Patti bilkul saaf aur chamakdaar hari hai (~{int(green_ratio * 100)}% swasth bhag)",
            "Koi bimari, fafund ya kide ka nishaan nahi hai",
            "Paudhe ki poshan aur paani ki sthiti bahut achhi hai"
        ]
    else:
        if brown_ratio > 0.05 or yellow_ratio > 0.10:
            profile_key = "leaf_spot"
            confidence = 0.84
            severity = "Mild (हल्की)"
            observed = [
                "Patte par chhote-mote daag aur halki peeli rangat hai",
                "Halki fafundi ya nami ke karan shuruati dhabbe ho sakte hain",
                "Samay par neem spray karne se roktham ho sakti hai"
            ]
        else:
            profile_key = "healthy"
            confidence = 0.88
            severity = "None (कोई बीमारी नहीं)"
            observed = [
                "Patti mukhyatatah swasth aur samanya hai",
                "Koi badi bimari ya nuksan nahi dikh raha hai",
                "Paudha achhi sthiti me vikasit ho raha hai"
            ]

    profile = get_disease_profile(profile_key)
    
    return PlantAnalysisOutput(
        crop_name=crop_type,
        health_status=profile["health_status"],
        disease_name=profile["disease_name"],
        confidence=round(confidence, 2),
        severity=severity,
        symptoms_observed=observed or profile["symptoms"],
        root_cause=profile["root_cause"],
        organic_remedies=profile["organic_remedies"],
        chemical_remedies=profile["chemical_remedies"],
        preventive_measures=profile["preventive_measures"],
        engine_used="Smart Botanical Offline Engine"
    )


def diagnose_leaf(
    image: Image.Image,
    crop_type: str = "Tomato",
    api_key: Optional[str] = None,
    model_name: str = "gemini-3.8-flash",
    force_offline: bool = False
) -> PlantAnalysisOutput:
    """
    Main diagnostic entry point.
    Accepts the user-selected crop_type and runs either Gemini Vision AI or Offline Engine.
    """
    if not force_offline and api_key and api_key.strip():
        try:
            return analyze_with_gemini(image, crop_type=crop_type, api_key=api_key.strip(), model_name=model_name)
        except Exception as e:
            logger.warning("Gemini Vision AI diagnosis failed, falling back to heuristic engine: %s", e)
            result = analyze_with_heuristic_engine(image, crop_type=crop_type)
            result.engine_used = "Smart Botanical Offline Engine (Gemini Fallback)"
            return result
    
    # Run smart offline heuristic engine
    return analyze_with_heuristic_engine(image, crop_type=crop_type)
