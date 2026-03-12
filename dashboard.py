import streamlit as st
import joblib
import pandas as pd
import psutil
import time

st.set_page_config(page_title="Sentinel AI - Live Monitoring", layout="wide")

st.title("Detekcja Obciążenia CPU (anomalii) Live")
st.markdown("Model: **Isolation Forest** | Dane: **System Telemetry (CPU & RAM)**")

# Inicjalizacja modelu - jednorazowo
@st.cache_resource
def load_model():
    return joblib.load('trained_isolation_forest.joblib')

try:
    model = load_model()
except FileNotFoundError:
    st.error("Nie znaleziono pliku 'trained_isolation_forest.joblib'. Najpierw zapisz wytrenowany model!")
    st.stop()

if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['timestamp', 'cpu_usage', 'ram_usage', 'score', 'anomaly'])

col1, col2, col3 = st.columns(3)
metric_cpu = col1.empty()
metric_ram = col2.empty()
metric_status = col3.empty()

chart_cpu = st.empty()
chart_score = st.empty()

stop_button = st.button("Zatrzymaj monitoring")

#Pętla Live
while not stop_button:
    # Pobieranie danych (Akwizycja)
    new_data = {
        'timestamp': pd.Timestamp.now(),
        'cpu_usage': psutil.cpu_percent(),
        'ram_usage': psutil.virtual_memory().percent
    }
    
    # Tworzenie DataFrame dla nowego punktu
    new_row = pd.DataFrame([new_data])
    
    # Predykcja na nowym punkcie
    # Używamy tych samych nazw kolumn co przy treningu
    X_live = new_row[['cpu_usage', 'ram_usage']]
    new_row['anomaly'] = model.predict(X_live)
    new_row['score'] = model.decision_function(X_live)

    # Aktualizacja bufora (ostatnie 100 odczytów)
    st.session_state.data = pd.concat([st.session_state.data, new_row]).iloc[-100:]
    df = st.session_state.data

    # Aktualizacja metryk tekstowych
    latest = df.iloc[-1]
    metric_cpu.metric("Obciążenie CPU", f"{latest['cpu_usage']}%")
    metric_ram.metric("Zużycie RAM", f"{latest['ram_usage']}%")

    if latest['anomaly'] == -1:
        metric_status.error("⚠️ WYKRYTO ANOMALIĘ")
    else:
        metric_status.success("✅ SYSTEM STABILNY")

    # Aktualizacja wykresów
    # Wykres CPU i RAM
    chart_cpu.line_chart(df.set_index('timestamp')[['cpu_usage', 'ram_usage']])
    
    # Wykres Anomaly Score (Decision Function)
    chart_score.area_chart(df.set_index('timestamp')['score'])
    
    time.sleep(1) # Odświeżanie co sekundę
    
    # Wymuszenie odświeżenia strony dla płynności (opcjonalnie)
    if stop_button:
        break