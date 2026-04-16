import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from gtts import gTTS
import uuid

# ---------------- UI ----------------
st.set_page_config(page_title="Medical AI Assistant", layout="centered")

st.title("🩺 Medical AI Assistant Pro")
st.warning("⚠️ هذا النظام يقدم معلومات عامة فقط وليس بديلاً عن الطبيب")

# ---------------- MODEL ----------------
@st.cache_resource
def load_model():
    model_name = "google/flan-t5-base"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    return tokenizer, model

tokenizer, model = load_model()

# ---------------- INPUT ----------------
symptoms = st.text_area("🧾 اكتب الأعراض هنا:")

# ---------------- FUNCTION ----------------
def analyze(symptoms):
    prompt = f"""
أنت مساعد طبي ذكي.

حلل الأعراض التالية وقدم:
1- نوع الحالة (تنفسية / هضمية / عصبية / جلدية / أخرى)
2- أسباب محتملة
3- مستوى الخطورة (خفيف / متوسط / طارئ)
4- نصيحة عامة

الأعراض: {symptoms}

اكتب الإجابة باللغة العربية الفصحى فقط.
"""

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)

    outputs = model.generate(
        **inputs,
        max_new_tokens=180,
        do_sample=False,
        num_beams=4
    )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return result

# ---------------- RUN ----------------
if result and result.strip():

    tts = gTTS(text=result, lang="ar")
    audio_file = f"voice_{uuid.uuid4().hex}.mp3"
    tts.save(audio_file)

    st.audio(audio_file)

else:
    st.warning("لا يوجد نص لتحويله إلى صوت")
        st.subheader("📋 النتيجة")
        st.write(result)

        # 🔊 صوت
        tts = gTTS(text=result, lang="ar")
        audio_file = f"voice_{uuid.uuid4().hex}.mp3"
        tts.save(audio_file)

        st.audio(audio_file)
