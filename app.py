import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Medical AI Assistant", page_icon="🩺")

# --- تحميل الموديل (مع التخزين المؤقت) ---
@st.cache_resource
def load_model():
    # موديل Flan-T5 كويس بس محتاج برومبت دقيق
    model_name = "google/flan-t5-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()

# --- واجهة المستخدم ---
st.title("🩺 مساعدك الطبي الذكي")
st.markdown("---")
st.info("قم بوصف الأعراض التي تشعر بها بدقة للحصول على تحليل أولي.")

symptoms = st.text_area("🧾 صف الأعراض هنا (بالعربي أو الإنجليزي):", 
                        placeholder="مثال: صداع مستمر مع ارتفاع في درجة الحرارة...",
                        height=150)

# --- دالة التحليل ---
def analyze_symptoms(text):
    # تحسين البرومبت ليفهمه الموديل بوضوح
    prompt = f"Medical Assistant Task: Analyze symptoms '{text}'. Provide: 1- Category, 2- Possible causes, 3- Urgency (Low/Medium/High), 4- General Advice. Answer in Arabic."
    
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs, 
            max_new_tokens=256,
            num_beams=5,
            early_stopping=True
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# --- زر التشغيل ---
if st.button("🔍 ابدأ التحليل الآن"):
    if symptoms.strip():
        with st.spinner('جاري تحليل البيانات...'):
            try:
                result = analyze_symptoms(symptoms)
                st.success("✅ تم التحليل بنجاح")
                st.subheader("📋 التقرير المتوقع:")
                st.write(result)
                
                st.warning("⚠️ تنبيه: هذا التحليل استرشادي فقط ولا يعوض عن زيارة الطبيب المختص.")
            except Exception as e:
                st.error(f"حدث خطأ أثناء المعالجة: {e}")
    else:
        st.warning("الرجاء إدخال الأعراض أولاً.")
