import uuid

from mongoengine import UUIDField

from ul_db_utils.modules.mongo_db_modules.db import DbDocument


class BaseDocument(DbDocument):
    meta = {
        'abstract': True,
    }

    id = UUIDField(mongo_name="_id", primary_key=True, required=True, default=uuid.uuid4)

    def to_mongo(self, *args, **kwargs):
        data = super().to_mongo(*args, **kwargs)
        data["id"] = data["_id"]
        return data

    def to_dict(self, only=()):
        return self.to_mongo(fields=only).to_dict()
