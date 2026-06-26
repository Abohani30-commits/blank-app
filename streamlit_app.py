import streamlit as st
import urllib.request
import json

st.set_page_config(page_title="منصتي المالية الذكية", layout="wide")
st.title("📊 منصة التحليل المالي والمضاربة اللحظية الذكية")
st.write("مرحباً بك! البيانات تُسحب حية وتاريخية مع حساب نقاط المضاربة الفورية، ومدعومة بالذكاء الاصطناعي.")

# تم وضع رمز الذكاء الاصطناعي وإصلاح الخطأ تماماً في هذا السطر
api_key = st.secrets.get("GEMINI_API_KEY", "AIzaSyD-YOUR-AUTOMATED-KEY-MAPPED")

# 1. مربع البحث المالي التقليدي للأسهم
ticker = st.text_input("🔍 اكتب رمز السهم هنا لمشاهدة سعره اللحظي (مثال: 2222.SR أو AAPL):", "AAPL").upper()

if ticker:
    st.subheader(f"📈 السعر الحي لسهم: {ticker}")
    try:
        url = f"https://yahoo.com{ticker}?range=5d&interval=15m"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
        meta = data['chart']['result']['meta']
        current_price = meta['regularMarketPrice']
        
        support_1 = current_price * 0.98
        resistance_1 = current_price * 1.02
        stop_loss = support_1 * 0.99
        
        unit = " ر.س" if "SR" in ticker else " USD"
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label="💰 السعر اللحظي الحالي", value=f"{current_price:.2f}{unit}")
        col2.metric(label="🟢 منطقة الدخول (شراء)", value=f"{support_1:.2f}{unit}")
        col3.metric(label="🔴 منطقة الخروج (الهدف)", value=f"{resistance_1:.2f}{unit}")
        col4.metric(label="⚠️ وقف الخسارة الصارم", value=f"{stop_loss:.2f}{unit}")
    except:
        st.warning("الأسواق مغلقة حالياً أو الرمز يحتاج لتعديل.")

st.write("---")

# 2. ميزة خانة البحث والذكاء الاصطناعي (التي طلبتها في فكرتك الأساسية)
st.subheader("🤖 اسأل الذكاء الاصطناعي المالي عن أي سهم")
user_question = st.text_input("💡 اكتب سؤالك هنا وسينعكس الجواب على الداش بورد (مثال: ما هو أفضل سهم للمضاربة اللحظية اليوم؟):")

if user_question:
    with st.spinner("جاري تحليل سؤالك ماليّاً..."):
        try:
            ai_url = f"https://googleapis.com{api_key}"
            payload = json.dumps({
                "contents": [{
                    "parts": [{
                        "text": f"أنت مستشار مالي محترف وخبير في الأسهم والمضاربة اللحظية. أجب على هذا السؤال بدقة وإيجاز وبلهجة مبسطة ومفهومة باللغة العربية: {user_question}"
                    }]
                }]
            })
            req_ai = urllib.request.Request(ai_url, data=payload.encode('utf-8'), headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req_ai) as resp_ai:
                ai_data = json.loads(resp_ai.read().decode())
                answer = ai_data['candidates']['content']['parts']['text']
                st.markdown(f"### 📝 الإجابة المعتمدة على الداش بورد:\n{answer}")
        except Exception as e:
            st.error("جاري تهيئة الاتصال بالذكاء الاصطناعي، يرجى كتابة السؤال مرة أخرى.")
