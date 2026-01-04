import streamlit as st
import openai

st.set_page_config(page_title="ReplyAI")

st.title("📧 ReplyAI - AI Customer Support Email Generator")
st.write("Generate professional customer support replies in seconds.")

# ------------------------------
# Free usage limit
# ------------------------------
if "used_count" not in st.session_state:
    st.session_state.used_count = 0

MAX_FREE_REPLIES = 5

if st.session_state.used_count >= MAX_FREE_REPLIES:
    st.error("Free limit reached. Please upgrade to continue.")
    st.stop()

# ------------------------------
# Inputs
# ------------------------------
email_text = st.text_area("Paste customer email here", height=150)
tone = st.selectbox("Reply tone", ["Professional", "Friendly", "Polite"])
company = st.text_input("Company name")

# ------------------------------
# API key from Streamlit secrets
# ------------------------------
openai.api_key = st.secrets.get("OPENAI_API_KEY", "")

# ------------------------------
# Generate AI reply
# ------------------------------
if st.button("Generate Reply"):
    if not email_text.strip():
        st.warning("Please paste an email to generate a reply.")
    elif not openai.api_key:
        st.error("OpenAI API key not found! Add it in Streamlit Secrets.")
    else:
        prompt = f"""
You are a professional customer support assistant.

Rules:
- Be polite and professional
- Do not make refunds or promises
- Keep the response under 120 words
- End with a friendly closing
- Mention this is an automated draft

Company: {company}
Tone: {tone}

Customer email:
{email_text}
"""

        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
            reply_text = response.choices[0].message.content

            st.session_state.used_count += 1

            st.subheader("Generated Reply")
            st.text_area("Reply", reply_text, height=200)

        except Exception as e:
            st.error(f"Error generating reply: {e}")
