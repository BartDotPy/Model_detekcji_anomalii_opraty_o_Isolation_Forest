import psutil
import time
import sqlite3

conn = sqlite3.connect('monitor_systemu.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS pomiary(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               timestamp DATATIME DEFAULT CURRENT_TIMESTAMP,
               cpu_usage REAL,
               ram_usage REAL)           
               ''')
print("Rozpoczęto zbieranie danych")

try:
    while True:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent

        cursor.execute('''
                       INSERT INTO pomiary (cpu_usage, ram_usage)
                       VALUES(?,?)''', (cpu, ram))
        
        conn.commit()
        print(f"Zapisano: CPU {cpu}%, | RAM {ram}%")

except KeyboardInterrupt:
    print('Zatrzymano zbieranie danych!')

finally:
    conn.close()