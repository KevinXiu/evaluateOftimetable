def dictfetchall(cursor):
    """转换成字典格式"""
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]