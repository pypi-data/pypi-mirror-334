import importlib
import logging
import os
from glob import glob
from typing import Optional, TYPE_CHECKING, Callable, TypeVar, Union

from flask import Flask
from flask_mongoengine import MongoEngine
from pymongo.collection import Collection
from pymongo import uri_parser

from ul_db_utils.conf import APPLICATION__DB_URI

if TYPE_CHECKING:
    from api_utils.modules.api_sdk import ApiSdk  # type: ignore
    from api_utils.modules.worker_sdk import WorkerSdk  # type: ignore


db: 'MongoEngine' = MongoEngine()

DbDocument = db.Document

logger = logging.getLogger(__name__)


TFn = TypeVar("TFn", bound=Callable)  # type: ignore


initialized_sdk: Optional['MongoDbConfig'] = None


class MongoDbConfig:
    """
    DbConfig for document databases of MongoDB DBS

    example:
        db_config = MongoDbConfig(
            uri="mongodb://localhost/database_name",
            models_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dir_name', 'model_dir_name'),
        )
    """

    def __init__(
        self,
        *,
        uri: Optional[str] = APPLICATION__DB_URI,
        models_path: str,
        repositories_path: Optional[str] = None,
        debug: bool = False,
        **ext_configs,
    ) -> None:
        assert uri
        self.uri = uri
        self.models_path = models_path
        self.repositories_path = repositories_path
        self.ext_configs = ext_configs
        self.debug = debug

        self._flask_app: Optional[Flask] = None

        assert os.path.exists(models_path), f'path of models {models_path} is not exists'

    @property
    def db(self) -> Optional[Collection]:
        db_instance = db.connection.get_default_database()
        if db_instance is None:
            raise OverflowError('DB instance must be initialized')
        return db_instance

    def _load_models(self) -> None:
        assert db.connection is not None, "DB connection must be established"
        self._load_route_modules(self.models_path)

    def _load_repositories(self) -> None:
        if self.repositories_path:
            self._load_route_modules(self.repositories_path)

    def _load_route_modules(self, dir: str, file_pref: str = '') -> None:
        suf = '.py'
        files = set()
        for route in glob(os.path.join(dir, f'{file_pref}*{suf}')):
            files.add(str(route))
        for route in glob(os.path.join(dir, f'**/{file_pref}*{suf}')):
            files.add(str(route))
        for file in files:
            file_rel = os.path.relpath(file, os.getcwd())
            mdl = file_rel[:-len(suf)].replace('\\', '/').strip('/').replace('/', '.')
            if self.debug:
                logger.info('loading module %s', mdl)
            importlib.import_module(mdl)

    def _init_from_sdk_with_flask(  # PRIVATE. ONLY FOR INTERNAL API-UTILS USAGE
        self,
        sdk: Union['ApiSdk', 'WorkerSdk'],
    ) -> None:
        global initialized_sdk
        if initialized_sdk is not None:
            raise OverflowError('initialized DbConfig must be only one! Db has already initialized')
        initialized_sdk = self

        if self._flask_app is not None:
            raise OverflowError()
        self._flask_app = sdk._flask_app

        self._flask_app.app_context().push()  # FUCKING HACK
        self._attach_to_flask_app(self._flask_app, db, **self.ext_configs)
        self._load_models()
        self._load_repositories()

    def init_with_flask(self, app_name: str) -> Flask:
        global initialized_sdk
        if initialized_sdk is not None:
            raise OverflowError('initialized DbConfig must be only one! Db has already initialized')
        initialized_sdk = self

        if self._flask_app is not None:
            raise OverflowError()
        self._flask_app = Flask(app_name)

        self._flask_app.app_context().push()  # FUCKING HACK
        self._attach_to_flask_app(self._flask_app, db, **self.ext_configs)
        self._load_models()
        self._load_repositories()

        return self._flask_app

    def _attach_to_flask_app(self, app: Flask, db_instance: 'MongoEngine', **mongo_client_configs) -> None:
        app.config["MONGODB_SETTINGS"] = [
            {
                "db": uri_parser.parse_uri(self.uri).get('database'),
                "host": self.uri,
            }
        ]
        db_instance.init_app(app, **mongo_client_configs)
