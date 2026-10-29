
import streamlit as st
from datetime import date, timedelta

st.set_page_config(
    page_title="AI Crop Doctor",
    page_icon="🌱",
    layout="wide"
)

# Approximate maturity durations in days.
# Actual timing varies by variety, climate and growing conditions.
CROPS = {
    "Wheat / گندم": 130,
    "Rice / چاول": 120,
    "Maize / مکئی": 100,
    "Cotton / کپاس": 160,
    "Sugarcane / گنا": 300,
    "Potato / آلو": 100,
    "Tomato / ٹماٹر": 90,
    "Onion / پیاز": 120,
    "Chickpea / چنا": 120,
    "Lentil / مسور": 110,
    "Mustard / سرسوں": 120,
    "Barley / جو": 110,
    "Sunflower / سورج مکھی": 100,
    "Sorghum / جوار": 100,
    "Millet / باجرا": 90,
    "Sugar beet / چقندر": 160,
    "Peas / مٹر": 90,
    "Chilli / مرچ": 120,
    "Brinjal / بینگن": 100,
    "Okra / بھنڈی": 60,
    "Cucumber / کھیرا": 60,
    "Pumpkin / کدو": 100,
    "Watermelon / تربوز": 90,
    "Carrot / گاجر": 100,
    "Cauliflower / پھول گوبھی": 100,
    "Cabbage / بند گوبھی": 100,
    "Garlic / لہسن": 150,
    "Spinach / پالک": 45,
    "Apple / سیب": 180,
    "Mango / آم": 150,
    "Banana / کیلا": 300,
    "Grapes / انگور": 150,
    "Orange / مالٹا": 240,
    "Guava / امرود": 150,
    "Papaya / پپیتا": 240,
    "Other / دوسری فصل": 120,
}

st.title("🌱 AI Crop Doctor & Harvest Predictor")
st.caption("Smart farming assistant | سمارٹ زرعی معاون")

language = st.radio(
    "Language / زبان",
    ["English", "اردو"],
    horizontal=True
)

urdu = language == "اردو"

if urdu:
    st.write("فصل کی معلومات، تصویر اور کٹائی کے وقت کا ابتدائی اندازہ حاصل کریں۔")
else:
    st.write("Upload a crop photo, review possible plant-health concerns, and estimate harvest timing.")

tab1, tab2, tab3 = st.tabs([
    "🌿 Crop & Harvest",
    "🔬 Disease Check",
    "ℹ️ About"
])

with tab1:
    st.subheader("فصل کی معلومات" if urdu else "Crop Information")

    crop = st.selectbox(
        "فصل منتخب کریں / Select crop",
        list(CROPS.keys())
    )

    sowing_date = st.date_input(
        "بوائی کی تاریخ / Sowing date",
        value=date.today() - timedelta(days=30),
        max_value=date.today()
    )

    stage = st.selectbox(
        "Growth stage / فصل کی موجودہ حالت",
        [
            "Seedling / ابتدائی بڑھوتری",
            "Vegetative / پتوں اور تنے کی بڑھوتری",
            "Flowering / پھول",
            "Fruit or grain development / پھل یا دانہ",
            "Maturing / پکنے کے قریب"
        ]
    )

    photo = st.file_uploader(
        "فصل یا پتے کی تصویر اپ لوڈ کریں",
        type=["jpg", "jpeg", "png"]
    )

    if photo:
        st.image(photo, caption="Uploaded crop photo", width=350)
        st.info(
            "Image uploaded. A trained AI model is needed to "
            "identify the crop or diagnose disease from this image."
        )

    if st.button("Estimate Harvest / کٹائی کا اندازہ", type="primary"):
        days = CROPS[crop]
        elapsed = (date.today() - sowing_date).days

        if sowing_date > date.today():
            st.error("Sowing date cannot be in the future.")
        else:
            remaining = max(0, days - elapsed)
            estimated_date = date.today() + timedelta(days=remaining)

            st.metric(
                "Approx. days remaining / باقی دن",
                remaining
            )
            st.write(
                "Estimated harvest date / متوقع کٹائی:",
                estimated_date.strftime("%d %B %Y")
            )
            st.warning(
                "This is a rough estimate, not an AI prediction. "
                "Crop variety, planting method, weather and growth "
                "stage can change the actual harvest date."
            )

with tab2:
    st.subheader("Plant Health Check / فصل کی صحت")

    st.write(
        "Select visible symptoms. This questionnaire does not "
        "confirm a disease."
    )

    symptoms = st.multiselect(
        "Observed symptoms / نظر آنے والی علامات",
        [
            "Yellow leaves / پیلے پتے",
            "Brown or black spots / بھورے یا کالے دھبے",
            "White powder / سفید پاؤڈر",
            "Wilting / پودا مرجھانا",
            "Holes in leaves / پتوں میں سوراخ",
            "Rotting / گلنا",
            "Stunted growth / نشوونما میں کمی",
            "No visible symptoms / کوئی علامت نہیں"
        ]
    )

    if st.button("Review Symptoms / علامات دیکھیں"):
        if not symptoms:
            st.info("Please select any observed symptoms.")
        elif "No visible symptoms / کوئی علامت نہیں" in symptoms:
            st.info(
                "No symptoms selected for review. Continue monitoring "
                "the crop and inspect both sides of the leaves."
            )
        else:
            st.write("Selected symptoms / منتخب علامات:")
            for symptom in symptoms:
                st.write("- " + symptom)

            st.warning(
                "These symptoms can have several causes, including "
                "disease, pests, nutrient problems or water stress. "
                "A trained crop-specific model or agricultural expert "
                "is needed for a more reliable diagnosis."
            )

with tab3:
    st.subheader("About / تعارف")
    st.write(
        "This is an initial crop-management prototype. "
        "It does not yet include a trained image-recognition model "
        "or live weather data."
    )
    st.write(
        "یہ ابتدائی نمونہ ہے۔ درست بیماری کی شناخت اور بہتر "
        "کٹائی کے اندازے کے لیے تربیت یافتہ AI ماڈل، فصل کی قسم "
        "اور مقامی موسمی معلومات درکار ہوں گی۔"
    )
