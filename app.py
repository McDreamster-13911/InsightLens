import os
import google.generativeai as genai
import PIL.Image as pillow_image
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()



# Get API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

headers = {
    "authorization" : st.secrets["GEMINI_API_KEY"],
    "content-type" : "application/json"
}

# Set page config
st.set_page_config(page_title="Image Analyzer", page_icon="📸", layout="centered")

# Custom CSS for aesthetics
st.markdown(
    """
    <style>
        .stApp {
            background-color: #f4f4f4;
        }
        .stTextInput input {
            border-radius: 8px;
            padding: 10px;
        }
        .stButton button {
            background-color: #4CAF50 !important;
            color: white !important;
            font-size: 16px !important;
            padding: 10px 20px !important;
            border-radius: 10px !important;
        }
        
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.markdown("<h1 style='text-align: center; color: #333;'>📷 Image Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>Analyze multiple images using AI</p>", unsafe_allow_html=True)

# User Input
prompt = st.text_input("🔍 Enter a prompt (e.g., 'Describe these images?')", key="input")

# File Upload for Multiple Images
image_files = st.file_uploader("📂 Upload one or more images (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key="image_files")

# Function to call API
def api_response(api_key, prompt, images):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name='gemini-2.0-flash')
    
    # Process images and send them along with the prompt
    responses = []
    for img in images:
        if prompt is "":
            prompt= "Analyze and describe the image(s)"
            response = model.generate_content([prompt, img])
            responses.append(response.text)
        else:
            response = model.generate_content([prompt, img])
            responses.append(response.text)
        
    
    return responses

# Display uploaded images
if image_files:
    st.markdown("### 🖼 Uploaded Image(s):")
    images = []
    for img_file in image_files:
        img = pillow_image.open(img_file)
        images.append(img)
        st.image(img, caption=f"📌 {img_file.name}", use_container_width=True)

# Submit Button
if st.button("🚀 Analyze Images"):
    if GEMINI_API_KEY and images:
        with st.spinner("⏳ Processing..."):
            try:
                responses = api_response(GEMINI_API_KEY, prompt, images)
                st.success("✅ Analysis Complete!")
                
                # Display results for each image
                for img_file, response in zip(image_files, responses):
                    st.subheader(f"🔎 AI Response for {img_file.name}:")
                    st.write(response)
                    
            except Exception as error:
                st.error(f"❌ Something went wrong: {error}")
    else:
        st.warning("⚠️ Please upload at least one image and enter a prompt.")

# Managing Session states to clear and refresh once the content has been generated
if "prompt" not in st.session_state:
    st.session_state.prompt = ""
if "image_files" not in st.session_state:
    st.session_state.image_files = None

if st.button("🔄 Clear Chat & Restart"):
    st.session_state.clear()
    st.rerun()

