from math import ceil


def paginate(query, page, per_page=10):
    if page < 1:
        page = 1
    total = query.count()
    items = query.limit(per_page).offset((page - 1) * per_page).all()
    pages = ceil(total / per_page) if per_page else 1
    return {
        'items': items,
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': pages
    }
