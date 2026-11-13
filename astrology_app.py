import streamlit as st
from datetime import datetime, time
from kerykeion import AstrologicalSubject, KerykeionChartSVG
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import tempfile
import os

st.set_page_config(
    page_title="निर्मोही निरञ्जन | Nirmohi Niranjan",
    page_icon="🕉️",
    layout="wide"
)

# Language dictionaries
TRANSLATIONS = {
    "en": {
        "title": "निर्मोही निरञ्जन",
        "subtitle": "Nirmohi Niranjan — Birth Chart & Spiritual Guidance",
        "intro": "Enter your birth details to receive your natal chart and personalised guidance. Ask questions about career, marriage, finance, or any life area.",
        "name": "Name (optional)",
        "dob": "Date of Birth",
        "tob": "Time of Birth",
        "place": "Place of Birth",
        "place_ph": "e.g. London, UK or Mumbai, India",
        "generate": "Generate Birth Chart",
        "language": "Language",
        "location_found": "Location found",
        "timezone": "Timezone",
        "chart": "Natal Birth Chart",
        "planets": "Planetary Positions",
        "key_points": "Key Points",
        "ascendant": "Ascendant",
        "sun": "Sun",
        "moon": "Moon",
        "ask": "Ask a Question",
        "ask_ph": "e.g. What does my chart say about career or marriage?",
        "get_pred": "Get Guidance",
        "general": "General Guidance",
        "footer": "Powered by Swiss Ephemeris. For spiritual reflection only — not a substitute for professional advice.",
        "geocode_error": "Could not find the place. Please try a more specific location.",
        "enter_place": "Please enter a place of birth.",
        "calculating": "Calculating your chart...",
        "career": "Career & Profession",
        "marriage": "Marriage & Relationships",
        "finance": "Finance & Prosperity",
        "health": "Health & Well-being",
        "note": "This reading is based on classical principles for self-reflection. Consult a qualified astrologer for personal guidance."
    },
    "hi": {
        "title": "निर्मोही निरञ्जन",
        "subtitle": "निर्मोही निरञ्जन — जन्म कुंडली एवं आध्यात्मिक मार्गदर्शन",
        "intro": "अपना जन्म विवरण दर्ज करें और अपनी कुंडली तथा व्यक्तिगत मार्गदर्शन प्राप्त करें। करियर, विवाह, वित्त या किसी भी विषय पर प्रश्न पूछें।",
        "name": "नाम (वैकल्पिक)",
        "dob": "जन्म तिथि",
        "tob": "जन्म समय",
        "place": "जन्म स्थान",
        "place_ph": "उदाहरण: मुंबई, भारत या दिल्ली",
        "generate": "कुंडली बनाएँ",
        "language": "भाषा",
        "location_found": "स्थान मिला",
        "timezone": "समय क्षेत्र",
        "chart": "जन्म कुंडली",
        "planets": "ग्रह स्थिति",
        "key_points": "मुख्य बिंदु",
        "ascendant": "लग्न",
        "sun": "सूर्य",
        "moon": "चंद्र",
        "ask": "प्रश्न पूछें",
        "ask_ph": "उदाहरण: मेरे करियर या विवाह के बारे में क्या कहती है कुंडली?",
        "get_pred": "मार्गदर्शन प्राप्त करें",
        "general": "सामान्य मार्गदर्शन",
        "footer": "स्विस एफेमेरिस द्वारा संचालित। केवल आध्यात्मिक चिंतन हेतु — पेशेवर सलाह का विकल्प नहीं।",
        "geocode_error": "स्थान नहीं मिला। कृपया अधिक स्पष्ट स्थान दर्ज करें।",
        "enter_place": "कृपया जन्म स्थान दर्ज करें।",
        "calculating": "आपकी कुंडली की गणना हो रही है...",
        "career": "करियर एवं व्यवसाय",
        "marriage": "विवाह एवं संबंध",
        "finance": "वित्त एवं समृद्धि",
        "health": "स्वास्थ्य एवं कल्याण",
        "note": "यह पाठ शास्त्रीय सिद्धांतों पर आधारित आत्म-चिंतन हेतु है। व्यक्तिगत मार्गदर्शन के लिए योग्य ज्योतिषी से परामर्श करें।"
    },
    "gu": {
        "title": "નિર્મોહી નિરંજન",
        "subtitle": "નિર્મોહી નિરંજન — જન્મ કુંડળી અને આધ્યાત્મિક માર્ગદર્શન",
        "intro": "તમારી જન્મ વિગતો દાખલ કરો અને તમારી કુંડળી તથા વ્યક્તિગત માર્ગદર્શન મેળવો. કારકિર્દી, લગ્ન, નાણાં અથવા કોઈપણ વિષય વિશે પ્રશ્ન પૂછો.",
        "name": "નામ (વૈકલ્પિક)",
        "dob": "જન્મ તારીખ",
        "tob": "જન્મ સમય",
        "place": "જન્મ સ્થળ",
        "place_ph": "ઉદાહરણ: મુંબઈ, ભારત અથવા અમદાવાદ",
        "generate": "કુંડળી બનાવો",
        "language": "ભાષા",
        "location_found": "સ્થળ મળ્યું",
        "timezone": "સમય ક્ષેત્ર",
        "chart": "જન્મ કુંડળી",
        "planets": "ગ્રહ સ્થિતિ",
        "key_points": "મુખ્ય મુદ્દા",
        "ascendant": "લગ્ન",
        "sun": "સૂર્ય",
        "moon": "ચંદ્ર",
        "ask": "પ્રશ્ન પૂછો",
        "ask_ph": "ઉદાહરણ: મારી કારકિર્દી અથવા લગ્ન વિશે કુંડળી શું કહે છે?",
        "get_pred": "માર્ગદર્શન મેળવો",
        "general": "સામાન્ય માર્ગદર્શન",
        "footer": "સ્વિસ એફેમેરિસ દ્વારા સંચાલિત. માત્ર આધ્યાત્મિક ચિંતન માટે — વ્યાવસાયિક સલાહનો વિકલ્પ નથી.",
        "geocode_error": "સ્થળ મળ્યું નથી. કૃપા કરીને વધુ સ્પષ્ટ સ્થળ દાખલ કરો.",
        "enter_place": "કૃપા કરીને જન્મ સ્થળ દાખલ કરો.",
        "calculating": "તમારી કુંડળીની ગણતરી થઈ રહી છે...",
        "career": "કારકિર્દી અને વ્યવસાય",
        "marriage": "લગ્ન અને સંબંધો",
        "finance": "નાણાં અને સમૃદ્ધિ",
        "health": "આરોગ્ય અને કલ્યાણ",
        "note": "આ વાંચન શાસ્ત્રીય સિદ્ધાંતો પર આધારિત આત્મ-ચિંતન માટે છે. વ્યક્તિગત માર્ગદર્શન માટે યોગ્ય જ્યોતિષીની સલાહ લો."
    }
}

