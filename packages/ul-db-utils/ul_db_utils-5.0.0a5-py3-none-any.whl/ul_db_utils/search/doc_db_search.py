"""
    Database filtering + sorting util for Document DB
"""

from typing import List, Dict, Optional, Tuple, Any, TypeVar, Type

from flask_mongoengine import Document, BaseQuerySet

from ul_db_utils.utils.filter_conversion_doc_db import filter_converter

TModel = TypeVar('TModel', bound=Document)


def doc_db_search(
    model: Type[TModel],
    filters: Optional[List[Dict[str, Any]]] = None,
    sorts: Optional[List[Tuple[str, str]]] = None,
    limit: Optional[int] = 1000,
    offset: int = 0,
) -> 'BaseQuerySet[TModel]':
    """
    Applies filters, sortings, limit, offset to SqlAlchemy Query

    :filter example: [{"name": "is_alive", "op": "==", "val": "True"}]
    :sort example: [("+", "id"), ("-", "date_modified")]
    """
    query = model.objects
    # Filter the query.
    if filters:
        filters = filter_converter(filters)
        query = query.filter(__raw__=filters)

    if sorts:
        sort = [f"{sort_direct}{sort_field}" for sort_direct, sort_field in sorts]
        query = query.order_by(*sort)

    if limit:
        query = query.limit(limit)

    if offset:
        query = query.skip(offset)
    return query
