import streamlit as st
from transformers import pipeline

# --- Page Configuration ---
st.set_page_config(
    page_title="Cute AI Text Detector 💖",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');
    
    .stApp {
        background: linear-gradient(to right, #87CEEB, #B0E0E6);
        font-family: 'Arial', sans-serif;
    }
    .st-emotion-cache-1y4p8pa { /* Main content */
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        transition: 0.3s;
    }
    .st-emotion-cache-1y4p8pa:hover {
        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
    }
    .st-emotion-cache-6q9sum { /* Sidebar */
        background-color: rgba(255, 240, 245, 0.8);
        border-radius: 15px;
    }
    h1, h2, h3 {
        font-family: 'Pacifico', cursive;
        color: #ff69b4; /* Hot Pink */
    }
    .stButton>button {
        background-color: #ffb6c1; /* Light Pink */
        color: white;
        border-radius: 20px;
        border: 2px solid #ff69b4;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff69b4;
        border-color: #ff1493;
        transform: scale(1.05);
    }
    .stTextArea>div>div>textarea {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        border: 2px dashed #ffb6c1;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 80px;'>🤖</h1>", unsafe_allow_html=True)
    st.title("About this App ✨")
    st.info(
        "Hello there! This little app uses a smart AI to guess if text is from a human or another AI. "
        "Just pop your text in the box and see the magic happen! 💖"
    )
    st.markdown("---")
    st.header("Model Info 📜")
    st.markdown(
        """
        - **Model:** `Hello-SimpleAI/chatgpt-detector-roberta`
        - **Type:** A special text-classifying robot! 🤖
        - **Based on:** The super-smart RoBERTa~
        """
    )
    st.markdown("---")
    st.caption("Made with love by Anny 🌸")


# --- Main Content ---
st.title("💖 AI vs Human Writer ✍️")
st.markdown("### Who wrote it? Let this cute AI guess for you!")
st.warning("Just a little heads-up: This AI is smart but not perfect! Use for fun! 💕")


# --- Load Model ---
@st.cache_resource
def load_model():
    model_name = "Hello-SimpleAI/chatgpt-detector-roberta"
    classifier = pipeline("text-classification", model=model_name)
    return classifier

with st.spinner('Waking up the AI... 😴... Almost there!'):
    classifier = load_model()

# --- User Input ---
st.subheader("📝 Paste Your Text Below")
user_text = st.text_area("", height=250, placeholder="Type or paste something here...")

col1, col2, col3 = st.columns([2, 2, 8])

with col1:
    analyze_button = st.button("✨ Analyze!", type="primary", use_container_width=True)

with col2:
    clear_button = st.button("🗑️ Clear", use_container_width=True)

if clear_button:
    user_text = ""

# --- Analysis and Output ---
if analyze_button and user_text.strip():
    with st.spinner("The AI is thinking... 🤔"):
        result = classifier(user_text)
        label = result[0]['label']
        score = result[0]['score']

        st.divider()
        st.subheader("🎉 Here's the result!")
        
        # Celebrate!
        st.balloons()

        if "ChatGPT" in label or "AI" in label:
            st.error("I think a friendly robot wrote this! 🤖")
            st.progress(score, text=f"Confidence: {score:.0%}")
        else:
            st.success("This sounds like a human wrote it! 🧑‍🎨")
            st.progress(score, text=f"Confidence: {score:.0%}")

        with st.expander("Show me the nerdy details! 🤓"):
            st.metric(label="Top Guess", value=label)
            st.metric(label="Confidence Score", value=f"{score:.2%}")
            st.json(result)

elif analyze_button and not user_text.strip():
    st.error("Oopsie! Please write something in the text box first. 😅")

# --- Footer ---
st.markdown("---")
st.caption("Powered by Streamlit & Hugging Face. Designed with a sprinkle of 💖 by Anny.")