import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

#pobieramy naszą bazę danych
conn = sqlite3.connect('monitor_systemu.db')
df = pd.read_sql_query('SELECT * FROM pomiary', conn)
conn.close()

#konwertujemy czas i wydzielamy część do wyszkolenia
df['timestamp'] = pd.to_datetime(df['timestamp'])
X = df[['cpu_usage', 'ram_usage']]

#import modelu
model = IsolationForest(contamination = 0.05, random_state=42)

#nowa kategoria
df['anomaly_score'] = model.fit_predict(X)
norma = df[df['anomaly_score'] == 1]
anomalie = df[df['anomaly_score'] == -1]

#rysowanie
plt.figure(figsize=(12,6))
plt.plot(df['timestamp'], df['cpu_usage'], color = 'gray')
plt.scatter(norma['timestamp'], norma['cpu_usage'], color = 'blue', alpha = 0.3)
plt.scatter(anomalie['timestamp'],  anomalie['cpu_usage'], color = 'red', alpha = 0.3)
plt.title('Predykcja modelu - anomalnie w obciążeniu CPU - Isolation Forest')
plt.xlabel('Czas')
plt.ylabel('Obciążenie CPU [%]')
plt.legend()
plt.show()