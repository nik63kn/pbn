import psycopg2
from config import DB_CONFIG

def create_table():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS domains (
            id SERIAL PRIMARY KEY,
            domain TEXT NOT NULL,
            time_free DATE,
            iks INTEGER,
            age INTEGER,
            is_org BOOLEAN DEFAULT FALSE,
            bet NUMERIC(10, 2),
            links_expired BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_table()
    print("Таблица 'domains' создана или уже существует.")