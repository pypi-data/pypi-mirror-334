from typing import Optional, Type, TypeVar

from sqlalchemy.exc import NoResultFound as NoResultFoundError

from ul_db_utils.modules.postgres_modules.db import DbModel
from ul_db_utils.modules.mongo_db_modules.db import DbDocument

EnsureModel = TypeVar('EnsureModel', bound=DbModel | DbDocument)


def ensure_db_object_exists(model: Type[EnsureModel], instance: Optional[EnsureModel]) -> EnsureModel:
    if instance is None:
        raise NoResultFoundError(f"{model.__name__} not found")
    return instance
