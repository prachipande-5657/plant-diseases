"""
Kisan & Gardener Friendly Plant Leaf Disease Knowledge Base
Contains simplified, common-term disease profiles, easy-to-understand reasons (Karan),
and step-by-step practical remedies (Organic / Gharelu Upchaar & Chemical / Dawai).
"""

from typing import Dict, Any, List

# Crops list for agricultural diagnostics
COMMON_CROPS: List[Dict[str, str]] = [
    {"id": "tomato", "name": "Tomato (Tamatar / टमाटर)", "icon": "🍅"},
    {"id": "potato", "name": "Potato (Aaloo / आलू)", "icon": "🥔"},
    {"id": "rice", "name": "Rice / Paddy (Dhan / धान)", "icon": "🌾"},
    {"id": "wheat", "name": "Wheat (Gehun / गेहूं)", "icon": "🌾"},
    {"id": "cotton", "name": "Cotton (Kapas / कपास)", "icon": "☁️"},
    {"id": "chili", "name": "Chili / Pepper (Mirch / मिर्च)", "icon": "🌶️"},
    {"id": "soybean", "name": "Soybean (सोयाबीन)", "icon": "🌱"},
    {"id": "corn", "name": "Corn / Maize (Makka / मक्का)", "icon": "🌽"},
    {"id": "apple", "name": "Apple (Seb / सेब)", "icon": "🍎"},
    {"id": "general", "name": "Other Crop / General Plant (अन्य पौधा)", "icon": "🌿"},
]

