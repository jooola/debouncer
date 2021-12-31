from .app import create_app
from .config import get_config

app = create_app(get_config())
