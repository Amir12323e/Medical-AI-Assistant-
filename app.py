import streamlit as st

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Medical AI Assistant", page_icon="🩺")

# تنسيق CSS بسيط لتحسين شكل الكلام
st.markdown("""
    <style>
    .report-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-right: 5px solid #ff4b4b;
        color: #31333F;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🩺 مساعدك الطبي الذكي")
st.markdown("---")

symptoms = st.text_area("🧾 صف الأعراض هنا (مثال: صداع، كحة، ألم بطن):", 
                        placeholder="اكتب أعراضك هنا...",
                        height=100)

# --- محرك التحليل (Logic Engine) ---
def analyze_symptoms_fast(text):
    text = text.lower()
    analysis = {
        "الحالة": "غير محددة بدقة، يرجى استشارة طبيب",
        "الأسباب المحتملة": "تحتاج لفحص سريري",
        "الخطورة": "متوسطة - يرجى المتابعة",
        "النصيحة": "شرب السوائل والراحة حتى زيارة الطبيب"
    }

    # تحليل بسيط بناءً على الكلمات المفتاحية
    if "صداع" in text or "رأس" in text:
        analysis.update({
            "الحالة": "أعراض عصبية / إجهاد",
            "الأسباب المحتملة": "إجهاد، قلة نوم، أو ضغط دم",
            "الخطورة": "خفيفة إلى متوسطة",
            "النصيحة": "الراحة في مكان مظلم وقياس ضغط الدم"
        })
    elif "كحة" in text or "سعال" in text or "صدر" in text:
        analysis.update({
            "الحالة": "أعراض تنفسية",
            "الأسباب المحتملة": "برد، حساسية، أو التهاب شعبي",
            "الخطورة": "متوسطة",
            "النصيحة": "شرب سوائل دافئة وعمل جلسة بخار"
        })
    elif "بطن" in text or "مغص" in text or "إسهال" in text:
        analysis.update({
            "الحالة": "أعراض هضمية",
            "الأسباب المحتملة": "نزلة معوية أو عسر هضم",
            "الخطورة": "متوسطة",
            "النصيحة": "تجنب الأكل الدسم والتركيز على المسلوق"
        })
    elif "حرارة" in text or "سخونية" in text:
        analysis.update({
            "الأسباب المحتملة": "عدوى بكتيرية أو فيروسية",
            "الخطورة": "تستدعي المتابعة",
            "النصيحة": "استخدام كمادات مياه فاتر وعمل فحص صورة دم"
        })

    return analysis

# --- زر التشغيل ---
if st.button("🔍 ابدأ التحليل الآن"):
    if symptoms.strip():
        with st.spinner('جاري معالجة البيانات...'):
            result = analyze_symptoms_fast(symptoms)
            
            st.success("✅ تم استخراج التقرير")
            
            # عرض النتيجة بشكل شيك
            st.markdown(f"""
            <div class="report-box">
                <h3>📋 التقرير المتوقع:</h3>
                <p><b>• نوع الحالة:</b> {result['الحالة']}</p>
                <p><b>• الأسباب المحتملة:</b> {result['الأسباب المحتملة']}</p>
                <p><b>• مستوى الخطورة:</b> {result['الخطورة']}</p>
                <p><b>• النصيحة:</b> {result['النصيحة']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.warning("⚠️ تنبيه: هذا التحليل برمجي فقط بناءً على كلماتك، ولا يغني أبداً عن زيارة الطبيب.")
    else:
        st.warning("الرجاء كتابة الأعراض أولاً.")
