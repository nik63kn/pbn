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

    @app.template_filter('pluralize_domains')
    def pluralize_domains(count):
        """Возвращает правильную форму слова 'домен' в зависимости от числа"""
        remainder100 = count % 100
        remainder10 = count % 10

        if 11 <= remainder100 <= 19:
            return "доменов"
        elif remainder10 == 1:
            return "домен"
        elif 2 <= remainder10 <= 4:
            return "домена"
        else:
            return "доменов"

    @app.route("/domains")
    def domains_page():
        # Базовые параметры
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        sort_by = request.args.get('sort', 'id')
        sort_dir = request.args.get('direction', 'asc')

        # Начинаем с базового запроса
        query = Domain.query

        # Словарь для хранения примененных фильтров (для отображения)
        applied_filters = {}

        # Применяем фильтры по каждому полю
        if domain_filter := request.args.get('domain'):
            query = query.filter(Domain.domain.ilike(f'%{domain_filter}%'))
            applied_filters['domain'] = domain_filter

        if time_free_filter := request.args.get('time_free'):
            query = query.filter(Domain.time_free == time_free_filter)
            applied_filters['time_free'] = time_free_filter

        if iks_min := request.args.get('iks_min', type=int):
            query = query.filter(Domain.iks >= iks_min)
            applied_filters['iks_min'] = iks_min

        if iks_max := request.args.get('iks_max', type=int):
            query = query.filter(Domain.iks <= iks_max)
            applied_filters['iks_max'] = iks_max

        if age_min := request.args.get('age_min', type=int):
            query = query.filter(Domain.age >= age_min)
            applied_filters['age_min'] = age_min

        if is_org_filter := request.args.get('is_org'):
            query = query.filter(Domain.is_org == is_org_filter)
            applied_filters['is_org'] = is_org_filter

        # Определяем сортировку
        column = getattr(Domain, sort_by)
        if sort_dir == 'desc':
            column = column.desc()

        # Применяем сортировку
        query = query.order_by(column)

        # Получаем общее количество записей после фильтрации
        total = query.count()
        total_pages = math.ceil(total / per_page)

        # Получаем данные для текущей страницы
        domains = query.paginate(page=page, per_page=per_page, error_out=False)

        return render_template(
            "domains.html",
            domains=domains.items,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
            total_domains=total,
            sort_by=sort_by,
            sort_dir=sort_dir,
            applied_filters=applied_filters
        )
