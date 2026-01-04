import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="ReplyAI (Free)")
st.title("📧 ReplyAI - Free AI Customer Support Email Generator")
st.write("Generate professional customer support replies in seconds — no API keys required!")

# ------------------------------
# Free usage limit
# ------------------------------
if "used_count" not in st.session_state:
    st.session_state.used_count = 0

MAX_FREE_REPLIES = 5

if st.session_state.used_count >= MAX_FREE_REPLIES:
    st.error("Free limit reached. Refresh or upgrade to continue.")
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
    # Use larger Flan-T5 model for better responses
    return pipeline("text2text-generation", model="google/flan-t5-large")

generator = load_model()

# ------------------------------
# Generate AI reply
# ------------------------------
if st.button("Generate Reply"):
    if not email_text.strip():
        st.warning("Please paste an email to generate a reply.")
    else:
        # Robust prompt for professional, friendly replies
        prompt = f"""
You are an AI customer support assistant for {company}. 
Write a complete email reply to the customer below.

Rules:
- Tone: {tone} (Friendly / Professional / Polite)
- Keep it under 120 words
- Do not repeat the customer's email
- Begin with a greeting (e.g., "Hello," "Hi," etc.)
- End with a friendly closing (e.g., "Best regards," "Thank you," etc.)
- Keep it concise and professional

Customer email:
{email_text}
"""

        try:
            # Generate reply
            reply = generator(
                prompt,
                max_length=200,
                do_sample=True,
                temperature=0.7
            )
            reply_text = reply[0]["generated_text"]

            # Remove accidental repetition
            if email_text in reply_text:
                reply_text = reply_text.replace(email_text, "").strip()

            # Update usage count
            st.session_state.used_count += 1

            st.subheader("Generated Reply")
            st.text_area("Reply", reply_text, height=200)

        except Exception as e:
            st.error(f"Error generating reply: {e}")
