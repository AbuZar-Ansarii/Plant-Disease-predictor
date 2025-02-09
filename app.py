import streamlit as st
import cv2
import numpy as np
import pickle
from PIL import Image


st.set_page_config(page_title="Plant Disease Predictor", page_icon="🌿", layout="wide")  # Set page title, icon, and layout

# Custom CSS for better appearance
st.markdown(
    """
    <style>
    body {
        font-family: sans-serif;
    }
    .main {
        padding: 2rem;
    }
    .container {
        display: flex;
        flex-direction: column; /* Stack elements vertically */
        align-items: center; /* Center horizontally */
    }
    .image-container {
        margin-bottom: 1rem; /* Space below the image */
        border: 1px dashed #ccc; /* Add a dashed border */
        padding: 10px;
    }
    .prediction-container {
        margin-top: 1rem;
        padding: 20px;
        border: 1px solid #eee;
        border-radius: 5px;
        background-color: #f9f9f9;
    }
    .stButton>button {
        background-color: #4CAF50; /* Green */
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit App Title with Markdown for styling
st.markdown("<h1 style='text-align: center;'>🌿 Plant Disease Predictor</h1>", unsafe_allow_html=True)

# --- Model and Class Names Loading (Improved Error Handling) ---
model = None
class_names = None

try:
    with open("plant_model.pkl", "rb") as f:
        model = pickle.load(f)
    st.success("Model loaded successfully!")
except FileNotFoundError:
    st.error("Model file not found. Please ensure 'plant_model.pkl' is in the correct directory.")
except (EOFError, pickle.UnpicklingError):
    st.error("Model file is corrupted or incomplete. Please retrain your model and save it again.")
except Exception as e:
    st.error(f"An unexpected error occurred during model loading: {e}")
    st.exception(e)

try:
    with open("class_names.pkl", "rb") as f:
        class_names = pickle.load(f)
    # st.success("Class names loaded successfully!")
except FileNotFoundError:
    st.error("Class names file not found. Please ensure 'class_names.pkl' is in the correct directory.")
except (EOFError, pickle.UnpicklingError):
    st.error("Class names file is corrupted or incomplete. Please regenerate the class names file.")
except Exception as e:
    st.error(f"An unexpected error occurred during class names loading: {e}")
    st.exception(e)

# Function to preprocess an image
def preprocess_image(uploaded_file):
    try:
        image = Image.open(uploaded_file)  # Use PIL to open the image
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) # Convert PIL image to BGR for OpenCV
        img = cv2.resize(img, (256, 256))
        img = img / 255.0
        img = np.expand_dims(img, axis=0)
        return img
    except Exception as e:
        st.error(f"Error during image preprocessing: {e}") # Handle and report errors
        st.exception(e) # Show the full traceback for debugging
        return None  # Return None to indicate failure

# --- File Uploader and Image Display ---
st.markdown("<div class='container'>", unsafe_allow_html=True)  # Start of container for centering
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], accept_multiple_files=False)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.markdown("<div class='image-container'>", unsafe_allow_html=True)  # Start of image container
    st.image(image, caption="Uploaded Image", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)  # End of image container
    # button
    if st.button("Predict Disease"):
        if model is None:
            st.error("Model is not loaded. Please check the model file.")
        elif class_names is None:
            st.error("Class names are not loaded. Please check the class names file.")
        else:
            processed_image = preprocess_image(uploaded_file)  # Process image
            if processed_image is not None:
                prediction = model.predict(processed_image)  # Predict
                # Get predicted class and confidence score
                predicted_class_index = np.argmax(prediction)
                predicted_class = class_names[predicted_class_index]
                confidence_score = np.max(prediction)
                # Display Result
                st.header(f"🌱 Predicted Disease: {predicted_class}")
                st.subheader(f"Confidence: {confidence_score:.2%}")

        st.markdown("< /div>", unsafe_allow_html=True)  # End of container
