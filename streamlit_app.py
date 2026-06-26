import streamlit as st
import urllib.request
import json

st.set_page_config(page_title="منصتي المالية الذكية", layout="wide")
st.title("📊 منصة التحليل المالي والمضاربة اللحظية الذكية")
st.write("مرحباً بك! البيانات تُسحب حية وتاريخية مع حساب نقاط المضاربة الفورية، ومدعومة بالذكاء الاصطناعي.")

# -------------------------------------------------------------
# 🛠️ ضَعْ الرمز الذي نسخته بين القوسين بالأسفل بدلاً من العبارة المكتوبة
# -------------------------------------------------------------
api_key = "import os
from google import genai

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
)

tools = [
    {
        'type': 'google_search',
    },
]

generation_config = {
    'temperature': 1,
    'max_output_tokens': 65536,
    'top_p': 0.95,
    'thinking_level': 'high',
}

interaction = client.interactions.create(
    model='models/gemini-3-flash-preview',
    input='',
    tools=tools,
    generation_config=generation_config,
)

print(interaction.steps[-1])


"

# 1. مربع البحث المالي التقليدي للأسهم
ticker = st.text_input("🔍 اكتب رمز السهم هنا لمشاهدة سعره اللحظي (مثال: 2222.SR أو AAPL):", "AAPL").upper()

if ticker:
    st.subheader(f"📈 السعر الحي لسهم: {ticker}")
    try:
        url = f"https://yahoo.com{ticker}?range=5d&interval=15m"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
        meta = data['chart']['result'][0]['meta']
        current_price = meta['regularMarketPrice']
        
        # حساب الدعم والمقاومة السريعة للمضاربة بناءً على السعر الحالي
        support_1 = current_price * 0.98
        resistance_1 = current_price * 1.02
        stop_loss = support_1 * 0.99
        
        unit = " ر.س" if "SR" in ticker else " USD"
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label="💰 السعر اللحظي الحالي", value=f"{current_price:.2f}{unit}")
        col2.metric(label="🟢 منطقة الدخول (شراء)", value=f"{support_1:.2f}{unit}")
        col3.metric(label="🔴 منطقة الخروج (الهدف)", value=f"{resistance_1:.2f}{unit}")
        col4.metric(label="⚠️ وقف الخسارة الصارم", value=f"{stop_loss:.2f}{unit}")
    except Exception as e:
        st.warning("السوق مغلق حالياً أو الرمز يحتاج لتعديل.")

st.write("---")

# 2. ميزة خانة البحث والذكاء الاصطناعي (التي طلبتها في فكرتك الأساسية)
st.subheader("🤖 اسأل الذكاء الاصطناعي المالي عن أي سهم")
user_question = st.text_input("💡 اكتب سؤالك هنا وسينعكس الجواب على الداش بورد (مثال: ما هو أفضل سهم للمضاربة اللحظية وكيف أختار مناطق الدخول؟):")

if user_question and api_key != "الزق_الرمز_الذي_نسخته_هنا":
    with st.spinner("جاري تحليل سؤالك ماليّاً ومحاكاة البيانات..."):
        try:
            # استخدام الموديل المستقر المحدث لربط الاستعلام السريع
            ai_url = f"https://googleapis.com{api_key}"
            
            # صياغة الطلب البرمجي وإجبار الذكاء الاصطناعي على التجاوب كمستشار أسهم
            payload = json.dumps({
                "contents": [{
                    "parts": [{
                        "text": f"أنت مستشار مالي محترف وخبير في الأسهم والمضاربة اللحظية. أجب على هذا السؤال بدقة وإيجاز وبلهجة مبسطة ومفهومة تناسب المتداولين باللغة العربية: {user_question}"
                    }]
                }]
            })
            
            req_ai = urllib.request.Request(ai_url, data=payload.encode('utf-8'), headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req_ai) as resp_ai:
                ai_data = json.loads(resp_ai.read().decode())
                answer = ai_data['candidates'][0]['content']['parts'][0]['text']
                st.markdown(f"### 📝 الإجابة المعتمدة على الداش بورد:\n{answer}")
        except Exception as e:
            st.error(f"تأكد من لصق مفتاح الـ API بشكل صحيح.")
