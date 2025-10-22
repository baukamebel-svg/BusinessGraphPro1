
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="BusinessGraph Pro", page_icon="💼", layout="wide")

# ----------- i18n -----------
LANGS = {
    "kk": {
        "title": "💼 BusinessGraph Pro",
        "subtitle": "Кәсіпкерлерге арналған пайда–шығын анализаторы (функция графиктері)",
        "language": "Тіл",
        "inputs": "📋 Деректер",
        "price": "Өнім бағасы (теңге)",
        "cost": "Өзіндік құн (теңге)",
        "fixed": "Тұрақты шығын (теңге)",
        "qtymax": "Максималды өнім саны",
        "calc": "📊 Есептеу және график салу",
        "results": "Нәтиже",
        "breakeven": "✅ Зиянсыздық нүктесі: шамамен {x0:.2f} дана өнім",
        "nobreakeven": "⚠️ Өнім бағасы өзіндік құннан төмен. Пайда болмайды.",
        "chart_title": "Функция графигін кәсіпорын экономикасында қолдану",
        "x": "Өнім саны (x)",
        "y": "Теңге",
        "revenue": "Түсім (T(x))",
        "costs": "Шығын (S(x))",
        "profit": "Пайда (P(x))",
        "download_img": "Графикті жүктеу (PNG)",
        "download_csv": "Деректерді жүктеу (CSV)",
        "ai_header": "🤖 ЖИ талдауы",
        "ai_tip": "💡 Кеңес: {tip}",
        "footer": "© 2025 Ералиева-Абильдаева",
        "about": "Бағдарлама: баға, өзіндік құн, тұрақты шығын арқылы түсім, шығын, пайда функцияларын есептейді, график салады және зиянсыздық нүктесін көрсетеді."
    },
    "ru": {
        "title": "💼 BusinessGraph Pro",
        "subtitle": "Анализатор прибыли и издержек для предпринимателей (графики функций)",
        "language": "Язык",
        "inputs": "📋 Данные",
        "price": "Цена продукта (тенге)",
        "cost": "Себестоимость (тенге)",
        "fixed": "Постоянные расходы (тенге)",
        "qtymax": "Максимальное количество продукции",
        "calc": "📊 Рассчитать и построить график",
        "results": "Результаты",
        "breakeven": "✅ Точка безубыточности: около {x0:.2f} единиц продукции",
        "nobreakeven": "⚠️ Цена ниже себестоимости. Прибыли не будет.",
        "chart_title": "Применение графика функции в экономике предприятия",
        "x": "Количество продукции (x)",
        "y": "Тенге",
        "revenue": "Выручка (T(x))",
        "costs": "Издержки (S(x))",
        "profit": "Прибыль (P(x))",
        "download_img": "Скачать график (PNG)",
        "download_csv": "Скачать данные (CSV)",
        "ai_header": "🤖 AI-анализ",
        "ai_tip": "💡 Совет: {tip}",
        "footer": "© 2025 Ералиева-Абильдаева",
        "about": "Приложение рассчитывает функции выручки, издержек и прибыли по цене, себестоимости и постоянным расходам, строит график и показывает точку безубыточности."
    }
}

# Language selector
lang = st.sidebar.selectbox("Language · Тіл", options=["kk", "ru"], format_func=lambda x: "Қазақша" if x=="kk" else "Русский")
T = LANGS[lang]

col_header1, col_header2 = st.columns([1,3])
with col_header1:
    st.image("banner.png", use_column_width=True)
with col_header2:
    st.markdown(f"## {T['title']}")
    st.markdown(f"**{T['subtitle']}**")
    st.caption(T["about"])

st.markdown("---")

# Inputs
left, right = st.columns([1,2])
with left:
    st.subheader(T["inputs"])
    price = st.number_input(T["price"], min_value=0.0, value=2000.0, step=100.0)
    cost = st.number_input(T["cost"], min_value=0.0, value=1200.0, step=100.0)
    fixed = st.number_input(T["fixed"], min_value=0.0, value=400000.0, step=10000.0)
    qty_max = st.slider(T["qtymax"], min_value=100, max_value=10000, value=1000, step=100)
    go = st.button(T["calc"], use_container_width=True)

with right:
    st.subheader(T["results"])
    if 'dataframe' not in st.session_state:
        st.session_state['dataframe'] = None

    if go:
        x = np.linspace(0, qty_max, 400)
        revenue = price * x
        costs = cost * x + fixed
        profit = revenue - costs

        # Save dataframe
        df = pd.DataFrame({"x": x, "revenue": revenue, "costs": costs, "profit": profit})
        st.session_state['dataframe'] = df

        # Plot
        fig, ax = plt.subplots(figsize=(8,5))
        ax.plot(x, revenue, label=T["revenue"])
        ax.plot(x, costs, label=T["costs"])
        ax.plot(x, profit, label=T["profit"])
        ax.axhline(0, linewidth=0.8)
        ax.set_xlabel(T["x"])
        ax.set_ylabel(T["y"])
        ax.set_title(T["chart_title"])
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.legend()
        st.pyplot(fig, use_container_width=True)

        # Breakeven and messages
        if price > cost:
            x0 = fixed / (price - cost)
            st.success(T["breakeven"].format(x0=x0))
        else:
            st.error(T["nobreakeven"])

        # Download buttons
        img_buf = BytesIO()
        fig.savefig(img_buf, format="png", dpi=200, bbox_inches="tight")
        img_buf.seek(0)
        st.download_button(T["download_img"], data=img_buf, file_name=f"businessgraph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png", mime="image/png")

        if st.session_state['dataframe'] is not None:
            csv = st.session_state['dataframe'].to_csv(index=False).encode('utf-8')
            st.download_button(T["download_csv"], data=csv, file_name="businessgraph_data.csv", mime="text/csv")

        # Simple rule-based AI-style insights (local, no external API)
        st.markdown(f"### {T['ai_header']}")
        tips_kk = [
            "Бағаны 5–10% көтеру зиянсыздық нүктесін жақындатады, бірақ сұраныстың өзгерісін ескеріңіз.",
            "Егер өзіндік құнды 5% азайтсаңыз, табыстылық айтарлықтай өседі.",
            "Тұрақты шығын көп болса, сату көлемін көбейту қажет — жарнама немесе акция ойластырыңыз.",
        ]
        tips_ru = [
            "Повышение цены на 5–10% приблизит точку безубыточности, но учитывайте спрос.",
            "Если снизить себестоимость на 5%, рентабельность заметно вырастет.",
            "При высоких постоянных расходах увеличьте объем продаж — подумайте о рекламе или акциях.",
        ]
        # Heuristic choose tip
        margin = price - cost
        if margin <= 0:
            tip = tips_kk[1] if lang=="kk" else tips_ru[1]
        elif margin / price < 0.15:
            tip = tips_kk[0] if lang=="kk" else tips_ru[0]
        else:
            tip = tips_kk[2] if lang=="kk" else tips_ru[2]
        st.info((T["ai_tip"]).format(tip=tip))

st.markdown("---")
st.caption(T["footer"])
