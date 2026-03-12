import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

#eskport modelu
import joblib

#pobieramy naszą bazę danych
conn = sqlite3.connect('monitor_systemu.db')
df = pd.read_sql_query('SELECT * FROM pomiary', conn)
conn.close()

#konwertujemy czas i wydzielamy część do wyszkolenia
df['timestamp'] = pd.to_datetime(df['timestamp'])
X = df[['cpu_usage', 'ram_usage']]

#import modelu
model = IsolationForest(contamination = 0.05, random_state=42)

model.fit(X)

#nowa kategoria
df['anomaly_score'] = model.predict(X)
norma = df[df['anomaly_score'] == 1]
anomalie = df[df['anomaly_score'] == -1]

#reprezentacja ścieżek w drzewie (im więcej tym bardziej skomplikowane rozdzieleniu próbki od pozostałych)
#im mniejsza złożoność rozdzielenia tym większa szanse że próbka jest anomalią
df['path_score'] = model.decision_function(X)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

#Predykcja anomalii CPU
ax1.plot(df['timestamp'], df['cpu_usage'], color='gray', alpha=0.5, label='Sygnał CPU')
ax1.scatter(norma['timestamp'], norma['cpu_usage'], color='blue', s=10, alpha=0.3, label='Norma')
ax1.scatter(anomalie['timestamp'], anomalie['cpu_usage'], color='red', s=30, label='Anomalia')
ax1.set_title('Predykcja modelu - Isolation Forest')
ax1.set_ylabel('Obciążenie CPU [%]')
ax1.legend()

#Złożoność ścieżek
ax2.plot(df['timestamp'], df['path_score'], label='Anomaly Score (Głębokość ścieżki)', color='orange')
ax2.fill_between(df['timestamp'], df['path_score'], 0, where=(df['path_score'] < 0), color='red', alpha=0.3)
ax2.set_ylabel('Decision Score')
ax2.set_xlabel('Czas')
ax2.axhline(0, color='black', lw=1, ls='--') # Linia pomocnicza "0"
ax2.legend()

plt.tight_layout() # Automatyczne dopasowanie marginesów
plt.show()

#zapis modelu
joblib.dump(model, 'trained_isolation_forest.joblib')
print('Zapisano model!')