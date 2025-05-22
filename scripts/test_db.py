import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import psycopg2
from config import DB_CONFIG

conn = None
try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    print("Подключение успешно! Версия PostgreSQL:", cursor.fetchone()[0])
except Exception as e:
    print("Ошибка подключения:", e)
finally:
    if conn:
        conn.close()
