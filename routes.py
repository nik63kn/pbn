from flask import render_template, request
import psycopg2
from config import DB_CONFIG
import math

def init_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/domains")
    def domains_page():
        # Количество элементов на странице
        per_page = 50
        
        # Получаем номер текущей страницы из параметра запроса
        page = request.args.get('page', 1, type=int)
        
        # Подключение к базе данных
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Получаем общее количество записей
        cur.execute("SELECT COUNT(*) FROM domains")
        total = cur.fetchone()[0]
        
        # Вычисляем общее количество страниц
        total_pages = math.ceil(total / per_page)



        # Получаем данные для текущей страницы
        offset = (page - 1) * per_page
        cur.execute(
            "SELECT id, domain, time_free, iks, age, is_org, bet, links_expired "
            "FROM domains ORDER BY id LIMIT %s OFFSET %s",
            (per_page, offset)
        )
        domains = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return render_template(
            "domains.html",
            domains=domains,
            page=page,
            total_pages=total_pages,
            total_domains=total
        )