SIGN_NAMES = {
    "en": {"Ari": "Aries", "Tau": "Taurus", "Gem": "Gemini", "Can": "Cancer", "Leo": "Leo", "Vir": "Virgo",
           "Lib": "Libra", "Sco": "Scorpio", "Sag": "Sagittarius", "Cap": "Capricorn", "Aqu": "Aquarius", "Pis": "Pisces"},
    "hi": {"Ari": "मेष", "Tau": "वृषभ", "Gem": "मिथुन", "Can": "कर्क", "Leo": "सिंह", "Vir": "कन्या",
           "Lib": "तुला", "Sco": "वृश्चिक", "Sag": "धनु", "Cap": "मकर", "Aqu": "कुंभ", "Pis": "मीन"},
    "gu": {"Ari": "મેષ", "Tau": "વૃષભ", "Gem": "મિથુન", "Can": "કર્ક", "Leo": "સિંહ", "Vir": "કન્યા",
           "Lib": "તુલા", "Sco": "વૃશ્ચિક", "Sag": "ધનુ", "Cap": "મકર", "Aqu": "કુંભ", "Pis": "મીન"}
}

@st.cache_resource
def get_geocoder():
    return Nominatim(user_agent="nirmohi_niranjan_app")

@st.cache_resource
def get_tf():
    return TimezoneFinder()

geolocator = get_geocoder()
tf = get_tf()

def get_place_coords(place: str):
    try:
        location = geolocator.geocode(place, timeout=10)
        if location:
            return location.latitude, location.longitude, location.address
        return None, None, None
    except Exception:
        return None, None, None

def get_timezone(lat, lng):
    try:
        return tf.timezone_at(lat=lat, lng=lng) or "UTC"
    except:
        return "UTC"

def create_subject(name, year, month, day, hour, minute, lat, lng, tz):
    return AstrologicalSubject(
        name=name or "Native",
        year=year, month=month, day=day,
        hour=hour, minute=minute,
        lng=lng, lat=lat, tz_str=tz, online=False
    )

def generate_chart_svg(subject):
    with tempfile.TemporaryDirectory() as tmpdir:
        chart = KerykeionChartSVG(subject, new_output_directory=tmpdir)
        chart.makeSVG()
        svg_files = [f for f in os.listdir(tmpdir) if f.endswith(".svg")]
        if svg_files:
            with open(os.path.join(tmpdir, svg_files[0]), "r", encoding="utf-8") as f:
                return f.read()
    return None

def planet_summary(subject, lang):
    planets = ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"]
    data = []
    for p in planets:
        planet = getattr(subject, p, None)
        if planet:
            sign_name = SIGN_NAMES[lang].get(planet.sign, planet.sign)
            house_num = int(planet.house.split("_")[0]) if planet.house else None
            data.append({
                "Planet": planet.name,
                "Sign": sign_name,
                "House": house_num or "—",
                "Degree": f"{planet.position:.1f}°",
                "R": "℞" if planet.retrograde else ""
            })
    return data

