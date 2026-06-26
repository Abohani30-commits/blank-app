import streamlit as st
import urllib.request
import json

st.set_page_config(page_title="منصتي المالية الذكية", layout="wide")
st.title("📊 منصة التحليل المالي والمضاربة اللحظية الذكية")
st.write("مرحباً بك في منصتك الخاصة! البيانات تُسحب حية وتاريخية مع حساب نقاط المضاربة.")

ticker = st.text_input("🔍 اكتب رمز السهم هنا (مثال للسوق السعودي: 2222.SR أو أسواق عالمية: AAPL):", "AAPL").upper()

if ticker:
    st.subheader(f"📈 التحليل الحي للمضاربة اللحظية لسهم: {ticker}")
    
    try:
        url = f"https://yahoo.com{ticker}?range=5d&interval=15m"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        result = data['chart']['result']
        meta = result['meta']
        current_price = meta['regularMarketPrice']
        currency = meta['currency']
        
        quotes = result['indicators']['quote']
        highs = [h for h in quotes['high'] if h is not None]
        lows = [l for l in quotes['low'] if l is not None]
        closes = [c for c in quotes['close'] if c is not None]
        
        if highs and lows and closes:
            high = max(highs)
            low = min(lows)
            close = closes[-1]
            
            # معادلات المضاربة اللحظية
            pivot = (high + low + close) / 3
            resistance_1 = (2 * pivot) - low   # منطقة الخروج وجني الربح
            support_1 = (2 * pivot) - high      # منطقة الدخول والشراء السريع
            stop_loss = support_1 * 0.99         # وقف الخسارة
            
            unit = " ر.س" if "SR" in ticker else f" {currency}"
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric(label="💰 السعر اللحظي الحالي", value=f"{current_price:.2f}{unit}")
            col2.metric(label="🟢 منطقة الدخول (شراء)", value=f"{support_1:.2f}{unit}")
            col3.metric(label="🔴 منطقة الخروج (الهدف)", value=f"{resistance_1:.2f}{unit}")
            col4.metric(label="⚠️ وقف الخسارة الصارم", value=f"{stop_loss:.2f}{unit}")
            
            st.success("🎯 نصيحة للمضاربة: يفضل الشراء بالقرب من منطقة الدخول والبيع السريع عند منطقة الخروج مع الالتزام بوقف الخسارة.")
        else:
            st.warning("السوق مغلق حالياً أو لا توجد بيانات كافية لهذا الرمز.")
            
    except Exception as e:
        st.error("تأكد من كتابة رمز السهم بشكل صحيح (مثال: أرامكو 2222.SR أو الراجحي 1120.SR).")