# Simple, farmer-friendly disease knowledge base
DISEASE_PROFILES: Dict[str, Dict[str, Any]] = {
    "early_blight": {
        "disease_name": "Early Blight (Patton ke Bhoore Dhabbe / अगेती झुलसा)",
        "simple_name": "Early Blight (पत्तियों पर काले-भूरे धब्बे)",
        "health_status": "Infected (बीमार)",
        "severity": "Moderate (मध्यम)",
        "symptoms": [
            "Purane aur nichle patton par gol chhalle jaise bhoore-kaale dhabbe (Target-like rings)",
            "Dhabbe ke chaaron taraf peela ghera (Yellow ring/halo around spot)",
            "Dheere-dheere patte sookh kar jhadne lagte hain"
        ],
        "root_cause": (
            "Fungus (फफूंद) ke sankraman se hota hai. Jab mausam garm ho (24°C-29°C) aur baarish, "
            "hawa me zyada nami (humidity) ya patton par lambe samay tak paani/os (dew) thehra rahe, "
            "toh yeh fafundi khet me tezi se failti hai."
        ),
        "organic_remedies": [
            "Kharab Patte Hatayein: Jin patton par dhabbe hain, unhe todkar khet ya gamle se door zameen me daba dein ya jala dein (compost me na dalein).",
            "Neem Tel Spray (Neem Oil): 1 litre gungune paani me 5 ml Neem Oil aur 2 boond bartan dhone wala sabun milakar har 7 din par chhidkaav karein.",
            "Baking Soda Ghol: 1 litre paani me 1 chammach baking soda milakar subah ke samay spray karein.",
            "Trichoderma / Jaivik Fafundinashak: 5 gram Trichoderma viride prati litre paani me milakar jadon ke paas chhidkein."
        ],
        "chemical_remedies": [
            "Saaf / Mancozeb (Dithane M-45): 2 se 2.5 gram prati litre paani me gholkar patton ke aage aur peeche achhi tarah chhidkein.",
            "Copper Oxychloride (Blitox 50): 2.5 se 3 gram prati litre paani me milakar 10 din ke antaral par spray karein.",
            "Amistar Top ya Nativo (Jyada failne par): 1 ml prati litre paani me milakar spray karein."
        ],
        "preventive_measures": [
            "Paani dete samay dhyaan rakhein ki paani seedhe jadon (roots) me dein, patton par paani na uchhalein.",
            "Paudhe ke neeche sookhi ghaas ya bhoose ki mulching karein taaki mitti ka ganda paani patton par na pade.",
            "Paudho ke beech 2 se 2.5 foot ki doori rakhein taaki dhoop aur taza hawa milti rahe."
        ]
    },
    "powdery_mildew": {
        "disease_name": "Powdery Mildew (Safed Churni Fafund / सफेद चूर्ण फफूंद)",
        "simple_name": "Powdery Mildew (पत्तियों पर सफेद पाउडर)",
        "health_status": "Infected (बीमार)",
        "severity": "Moderate (मध्यम)",
        "symptoms": [
            "Patton ke upar aur neeche safed powder / aate jaisi parat jam jati hai",
            "Patte tedhe-medhe hone lagte hain aur unka rang peela pad jata hai",
            "Naye patte aur kaliyaan theek se khil nahi paati aur sookh jati hain"
        ],
        "root_cause": (
            "Safed Fafundi (Mildew Fungus) ke karan hota hai. Jab paudhe ko dhoop kam milti hai, "
            "hawa ka bahaav kam hota hai aur hawa me zyada nami (humid weather) hoti hai, "
            "tab yeh safed fafund patton par tezi se chha jati hai."
        ),
        "organic_remedies": [
            "Doodh aur Paani ka Ghol: 1 hissa doodh (ya chhaachh/buttermilk) aur 9 hissa paani milakar tez dhoop ke samay chhidkein (doodh ke tatva fafund ko khatam karte hain).",
            "Baking Soda Spray: 1 litre paani me 1 chammach meetha soda (Baking Soda) aur thoda sa sabun milakar spray karein.",
            "Neem Tel Chhidkaav: 5ml Neem Oil prati litre paani me milakar hafte me ek baar spray karein.",
            "Sookhe aur Ghane Patte Kaatein: Paudhe ke beech ke faaltu patte kaat dein taaki dhoop andar tak pahunche."
        ],
        "chemical_remedies": [
            "Sulphas (Wettable Sulfur 80% WP): 2 gram prati litre paani me gholkar chhidkein (Dhyan rahe: Jab taapman 32°C se zyada ho tab na dalein).",
            "Hexaconazole (Contaf Plus): 1 se 1.5 ml prati litre paani me milakar spray karein.",
            "Myclobutanil / Score (Difenoconazole): 0.5 se 1 ml prati litre paani me gholkar spray karein."
        ],
        "preventive_measures": [
            "Paudho ko aisi jagah lagayein jahan kam se kam 5-6 ghante ki achhi dhoop aati ho.",
            "Ghane paudho ki chhantai (pruning) karein taaki hawa aar-paar ja sake.",
            "Urea (Nitrogen) khad ka zaroorat se zyada upyog na karein, isse bimari jaldi aati hai."
        ]
    },
    "common_rust": {
        "disease_name": "Leaf Rust (Gerui / Ratuya Rog / गेरुआ-रतुआ रोग)",
        "simple_name": "Leaf Rust (पत्तियों पर लाल-भूरे जंग जैसे दाने)",
        "health_status": "Infected (बीमार)",
        "severity": "Moderate (मध्यम)",
        "symptoms": [
            "Patton par laal, peele ya narangi-bhoore rang ke ubhre hue daane (pustules)",
            "Chhoone par ungli par laal-peela powder/zang (rust) jaisa lagta hai",
            "Dheere-dheere patti peeli hokar poori tarah sookhne lagti hai"
        ],
        "root_cause": (
            "Rust Fafundi (जंग फफूंद) ke karan hota hai. Iske beej (spores) hawa ke sath udkar "
            "khet me aate hain. Thanda-halka garm mausam (15°C-25°C) aur subah ki os (dew) me "
            "yeh bimari tezi se panapti hai."
        ),
        "organic_remedies": [
            "Khatti Chhaachh (Sour Buttermilk): 1 litre khatti chhaachh ko 10 litre paani me milakar chhidkaav karein.",
            "Neem Tel Spray: 5 ml pure Neem Oil prati litre paani me gholkar chhidkein.",
            "Gandhak (Sulfur Dust): Barish rukne ke baad patton par sulfur ka halka chhidkaav karein."
        ],
        "chemical_remedies": [
            "Propiconazole (Tilt 25% EC): 1 ml prati litre paani me milakar spray karein (Rust ke liye sabse asardaar).",
            "Mancozeb (Dithane M-45): 2.5 gram prati litre paani me gholkar rokthaam ke liye spray karein.",
            "Tebuconazole (Folicur): 1 ml prati litre paani me gholkar chhidkein."
        ],
        "preventive_measures": [
            "Rust se bachne wali beej kismen (Resistant seed varieties) boyein.",
            "Khet me se sookhe avshesh aur purani pattiyaan hata kar saaf rakhein.",
            "Khet me paani ka jamav na hone dein aur samay par niraai-gudaai karein."
        ]
    },
    "late_blight": {
        "disease_name": "Late Blight (Pichheti Jhulsa / Kala Rog / पिछेती झुलसा)",
        "simple_name": "Late Blight (पत्तियों का काला पड़कर सड़ना)",
        "health_status": "Infected (बीमार)",
        "severity": "Severe (गंभीर / तुरंत इलाज चाहिए)",
        "symptoms": [
            "Patton par paani bheege jaise kaale-bhoore geelay dhabbe",
            "Patte ke nichle hisse par safed-dhundhli fafund dikhti hai",
            "Do se teen din me poora paudha aur tana murjha kar kaala padne lagta hai"
        ],
        "root_cause": (
            "Yeh ek bahut aakramak fafundi (Phytophthora) ke karan hota hai. "
            "Thanda mausam (15°C-20°C), badal chhaaye rehna aur lagatar jhim-jhim barish ya ghani "
            "dhundh/kohra hone par yeh bimari aati hai aur poore khet ko tezi se barbaad kar sakti hai."
        ),
        "organic_remedies": [
            "Rogi Paudhe Nikalein: Roggrast hisso ko polythene bag me band karke khet se door phenkein ya jala dein.",
            "Copper Sulfate (Bordeaux Mixture): 1% Bordaux mix ka ghol banakar turant spray karein.",
            "Gaumutra aur Neem Ark: 1 litre gaumutra + 50ml neem ark 10 litre paani me milakar chhidkein."
        ],
        "chemical_remedies": [
            "Ridomil Gold (Metalaxyl + Mancozeb): 2 gram prati litre paani me gholkar turant chhidkaav karein.",
            "Cymoxanil + Mancozeb (Curzate): 2 se 2.5 gram prati litre paani me milakar spray karein.",
            "Dimethomorph (Acrobat): 1 gram prati litre paani me milakar prayog karein."
        ],
        "preventive_measures": [
            "Hamesha pramanit aur bimari-mukt beej (certified seed) ka hi prayog karein.",
            "Mausam me kohra aur thand badhne par bimari aane se pehle hi Mancozeb ka roktham chhidkaav karein.",
            "Khet me paani ki nikasi (drainage) behtar banayein."
        ]
    },
    "leaf_spot": {
        "disease_name": "Leaf Spot (Patton ke Dhabbe / टिक्का व पत्ती धब्बा रोग)",
        "simple_name": "Leaf Spot (पत्तियों पर छोटे-छोटे धब्बे)",
        "health_status": "Infected (बीमार)",
        "severity": "Moderate (मध्यम)",
        "symptoms": [
            "Patton par chhote-chhote gol bhoore, kaale ya laal rang ke dhabbe",
            "Dhabbo ke chaaron taraf patti peeli pad jati hai",
            "Jyada bimari me dhabbe aapas me mil jate hain aur patti sookh kar gir jati hai"
        ],
        "root_cause": (
            "Fafundi (Fungus/Bacteria) ke kano se hota hai. Barish ke samay mitti ke chheente "
            "patton par padne se ya gande paani ke chhidkaav se yeh rog paudhe me lagta hai."
        ),
        "organic_remedies": [
            "Neeche ke Dhabbedar Patte Hatayein: Zameen ke paas ke 6 inch tak ke sabhi dhabbedar patte kaat dein.",
            "Neem Oil Spray: 5ml Neem Oil 1 litre paani me gholkar hafte me 1 baar spray karein.",
            "Haldi aur Chhaachh Ghol: 100 gram haldi powder 1 litre chhaachh me gholkar 10 litre paani me milakar spray karein."
        ],
        "chemical_remedies": [
            "Chlorothalonil (Kavach): 2 gram prati litre paani me milakar chhidkein.",
            "Carbendazim + Mancozeb (Saaf): 2 gram prati litre paani me gholkar spray karein.",
            "Copper Oxychloride: 2.5 gram prati litre paani me milakar spray karein."
        ],
        "preventive_measures": [
            "Khet me sookhi ghaas ya mulch bichhayein taaki mitti patton par na uchhale.",
            "Drip irrigation ya jado ke paas paani dein, phuhar se patte na bhigoyen.",
            "Fasal chakra (crop rotation) apnayein."
        ]
    },
    "leaf_curl": {
        "disease_name": "Leaf Curl (Patte Mudna / Churda-Murda Rog / मरोड़िया रोग)",
        "simple_name": "Leaf Curl (पत्तियों का मुड़ना व सिकुड़ना)",
        "health_status": "Infected (बीमार)",
        "severity": "Moderate to Severe (मध्यम से गंभीर)",
        "symptoms": [
            "Patte katori ke aakar me upar ya neeche ki taraf mud jate hain",
            "Pattiyaan moti, khurduri aur sikudi hui dikhti hain",
            "Paudhe ka vikas ruk jata hai aur phool/fal nahi aate"
        ],
        "root_cause": (
            "Ras choosne wale keede (jaise Safed Makkhi/Whitefly, Thrips, Mites) patton ka ras chooste hain "
            "aur paudhe me virus (Vishaanoo) faila dete hain. Khushk aur garm mausam me keede tezi se badhte hain."
        ),
        "organic_remedies": [
            "Peele aur Neele Chipchipe Card (Yellow/Blue Sticky Traps): Khet me 6-8 sticky traps lagayein jo safed makkhi aur thrips ko pakadte hain.",
            "Neem Oil Chhidkaav: 5ml Neem Oil (15000 PPM) prati litre paani me milakar har 5 din par chhidkein.",
            "Khurdure Rogi Paudhe Ukhadein: Agar 1-2 paudho me bimari shuru hui hai toh unhe ukhad kar door zameen me daba dein."
        ],
        "chemical_remedies": [
            "Keedo ki Roktham ke liye (Thrips/Makkhi): Imidacloprid 17.8% SL (0.5 ml prati litre) ya Thiamethoxam 25% WG (0.5 gram prati litre paani).",
            "Mite (Makdi) hone par: Spiromesifen (Oberon) 1 ml prati litre paani me milakar spray karein.",
            "Acetamiprid 20% SP: 0.5 gram prati litre paani me milakar chhidkein."
        ],
        "preventive_measures": [
            "Paudha lagate samay beej ko keetnashak se upcharit (seed treatment) karein.",
            "Khet ke aas-paas kharpatwaar (weeds) saaf rakhein jahan safed makkhi panapti hai.",
            "Peele sticky trap khet me shuruat se hi lagayein."
        ]
    },
    "rice_blast": {
        "disease_name": "Rice Blast (Dhan ka Jhulsa / धान का झुलसा रोग)",
        "simple_name": "Rice Blast (धान की पत्तियों पर आंख जैसे धब्बे)",
        "health_status": "Infected (बीमार)",
        "severity": "Severe (गंभीर)",
        "symptoms": [
            "Patton par naav ya aankh ke aakar ke dhabbe (Spindle-shaped spots)",
            "Dhabbe ke beech ka hissa raakh jaisa aur kinare bhoore hote hain",
            "Dhabbe badhkar poori patti ko jhulsa kar sookha dete hain"
        ],
        "root_cause": (
            "Fafundi (Magnaporthe) ke karan hota hai. Dhan ke khet me zaroorat se zyada Urea (Nitrogen) daalne, "
            "hawa me 90% se zyada nami hone aur raat me halki thandi (20°C-26°C) hone par yeh rog lagta hai."
        ),
        "organic_remedies": [
            "Trichoderma viride: 1 kg Trichoderma ko 50 kg gobar khad me milakar khet me dalein.",
            "Gaumutra aur Neem Ghol: 10% gaumutra ghol ka chhidkaav karein.",
            "Urea Daalna Band Karein: Bimari dikhte hi khet me urea ka chhidkaav turant rok dein."
        ],
        "chemical_remedies": [
            "Tricyclazole 75% WP (Baan / Beam): 0.6 gram prati litre paani me gholkar chhidkaav karein (Blast rog ke liye sabse asardaar).",
            "Isoprothiolane 40% EC (Fuji-One): 1.5 se 2 ml prati litre paani me milakar spray karein.",
            "Kasugamycin 3% SL: 2 ml prati litre paani me gholkar chhidkein."
        ],
        "preventive_measures": [
            "Urea (Nitrogen) ko ek baar me na daalein, 3-4 kisto me baant kar dein aur Potash ki sahi matra dein.",
            "Khet me paani ka nikaas karke 2-3 din khet ko hawa lagne dein.",
            "Pratirodhi kismein jaise IR-64 ya Pusa Sugandh ka chayan karein."
        ]
    },
    "nutrient_deficiency": {
        "disease_name": "Nutrient Deficiency (Khad/Poshak Tatva ki Kami / पोषक तत्वों की कमी)",
        "simple_name": "Nutrient Deficiency (पत्तियों का पीला पड़ना - खाद की कमी)",
        "health_status": "Infected (बीमार - पोषक तत्व की कमी)",
        "severity": "Mild to Moderate (हल्की से मध्यम)",
        "symptoms": [
            "Pattiyaan peeli pad rahi hain par koi fafund ya kide nahi hain",
            "Patti ki nasen (veins) hari rehti hain aur beech ka hissa peela hota hai (Iron/Magnesium kami)",
            "Neeche ke purane patte peele pad rahe hain (Nitrogen kami)"
        ],
        "root_cause": (
            "Mitti me jaroori khad (jaise Nitrogen, Iron, ya Magnesium) ki kami hone, "
            "ya mitti me zyada paani bharne se jadon dwara khurak na lene ke karan patte peele padte hain."
        ),
        "organic_remedies": [
            "Sadi Gobar Khad / Vermicompost: Paudhe ke jad ke paas 2 mutthi achhi vermicompost khad dalein.",
            "Epsom Salt (Magnesium Sulfate): 1 litre paani me 1 chammach Epsom salt gholkar patton par spray karein.",
            "Khad Ghol (Liquid Compost Tea): Gobar khad ka ras nikaal kar paani me milakar jadon me dein."
        ],
        "chemical_remedies": [
            "Micronutrient Mixture (Sookshma Poshak Tatva): 2 se 2.5 gram prati litre paani me milakar spray karein.",
            "Chelated Iron (EDTA Iron 12%): 1 gram prati litre paani me milakar chhidkein (agar nasen hari aur patta peela ho).",
            "NPK 19:19:19 ya 20:20:20: 5 gram prati litre paani me gholkar patton par chhidkaav karein."
        ],
        "preventive_measures": [
            "Khet/gamle ki mitti me paani jamne na dein, jal-nikasi theek rakhein.",
            "Har saal fasal bone se pehle khet me achhi gobar ki khad dalein.",
            "Mitti ki jaanch (Soil Test) karwayein taaki zaroori poshak tatvo ka pata chal sake."
        ]
    },
    "healthy": {
        "disease_name": "Healthy Foliage (Swasth Paudha / बिल्कुल स्वस्थ पत्ता)",
        "simple_name": "Healthy Foliage (स्वस्थ फसल / कोई बीमारी नहीं)",
        "health_status": "Healthy (स्वस्थ)",
        "severity": "None (कोई बीमारी नहीं)",
        "symptoms": [
            "Patton ka rang chamakdaar hara aur ek-samaan hai",
            "Patte par koi daag-dhabba, kida ya fafundi nahi hai",
            "Patti ke kinaray bilkul saaf aur swasth hain"
        ],
        "root_cause": (
            "Aapka paudha bilkul swasth hai! Paudhe ko zaroori dhoop, sahi matra me paani aur "
            "santulit poshan (nutrition) mil raha hai. Khet me koi hanikarak fafundi ya keeda maujood nahi hai."
        ),
        "organic_remedies": [
            "Niyamit Dekhbhal: Paudhe ki zaroorat ke hisaab se sahi samay par paani dete rahein.",
            "Mulching: Jadon ke paas thodi sookhi ghaas ki parat rakhein taaki nami bani rahe.",
            "Suraksha Spray: Har 15-20 din me halke Neem Tel (3ml/litre) ka spray karein taaki keede aane se pehle hi door rahein."
        ],
        "chemical_remedies": [
            "Kisi bhi chemical dawai ya fafundinashak ki zaroorat nahi hai.",
            "Phal/phool aate samay zaroorat padne par halki NPK khad de sakte hain."
        ],
        "preventive_measures": [
            "Hafte me ek baar patton ke neeche ke hisse ki jaanch karte rahein.",
            "Paani dete samay paani jad me dein, patton ko zyada gila na rakhein.",
            "Hawa aur dhoop ka aana-jaana banaye rakhein."
        ]
    }
}

def get_disease_profile(key: str) -> Dict[str, Any]:
    """Retrieve disease profile by key with safe fallback to healthy profile."""
    return DISEASE_PROFILES.get(key, DISEASE_PROFILES["healthy"])

def list_known_diseases() -> List[Dict[str, str]]:
    """Return summary list of all known disease profiles with simple names."""
    return [
        {
            "key": k,
            "name": v["disease_name"],
            "simple_name": v.get("simple_name", v["disease_name"]),
            "status": v["health_status"]
        }
        for k, v in DISEASE_PROFILES.items()
    ]