def interpret(subject, topic, lang, t):
    topic = topic.lower()
    lines = []

    if any(w in topic for w in ["job", "career", "work", "profession", "business", "करियर", "नौकरी", "વ્યવસાય", "કારકિર્દી"]):
        lines.append(f"**{t['career']}**")
        lines.append(f"10th House: {SIGN_NAMES[lang].get(subject.tenth_house.sign, subject.tenth_house.sign)}")
        lines.append(f"Sun: {SIGN_NAMES[lang].get(subject.sun.sign)} ({subject.sun.house})")
        lines.append(f"Saturn: {SIGN_NAMES[lang].get(subject.saturn.sign)} ({subject.saturn.house})")
    elif any(w in topic for w in ["marriage", "love", "relationship", "partner", "विवाह", "शादी", "લગ્ન", "પ્રેમ"]):
        lines.append(f"**{t['marriage']}**")
        lines.append(f"7th House: {SIGN_NAMES[lang].get(subject.seventh_house.sign)}")
        lines.append(f"Venus: {SIGN_NAMES[lang].get(subject.venus.sign)} ({subject.venus.house})")
        lines.append(f"Moon: {SIGN_NAMES[lang].get(subject.moon.sign)} ({subject.moon.house})")
    elif any(w in topic for w in ["finance", "money", "wealth", "धन", "पैसे", "નાણાં", "ધન"]):
        lines.append(f"**{t['finance']}**")
        lines.append(f"2nd House: {SIGN_NAMES[lang].get(subject.second_house.sign)}")
        lines.append(f"Jupiter: {SIGN_NAMES[lang].get(subject.jupiter.sign)} ({subject.jupiter.house})")
    elif any(w in topic for w in ["health", "स्वास्थ्य", "આરોગ્ય"]):
        lines.append(f"**{t['health']}**")
        lines.append(f"Sun: {SIGN_NAMES[lang].get(subject.sun.sign)}")
        lines.append(f"6th House: {SIGN_NAMES[lang].get(subject.sixth_house.sign)}")
    else:
        lines.append(f"**{t['general']}**")
        lines.append(f"{t['sun']}: {SIGN_NAMES[lang].get(subject.sun.sign)} ({subject.sun.house})")
        lines.append(f"{t['moon']}: {SIGN_NAMES[lang].get(subject.moon.sign)} ({subject.moon.house})")
        lines.append(f"{t['ascendant']}: {SIGN_NAMES[lang].get(subject.first_house.sign)}")

    lines.append(f"\n*{t['note']}*")
    return "\n\n".join(lines)

# --- UI ---
lang = st.sidebar.selectbox(
    "Language / भाषा / ભાષા",
    options=["en", "hi", "gu"],
    format_func=lambda x: {"en": "English", "hi": "हिन्दी", "gu": "ગુજરાતી"}[x]
)
t = TRANSLATIONS[lang]

# Header with logo
col_logo, col_title = st.columns([1, 4])
with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=140)
with col_title:
    st.markdown(f"# {t['title']}")
    st.markdown(f"### {t['subtitle']}")

st.markdown(t["intro"])

# Sidebar inputs
with st.sidebar:
    st.header(t["title"])
    name = st.text_input(t["name"])
    birth_date = st.date_input(t["dob"], value=datetime(1990, 1, 1).date())
    birth_time = st.time_input(t["tob"], value=time(12, 0))
    place = st.text_input(t["place"], placeholder=t["place_ph"])
    generate = st.button(t["generate"], type="primary")

if generate and place:
    with st.spinner(t["calculating"]):
        lat, lng, full_place = get_place_coords(place)
        if lat is None:
            st.error(t["geocode_error"])
        else:
            tz = get_timezone(lat, lng)
            st.success(f"{t['location_found']}: {full_place} | {t['timezone']}: {tz}")

            subject = create_subject(
                name, birth_date.year, birth_date.month, birth_date.day,
                birth_time.hour, birth_time.minute, lat, lng, tz
            )

            st.subheader(t["chart"])
            svg = generate_chart_svg(subject)
            if svg:
                st.components.v1.html(svg, height=620, scrolling=True)

            st.subheader(t["planets"])
            st.dataframe(planet_summary(subject, lang), use_container_width=True, hide_index=True)

            st.subheader(t["key_points"])
            c1, c2, c3 = st.columns(3)
            c1.metric(t["ascendant"], SIGN_NAMES[lang].get(subject.first_house.sign, "—"))
            c2.metric(t["sun"], SIGN_NAMES[lang].get(subject.sun.sign, "—"))
            c3.metric(t["moon"], SIGN_NAMES[lang].get(subject.moon.sign, "—"))

            st.subheader(t["ask"])
            question = st.text_area(t["ask"], placeholder=t["ask_ph"], height=100)
            if st.button(t["get_pred"]) or (question and question.strip()):
                if question and question.strip():
                    st.markdown(interpret(subject, question, lang, t))
                else:
                    st.info(t["ask_ph"])

            with st.expander(t["general"]):
                st.markdown(interpret(subject, "general", lang, t))

elif generate:
    st.warning(t["enter_place"])

st.markdown("---")
st.caption(t["footer"])
