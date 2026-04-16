import streamlit as st
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Medical AI", page_icon="🩺")

st.title("🩺 مساعدك الطبي الذكي")
st.markdown("---")

# --- تحميل الموديل والـ Tokenizer بشكل منفصل أضمن ---
@st.cache_resource
def load_model_components():
    # موديل LaMini ده صغير جداً وسريع جداً وأذكى من T5 العادي في الردود
    model_id = "MBZUAI/LaMini-Flan-T5-77M" 
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
    return tokenizer, model

try:
    tokenizer, model = load_model_components()
except Exception as e:
    st.error("خطأ في تحميل الملفات الأساسية. جرب عمل Refresh.")

symptoms = st.text_area("🧾 صف الأعراض هنا:", 
                        placeholder="مثال: عندي كحة جافة وارتفاع في الحرارة...",
                        height=100)

if st.button("🔍 ابدأ التحليل الآن"):
    if symptoms.strip():
        with st.spinner('جاري تحليل الأعراض طبيباً...'):
            # البرومبت هنا هو السر: بنجبره يحلل ويطلع خطوات
            input_text = f"As a medical assistant, analyze these symptoms: {symptoms}. Categorize them and give advice in Arabic."
            
            inputs = tokenizer(input_text, return_tensors="pt")
            
            with torch.no_grad():
                outputs = model.generate(
                    **inputs, 
                    max_new_tokens=256, 
                    do_sample=True, 
                    temperature=0.7,
                    top_p=0.9
                )
            
            result = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            st.success("✅ تم التحليل")
            st.subheader("📋 النتيجة:")
            st.info(result) 
            
            st.warning("⚠️ هذا التحليل استرشادي فقط، توجه لأقرب طبيب فوراً إذا كانت الحالة طارئة.")
    else:
        st.warning("من فضلك اكتب الأعراض.")
