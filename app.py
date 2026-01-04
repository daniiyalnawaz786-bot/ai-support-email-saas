import streamlit as st
import OpenAI

st.set_page_config(page_title="AI Support Email Generator")

st.title("📧 AI Customer Support Email Generator")
st.write("Generate professional customer support replies in seconds.")

# Usage limit
if "count" not in st.session_state:
    st.session_state.count = 0

if st.session_state.count >= 5:
    st.error("Free limit reached. Please upgrade to continue.")
    st.stop()

email_text = st.text_area("Paste customer email here")
tone = st.selectbox("Reply tone", ["Professional", "Friendly", "Polite"])
company = st.text_input("Company name")

if st.button("Generate Reply"):
    if email_text.strip() == "":
        st.warning("Please paste an email.")
    else:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        prompt = f"""
You are a customer support assistant.

Rules:
- Be polite and professional
- Do not make refunds or promises
- Keep response under 120 words
- End with a friendly closing
- Mention this is an automated draft

Company: {company}
Tone: {tone}

Customer email:
{email_text}
"""

openai.api_key = st.secrets["OPENAI_API_KEY"]

response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)


        st.session_state.count += 1

        st.subheader("Generated Reply")
        st.text_area("Reply", response.choices[0].message['content'], height=200)

