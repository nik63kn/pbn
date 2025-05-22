from flask import render_template, request
import math
from models import Domain


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

        # Получаем общее количество записей
        total = Domain.query.count()

        # Вычисляем общее количество страниц
        total_pages = math.ceil(total / per_page)

        # Получаем данные для текущей страницы с пагинацией
        pagination = Domain.query.order_by(Domain.id).paginate(
            page=page, per_page=per_page, error_out=False)

        domains = pagination.items

        return render_template(
            "domains.html",
            domains=domains,
            page=page,
            total_pages=total_pages,
            total_domains=total
        )
