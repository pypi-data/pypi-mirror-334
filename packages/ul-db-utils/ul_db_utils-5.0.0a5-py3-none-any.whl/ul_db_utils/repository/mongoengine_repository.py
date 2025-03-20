from abc import ABC
from typing import Optional, List, Dict, Any, Tuple, Iterator
from uuid import UUID

from ul_db_utils.model.base_document import BaseDocument
from ul_db_utils.modules.mongo_db_modules.db import DbDocument
from ul_db_utils.repository.abstract_repository import Repository
from ul_db_utils.search.doc_db_search import doc_db_search
from ul_db_utils.utils.ensure_db_object_exists import ensure_db_object_exists


class MongoEngineRepository(Repository, ABC):
    model: DbDocument

    @classmethod
    def __iter__(cls) -> Iterator[BaseDocument]:
        return cls.model.objects.all()

    @classmethod
    def __len__(cls) -> int:
        return cls.model.objects.count()

    @classmethod
    def get_all(
        cls,
        limit: Optional[int],
        offset: Optional[int] = 0,
        filters: Optional[List[Dict[str, Any]]] = None,
        sorts: Optional[List[Tuple[str, str]]] = None,
    ) -> List[BaseDocument]:
        object_list = doc_db_search(
            model=cls.model,
            filters=filters,
            limit=limit,
            offset=offset if offset else 0,
            sorts=sorts,
        ).all()
        return object_list

    @classmethod
    def get_total_count(
        cls,
        filters: Optional[List[Dict[str, Any]]],
    ) -> int:
        object_list = doc_db_search(
            model=cls.model,
            filters=filters if filters else [],
        ).count()
        return object_list

    @classmethod
    def get_by_id(
        cls,
        id: UUID,
    ) -> BaseDocument:
        obj = cls.model.objects.with_id(id)
        return ensure_db_object_exists(cls.model, obj)

    @classmethod
    def soft_get_by_id(
        cls,
        id: UUID,
    ) -> Optional[BaseDocument]:
        return cls.model.objects.with_id(id)

