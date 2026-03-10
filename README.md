Lekki system monitorowania parametrów systemowych (CPU, RAM) w czasie rzeczywistym, wykorzystujący uczenie nienadzorowane (Isolation Forest) do automatycznego wykrywania incydentów i anomalii wydajnościowych. Projekt powstał, aby rozwiązać problem wysokiej liczby fałszywych alarmów (False Positives) w tradycyjnych systemach progowych.

Dzięki zastosowaniu ML jesteśmy w stanie dokonywać trafniejszych detekcji, ponieważ nie określamy sztywno progów anomalii, natomiast nasz model AI dopasowuje się do warunków pracy danego urządzenia.

<img width="1200" height="1000" alt="anomalie1" src="https://github.com/user-attachments/assets/57cdad6d-6b00-4b7a-8276-6fa46c71c7d8" />

**Key Features**  
-Data Acquisition: Pobieranie danych telemetrycznych bezpośrednio z procesów systemowych (psutil).  
-Edge Storage: Lokalna baza danych SQLite zapewniająca spójność danych i buforowanie pomiarów.  
-ML Engine: Implementacja algorytmu Isolation Forest do detekcji outlierów bez konieczności etykietowania danych.  
-Advanced Analytics: Wyznaczanie Anomaly Score na podstawie głębokości izolacji punktów w lesie drzew decyzyjnych.  

W projekcie skupiłem się na wykorzystaniu asymetrii między stanem normalnym a awaryjnym. Algorytm izoluje punkty poprzez losowe podziały cech. Punkty wymagające mniejszej liczby podziałów (krótsza ścieżka w drzewie) są klasyfikowane jako anomalie.

**Kluczowe metryki:**  
-Contamination: Parametr sterujący czułością modelu (suwak między precyzją a czułością).  
-Path Length: Średnia głębokość izolacji, służąca jako miara pewności predykcji.
