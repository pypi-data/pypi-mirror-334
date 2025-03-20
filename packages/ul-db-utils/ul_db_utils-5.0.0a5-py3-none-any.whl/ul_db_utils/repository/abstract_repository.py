from abc import ABC, abstractmethod
from typing import Any, List, Optional, Dict, Tuple
from uuid import UUID


class Repository(ABC):

    @classmethod
    @abstractmethod
    def get_all(
        cls,
        limit: int,
        offset: int,
        filters: Optional[List[Dict[str, Any]]],
        sorts: Optional[List[Tuple[str, str]]],
    ) -> List[Any]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_total_count(
        cls,
        filters: Optional[List[Dict[str, Any]]],
    ) -> int:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_by_id(cls, id: UUID) -> Any:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def create(cls, item: Any) -> Any:
        raise NotImplementedError

    @classmethod
    def update(cls, item: Any) -> Any:
        raise NotImplementedError

    @classmethod
    def delete(cls, item: Any) -> None:
        raise NotImplementedError

    @classmethod
    def delete_by_id(cls, id: UUID) -> None:
        raise NotImplementedError
