from flask import render_template, request
import math
from models import Domain


def init_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route('/check_dates')
    def check_dates():
        domain = Domain.query.first()
        return f"Updated at: {domain.updated_at}, Type: {type(domain.updated_at)}"

    @app.route("/domains")
    def domains_page():
        # Количество элементов на странице
        per_page = 50

        # Получаем номер текущей страницы из параметра запроса
        page = request.args.get('page', 1, type=int)

        sort_by = request.args.get('sort', 'id')
        sort_dir = request.args.get('direction', 'asc')

        if not hasattr(Domain, sort_by):
            sort_by = 'id'

        column = getattr(Domain, sort_by)
        if sort_dir == 'desc':
            column = column.desc()

        # Получаем общее количество записей
        total = Domain.query.count()

        # Вычисляем общее количество страниц
        total_pages = math.ceil(total / per_page)

        # Получаем данные для текущей страницы с пагинацией
        pagination = Domain.query.order_by(column).paginate(
            page=page, per_page=per_page, error_out=False)

        domains = pagination.items

        return render_template(
            "domains.html",
            domains=domains,
            page=page,
            total_pages=total_pages,
            total_domains=total,
            sort_by = sort_by,
            sort_dir = sort_dir
        )
