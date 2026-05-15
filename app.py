import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import pyttsx3
import uuid
import os

# ---------------- PAGE ----------------
st.set_page_config(page_title="AI Studio Pro", layout="wide")

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align:center; color:#60a5fa;'>
🚀 AI Studio Pro
</h1>

<h4 style='text-align:center; color:#a1a1aa;'>
Created by <b>Pallavi Khadse</b>
</h4>
""", unsafe_allow_html=True)

# ---------------- STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1220, #111827);
    color: white;
}

.card {
    background: #1f2937;
    padding: 12px;
    border-radius: 12px;
    margin: 8px 0;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------------- OLLAMA ----------------
def ask_ollama(prompt):
    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "tinyllama", "prompt": prompt, "stream": False},
            timeout=120
        )
        return res.json().get("response", "")
    except Exception as e:
        return str(e)

# ---------------- IMAGE ----------------
def generate_image(prompt):
    url = f"https://image.pollinations.ai/prompt/{prompt}"
    res = requests.get(url)

    if res.status_code == 200:
        return Image.open(BytesIO(res.content))
    return None

# ---------------- AUDIO (FIXED + SPEED + DOWNLOAD) ----------------
def generate_audio_file(text, speed=150):
    engine = pyttsx3.init()

    # SPEED CONTROL
    engine.setProperty('rate', speed)

    filename = f"audio_{uuid.uuid4().hex}.mp3"
    folder = "temp_audio"
    os.makedirs(folder, exist_ok=True)

    filepath = os.path.join(folder, filename)

    engine.save_to_file(text, filepath)
    engine.runAndWait()

    return filepath

# ---------------- SIDEBAR ----------------
st.sidebar.title("🚀 AI Studio Pro")

mode = st.sidebar.radio("Select Feature", [
    "💬 Chat AI",
    "🎨 Image Generator",
    "🔊 Audio AI"
])

st.title("🔥 AI Multi Tool (Offline + Free)")

# ================= CHAT =================
if mode == "💬 Chat AI":

    user = st.text_input("Ask anything")

    if st.button("Send"):
        if user:
            reply = ask_ollama(user)
            st.session_state.chat.append(("You", user))
            st.session_state.chat.append(("AI", reply))

    for r, m in st.session_state.chat:
        st.markdown(f"<div class='card'><b>{r}:</b> {m}</div>", unsafe_allow_html=True)

# ================= IMAGE =================
elif mode == "🎨 Image Generator":

    prompt = st.text_input("Describe image")

    if st.button("Generate Image"):
        if prompt:
            img = generate_image(prompt)

            if img:
                st.image(img)

                buf = BytesIO()
                img.save(buf, format="PNG")

                st.download_button(
                    "⬇ Download Image",
                    data=buf.getvalue(),
                    file_name="image.png",
                    mime="image/png"
                )

# ================= AUDIO =================
elif mode == "🔊 Audio AI":

    st.subheader("🔊 Advanced Audio Generator")

    text = st.text_input("Enter text to convert to speech")

    speed = st.slider("🎚 Speech Speed", 80, 250, 150)

    if st.button("Generate Audio"):
        if text:

            path = generate_audio_file(text, speed)

            st.success("Audio Generated!")

            with open(path, "rb") as f:
                audio_bytes = f.read()

            # PLAY AUDIO
            st.audio(audio_bytes, format="audio/mp3")

            # DOWNLOAD AUDIO
            st.download_button(
                "⬇ Download Audio",
                data=audio_bytes,
                file_name="speech.mp3",
                mime="audio/mp3"
            )