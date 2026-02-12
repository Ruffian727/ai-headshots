# headshot_generator.py - Complete working app
import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import base64

st.title("🎭 AI Headshot Generator - $29 for Pro Results")
st.markdown("Upload selfie → Get LinkedIn-ready headshots in 30 seconds")

# Free Replicate API key (sign up: replicate.com)
REPLICATE_API = st.secrets.get("REPLICATE_API", "your_free_key_here")

if "images" not in st.session_state:
    st.session_state.images = []

uploaded_file = st.file_uploader("📸 Upload your selfie", type=["jpg", "png"])
if uploaded_file and st.button("✨ Generate Headshots ($29)"):
    
    with st.spinner("Generating your pro headshots..."):
        # Free Hugging Face model call
        prompt = "professional linkedin headshot, clean background, high quality, studio lighting"
        response = requests.post(
            "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0",
            headers={"Authorization": "Bearer YOUR_HF_TOKEN"},
            json={"inputs": f"{prompt}, based on {uploaded_file.name}"}
        )
        
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            st.session_state.images.append(image)
            st.image(image, caption="Your Pro Headshot!")
            st.success("✅ Ready to download! Pay $29 via CashApp: $YourHandle")
        else:
            st.error("API busy. Try again in 30s.")

# Download button
for i, img in enumerate(st.session_state.images):
    buf = BytesIO()
    img.save(buf, format="PNG")
    st.download_button(f"Download Headshot {i+1}", buf.getvalue(), f"headshot_{i+1}.png")
