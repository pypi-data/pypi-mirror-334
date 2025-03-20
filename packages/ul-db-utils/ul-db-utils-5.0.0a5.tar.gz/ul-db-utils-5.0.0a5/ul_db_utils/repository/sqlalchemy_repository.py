from abc import ABC
from typing import Optional, List, Dict, Any, Tuple
from uuid import UUID

from sqlalchemy.orm import Query, Session
from ul_py_tool.utils.class_property import classproperty

from ul_db_utils.model.base_model import BaseModel
from ul_db_utils.modules.postgres_modules.db import DbModel, db

from ul_db_utils.repository.abstract_repository import Repository
from ul_db_utils.search.db_search import db_search
from ul_db_utils.utils.ensure_db_object_exists import ensure_db_object_exists


class SQLAlchemyRepository(Repository, ABC):
    model: DbModel

    @classproperty
    def session(cls) -> Session:
        return db.session

    @classmethod
    def get_all(
        cls,
        limit: int,
        offset: int,
        filters: Optional[List[Dict[str, Any]]],
        sorts: Optional[List[Tuple[str, str]]],
        initial_query: 'Optional[Query[BaseModel]]' = None,
    ) -> List[BaseModel]:
        object_list = db_search(
            model=cls.model,
            filters=filters,
            sorts=sorts,
            limit=limit,
            offset=offset,
            initial_query=initial_query,
        ).all()
        return object_list

    @classmethod
    def get_total_count(
        cls,
        filters: Optional[List[Dict[str, Any]]],
        initial_query: 'Optional[Query[BaseModel]]' = None,
    ) -> int:
        list_count = db_search(
            model=cls.model,
            initial_query=initial_query,
            filters=filters,
        ).count()
        return list_count

    @classmethod
    def get_by_id(
        cls,
        id: UUID,
    ) -> BaseModel:
        obj = cls.model.query.filter_by(id=id).first()
        return ensure_db_object_exists(cls.model, obj)

    @classmethod
    def soft_get_by_id(
        cls,
        id: UUID,
    ) -> Optional[BaseModel]:
        return cls.model.query.filter_by(id=id).first()
