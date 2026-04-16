import streamlit as st
from transformers import pipeline

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Medical AI Assistant", page_icon="🩺")

st.title("🩺 مساعدك الطبي الذكي")
st.markdown("---")

# --- تحميل الموديل (استخدام Pipeline أضمن وأسرع) ---
@st.cache_resource
def load_analysis_pipeline():
    # استخدمنا موديل أصغر وأسرع ومناسب للمهمات دي
    # الموديل ده "Zero-Shot" بيقدر يحلل النصوص حتى لو مش متدرب عربي
    return pipeline("text2text-generation", model="google/flan-t5-small")

pipe = load_analysis_pipeline()

symptoms = st.text_area("🧾 صف الأعراض هنا:", 
                        placeholder="مثال: صداع شديد وحرارة...",
                        height=100)

if st.button("🔍 ابدأ التحليل الآن"):
    if symptoms.strip():
        with st.spinner('جاري التحليل...'):
            # كتابة البرومبت بالإنجليزي للموديل داخلياً عشان نضمن إنه يخرج داتا
            # لكن هنطلب منه يرد بالعربي
            prompt = f"Analyze these medical symptoms: {symptoms}. Provide possible cause and advice in Arabic language."
            
            try:
                # توليد النتيجة
                raw_result = pipe(prompt, max_length=200, num_beams=5)[0]['generated_text']
                
                st.success("✅ تم التحليل بنجاح")
                st.subheader("📋 التقرير المتوقع:")
                
                # لو الموديل هلفط بالعربي، هنعرض النتيجة ونحط حل بديل
                if len(raw_result) < 3:
                     st.info("الموديل لم يستطع تكوين جملة مفيدة، حاول وصف الأعراض بشكل أدق.")
                else:
                     st.write(raw_result)
                
            except Exception as e:
                st.error("حدث ضغط على السيرفر، يرجى المحاولة مرة أخرى.")
    else:
        st.warning("الرجاء كتابة الأعراض أولاً.")

st.warning("⚠️ تنبيه: هذا التطبيق تعليمي فقط، استشر طبيبك دائماً.")
