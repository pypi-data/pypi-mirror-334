import os.path
from typing import Optional

THIS_LIBRARY_DIR = os.path.dirname(__file__)

APPLICATION__DB_ADDRESS: Optional[str] = os.environ.get('APPLICATION__DB_ADDRESS', None)
APPLICATION__DB_PORT: Optional[str] = os.environ.get('APPLICATION__DB_PORT', None)
APPLICATION__DB_SCHEMA: Optional[str] = os.environ.get('APPLICATION__DB_SCHEMA', None)
APPLICATION__DB_USER: Optional[str] = os.environ.get('APPLICATION__DB_USER', None)
APPLICATION__DB_PASSWORD: Optional[str] = os.environ.get('APPLICATION__DB_PASSWORD', None)
APPLICATION__DB_DATABASE: Optional[str] = os.environ.get('APPLICATION__DB_DATABASE', None)
if all(
    [
        APPLICATION__DB_ADDRESS,
        APPLICATION__DB_PORT,
        APPLICATION__DB_SCHEMA,
        APPLICATION__DB_USER,
        APPLICATION__DB_PASSWORD,
        APPLICATION__DB_DATABASE,
    ]
):
    APPLICATION__DB_URI = f'{APPLICATION__DB_SCHEMA}://{APPLICATION__DB_USER}:{APPLICATION__DB_PASSWORD}@{APPLICATION__DB_ADDRESS}:{APPLICATION__DB_PORT}/{APPLICATION__DB_DATABASE}'
else:
    APPLICATION__DB_URI = os.environ.get('APPLICATION__DB_URI', None)  # none only for backward compatibility
