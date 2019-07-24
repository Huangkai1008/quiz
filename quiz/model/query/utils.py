def and_pagination(query, page=1, size=10):
    """分页"""
    pos = (page - 1) * size
    return query.limit(size).offset(pos)
