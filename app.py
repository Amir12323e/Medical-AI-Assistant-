import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# ---------------- UI ----------------
st.set_page_config(page_title="Medical AI Assistant", layout="centered")

st.title("🩺 Medical AI Assistant")
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
symptoms = st.text_area("🧾 اكتب الأعراض:", placeholder="مثال: صداع، حرارة، كحة")

# ---------------- ANALYSIS ----------------
def analyze(symptoms):
    prompt = f"""
أنت مساعد طبي ذكي.

حلل الأعراض التالية وقدم:
1- نوع الحالة (تنفسية / هضمية / عصبية / جلدية / أخرى)
2- أسباب محتملة
3- مستوى الخطورة (خفيف / متوسط / طارئ)
4- نصيحة عامة

الأعراض: {symptoms}

اكتب الإجابة باللغة العربية الفصحى بشكل واضح ومنظم.
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
if st.button("🔍 تحليل الأعراض"):

    if not symptoms.strip():
        st.warning("من فضلك اكتب الأعراض أولاً")
    else:
        result = analyze(symptoms)

        st.subheader("📋 النتيجة")
        st.write(result)
