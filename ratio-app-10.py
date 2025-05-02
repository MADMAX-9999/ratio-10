import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def simulate_gsr_strategy(start_gold, start_silver, gsr_threshold_high, gsr_threshold_low, gsr_sequence, trade_percent):
    gold = start_gold
    silver = start_silver
    transactions = []
    portfolio_values = []

    for gsr in gsr_sequence:
        portfolio_values.append({
            'GSR': gsr,
            'Gold (oz)': gold,
            'Silver (oz)': silver,
            'Total Metal Units': gold + silver
        })

        if gsr >= gsr_threshold_high:
            traded_gold = gold * trade_percent / 100
            gold -= traded_gold
            bought_silver = traded_gold * gsr
            silver += bought_silver
            transactions.append(f"Wysokie GSR {gsr}: Zamiana {traded_gold:.2f} oz złota na {bought_silver:.2f} oz srebra.")

        elif gsr <= gsr_threshold_low:
            traded_silver = silver * trade_percent / 100
            silver -= traded_silver
            bought_gold = traded_silver / gsr
            gold += bought_gold
            transactions.append(f"Niskie GSR {gsr}: Zamiana {traded_silver:.2f} oz srebra na {bought_gold:.2f} oz złota.")

    return gold, silver, transactions, pd.DataFrame(portfolio_values)

st.title("Zaawansowany Symulator Strategii Gold Silver Ratio (GSR)")

st.sidebar.header("Ustawienia początkowe")
start_gold = st.sidebar.number_input("Początkowa ilość złota (oz)", min_value=0.0, value=10.0, step=0.1)
start_silver = st.sidebar.number_input("Początkowa ilość srebra (oz)", min_value=0.0, value=800.0, step=1.0)
gsr_threshold_high = st.sidebar.number_input("Próg wysokiego GSR (zamiana złota na srebro)", min_value=50, max_value=150, value=90)
gsr_threshold_low = st.sidebar.number_input("Próg niskiego GSR (zamiana srebra na złoto)", min_value=10, max_value=100, value=50)
trade_percent = st.sidebar.slider("Procent aktywa do zamiany przy sygnale (%)", min_value=5, max_value=50, value=10)

st.sidebar.header("Import lub podaj sekwencję GSR")
upload_file = st.sidebar.file_uploader("Wgraj plik CSV z wartościami GSR", type=["csv"])

if upload_file:
    df_gsr = pd.read_csv(upload_file)
    gsr_sequence = df_gsr.iloc[:, 0].tolist()
else:
    gsr_sequence_input = st.sidebar.text_area("Podaj sekwencję GSR (oddzielone przecinkami)", "80,85,90,95,100,90,80,70,60,50,45,55")
    gsr_sequence = [float(g.strip()) for g in gsr_sequence_input.split(",")]

if st.button("Rozpocznij symulację"):
    final_gold, final_silver, transactions, portfolio_df = simulate_gsr_strategy(
        start_gold, start_silver, gsr_threshold_high, gsr_threshold_low, gsr_sequence, trade_percent
    )

    st.subheader("Wynik końcowy")
    st.write(f"Finalna ilość złota: **{final_gold:.2f} oz**")
    st.write(f"Finalna ilość srebra: **{final_silver:.2f} oz**")
    st.write(f"Łączna liczba jednostek metali: **{(final_gold + final_silver):.2f}**")

    st.subheader("Historia transakcji")
    for t in transactions:
        st.write("-", t)

    st.subheader("Wizualizacja portfela")
    fig, ax = plt.subplots()
    portfolio_df['Total Metal Units'].plot(ax=ax)
    ax.set_xlabel('Krok symulacji')
    ax.set_ylabel('Łączna ilość jednostek metali')
    ax.set_title('Zmiana wielkości portfela w czasie')
    st.pyplot(fig)

    st.subheader("Szacunkowa wycena końcowa")
    est_gold_price = st.number_input("Podaj szacunkową cenę złota (USD/oz)", min_value=0.0, value=2000.0, step=10.0)
    est_silver_price = st.number_input("Podaj szacunkową cenę srebra (USD/oz)", min_value=0.0, value=25.0, step=0.5)

    total_value = final_gold * est_gold_price + final_silver * est_silver_price
    st.write(f"Wartość portfela przy założonych cenach: **{total_value:,.2f} USD**")

    st.success("Symulacja zakończona! 🎯")
