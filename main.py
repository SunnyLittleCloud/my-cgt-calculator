import streamlit as st
from datetime import date

# 1. 页面配置
st.set_page_config(page_title="CGT Calculator", page_icon="🧮")

# --- 2. 自定义 CSS 样式 (背景色和蓝色云朵) ---
st.markdown("""
    <style>
    /* 全局背景颜色：低饱和淡黄色 */
    .stApp {
        background-color: #fef9e7;
    }

    /* 云朵容器 */
    .cloud-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 60px 0 40px 0;
    }

    /* 云朵形状：填充淡蓝色 #BAE1FF */
    .cloud {
        position: relative;
        width: 450px;
        height: 140px;
        background: #BAE1FF; 
        border-radius: 100px;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        text-align: center;
        border: 2px solid #91C9F2; /* 浅蓝色边框增强立体感 */
    }

    /* 云朵上的小圆弧 */
    .cloud:after, .cloud:before {
        content: '';
        position: absolute;
        background: #BAE1FF;
        z-index: 0;
    }

    .cloud:after {
        width: 150px;
        height: 150px;
        top: -70px;
        left: 60px;
        border-radius: 50%;
        border-top: 2px solid #91C9F2;
    }

    .cloud:before {
        width: 200px;
        height: 200px;
        top: -100px;
        right: 60px;
        border-radius: 50%;
        border-top: 2px solid #91C9F2;
    }

    /* 标题文字样式：深蓝色 #1E3A5F */
    .cloud-title {
        color: #1E3A5F;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 26px;
        font-weight: 700;
        z-index: 10;
        padding: 0 30px;
        line-height: 1.2;
    }

    /* 调整下方的副标题文字 */
    .stCaption {
        color: #5D6D7E !important;
        text-align: center !important;
        display: block;
    }
    </style>
    
    <div class="cloud-container">
        <div class="cloud">
            <div class="cloud-title">Australian Capital Gain Tax Calculator</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.caption("Automatically calculates the 50% CGT Discount for assets held over 12 months.")
st.write("---")

# --- 3. 输入部分 (INPUT SECTION) ---
col1, col2 = st.columns(2) 

with col1:
    buy_price = st.number_input("Buy Price ($)", min_value=0.0, step=100.0, value=1000.0)
    buy_date = st.date_input("Buy Date", value=date(2023, 1, 1))

with col2:
    sell_price = st.number_input("Sell Price ($)", min_value=0.0, step=100.0, value=2500.0)
    sell_date = st.date_input("Sell Date", value=date.today())

# --- 4. 逻辑处理部分 (LOGIC SECTION) ---
if st.button("Calculate Tax", type="primary"):
    
    # 基础计算
    gross_profit = sell_price - buy_price
    held_days = (sell_date - buy_date).days

    # 错误检查
    if held_days < 0:
        st.error("⚠️ Error: Sell date cannot be earlier than Buy date.")
    
    else:
        # 有效交易展示
        st.write(f"📅 Asset held for **{held_days}** days")
        st.divider()

        if gross_profit > 0:
            # 盈利场景
            if held_days > 365:
                taxable_income = gross_profit * 0.5
                discount_msg = "<span style='color:green; font-weight:bold;'>✅ Eligible for 50% Discount (>12M)</span>"
                st.balloons()
            else:
                taxable_income = gross_profit
                discount_msg = "<span style='color:red; font-weight:bold;'>❌ No Discount (<12M)</span>"

            # 结果展示列
            c1, c2, c3 = st.columns(3)
            
            c1.metric("Gross Profit", f"${gross_profit:,.2f}")
            
            with c2:
                st.write("Discount Status")
                st.markdown(discount_msg, unsafe_allow_html=True)
            
            c3.metric("Taxable Income", f"${taxable_income:,.2f}")
            
            st.info(f"💡 This **${taxable_income:,.2f}** will be added to your assessable income for the financial year.")

        elif gross_profit < 0:
            # 亏损场景
            st.error(f"💸 Capital Loss: **${abs(gross_profit):,.2f}**")
            st.write("This loss can be carried forward to offset future capital gains.")
            
        else:
            # 盈亏平衡
            st.warning("Break even. No gain, no loss.")

# --- 5. 免责声明 ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.caption("Disclaimer: This tool is for educational purposes only. Please consult a registered tax agent for official advice.")