
import streamlit as st
import numpy as np
import tf_keras
from PIL import Image

st.set_page_config(
    page_title="ZingZest",
    page_icon="🍋",
    layout="centered"
)

@st.cache_resource
def load_model():
    return tf_keras.models.load_model(
        "keras_model.h5",
        compile=False
    )

def load_labels():
    with open("labels.txt", "r") as file:
        return [
            line.strip().split(" ", 1)[-1]
            for line in file.readlines()
        ]

def predict_fruit(image):
    model = load_model()
    labels = load_labels()

    image = image.resize((224, 224))
    image_array = np.asarray(image).astype(np.float32)
    image_array = (image_array / 127.5) - 1
    image_array = np.expand_dims(image_array, axis=0)

    prediction = model.predict(image_array, verbose=0)[0]
    index = int(np.argmax(prediction))

    return labels[index], float(prediction[index]) * 100


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #FFF9EF;
    font-family: 'Fredoka', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

.main .block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    background: linear-gradient(135deg, #FFDCE7, #FFF0B8, #DDF5E4);
    border-radius: 32px;
    padding: 35px 20px;
    text-align: center;
    border: 3px solid white;
    box-shadow: 0 8px 25px #e9d8c5;
}

.logo {
    font-size: 48px;
    font-weight: 700;
    color: #E66D91;
    margin: 0;
}

.tagline {
    color: #806A7C;
    font-size: 19px;
}

.fruit-row {
    font-size: 38px;
    margin: 18px 0 5px 0;
    letter-spacing: 9px;
}

.section-title {
    color: #6B8061;
    font-size: 25px;
    font-weight: 600;
    text-align: center;
    margin-top: 30px;
}

.info-card {
    background: white;
    border: 2px solid #F7DCE4;
    border-radius: 23px;
    padding: 22px;
    text-align: center;
    color: #806A7C;
    margin: 12px 0;
}

.result-card {
    background: linear-gradient(135deg, #FFE3EC, #FFF3C9);
    border: 3px solid white;
    border-radius: 25px;
    padding: 25px;
    text-align: center;
    color: #806A7C;
    margin-top: 20px;
}

div.stButton > button {
    background: #FF8FAB;
    color: white;
    border: none;
    border-radius: 30px;
    padding: 12px 25px;
    font-family: 'Fredoka', sans-serif;
    font-size: 19px;
    font-weight: 600;
    width: 100%;
}

div.stButton > button:hover {
    background: #F47799;
    color: white;
    border: none;
}

.footer {
    text-align: center;
    color: #A18AA0;
    font-size: 15px;
    margin-top: 35px;
}
</style>

<div class="hero">
    <p class="logo">🍋 ZingZest 🍓</p>
    <p class="tagline">A little fruit adventure awaits!</p>
    <div class="fruit-row">🍎 🍌 🥭 🍇 🍉</div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<p class="section-title">🌈 Ready to explore?</p>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="info-card">
    <h2>🍊 Meet your fruity world!</h2>
    <p>Discover fruits, one picture at a time.</p>
    <p>Simply take a photo and let our AI help identify it!</p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<p class="section-title">📸 Your fruit scanner</p>',
    unsafe_allow_html=True
)

photo = st.camera_input("Take a picture of a fruit")

if photo is not None:
    image = Image.open(photo).convert("RGB")
    st.image(image, caption="Your fruity picture", use_container_width=True)

    with st.spinner("🍓 ZingZest is identifying your fruit..."):
        try:
            fruit, confidence = predict_fruit(image)

            st.markdown(f"""
            <div class="result-card">
                <h2>🎉 It's a {fruit.capitalize()}!</h2>
                <p>Your fruit has been recognised!</p>
                <h3>✨ Confidence: {confidence:.1f}%</h3>
            </div>
            """, unsafe_allow_html=True)

        except Exception as error:
            st.error("Oops! Something went wrong while recognising the fruit.")
            st.exception(error)

st.markdown("""
<div class="footer">
    🍒 Stay curious • Eat colourful • Keep it fruity! 🍒
</div>
""", unsafe_allow_html=True)
