import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="ReplyAI (Free)")
st.title("📧 ReplyAI - Free AI Customer Support Email Generator")
st.write("Generate professional customer support replies without any API keys!")

# ------------------------------
# Free usage limit
# ------------------------------
if "used_count" not in st.session_state:
    st.session_state.used_count = 0

MAX_FREE_REPLIES = 5

if st.session_state.used_count >= MAX_FREE_REPLIES:
    st.error("Free limit reached. Upgrade or refresh to continue.")
    st.stop()

# ------------------------------
# Inputs
# ------------------------------
email_text = st.text_area("Paste customer email here", height=150)
tone = st.selectbox("Reply tone", ["Professional", "Friendly", "Polite"])
company = st.text_input("Company name", "")

# ------------------------------
# Initialize Hugging Face generator
# ------------------------------
@st.cache_resource(show_spinner=False)
def load_model():
    return pipeline("text2text-generation", model="google/flan-t5-small")

generator = load_model()

# ------------------------------
# Generate AI reply
# ------------------------------
if st.button("Generate Reply"):
    if not email_text.strip():
        st.warning("Please paste an email to generate a reply.")
    else:
        # Build prompt for the model
        prompt = f"""
You are a professional customer support assistant for {company}.
Tone: {tone}.
Reply professionally and politely to this email:

{email_text}
"""

        try:
            reply = generator(prompt, max_length=150, do_sample=True, temperature=0.7)
            reply_text = reply[0]["generated_text"]

            st.session_state.used_count += 1

            st.subheader("Generated Reply")
            st.text_area("Reply", reply_text, height=200)

        except Exception as e:
            st.error(f"Error generating reply: {e}")
