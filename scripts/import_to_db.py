import psycopg2
import csv
from datetime import datetime

DB_CONFIG = {
    "host": "localhost",
    "database": "domain_monitor",
    "user": "domain_user",
    "password": "secure_password_123"
}

file_path = "/var/www/data_scripts/scripts/expired.csv"

def parse_bet(val):
    try:
        val = val.strip()
        if val.lower() in ('', 'нет', 'n/a'):
            return None
        return float(val.replace(',', '.'))
    except Exception:
        return None

def parse_int(val):
    try:
        return int(val)
    except (ValueError, TypeError):
        return None

def parse_row(row):
    return (
        row['Домен'],
        row['Ставка'],
        datetime.strptime(row['Дата освобождения'], '%Y-%m-%d').date() if row['Дата освобождения'] else None,
        parse_int(row['ИКС']),
        parse_int(row['Возраст']),
        row['Юр.'] if row['Юр.'] else None,
        parse_int(row['Links']),
    )

def insert_data_to_db(data):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    for row in data:
        cursor.execute(
            """
            INSERT INTO domains (domain, bet, time_free, iks, age, is_org, links_expired)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (domain) DO UPDATE SET
                bet = EXCLUDED.bet,
                time_free = EXCLUDED.time_free,
                iks = EXCLUDED.iks,
                age = EXCLUDED.age,
                is_org = EXCLUDED.is_org,
                links_expired = EXCLUDED.links_expired
            """,
            row
        )
    conn.commit()
    cursor.close()
    conn.close()

def main():
    data = []
    with open(file_path, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            data.append(parse_row(row))
    insert_data_to_db(data)

if __name__ == '__main__':
    main()
