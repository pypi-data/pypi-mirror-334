from pathlib import Path

from sanic import Sanic
from sanic.config import Config

from testbench_requirement_service.middleware import check_request_auth, log_request, log_response
from testbench_requirement_service.routes import router


class AppConfig(Config):
    def __init__(
        self,
        config_path: str | None = None,
        reader_class: str | None = None,
        reader_config_path: str | None = None,
        loglevel: str | None = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.CONFIG_PATH = "config.py"
        self.READER_CLASS = "testbench_requirement_service.readers.JsonlFileReader"
        self.READER_CONFIG_PATH = "reader_config.py"
        self.LOGLEVEL = "INFO"
        self.OAS_UI_DEFAULT = "swagger"
        self.OAS_UI_REDOC = False
        self.OAS_CUSTOM_FILE = (Path(__file__).parent / "openapi.yaml").resolve().as_posix()

        if config_path:
            self.CONFIG_PATH = config_path
        if not Path(self.CONFIG_PATH).exists():
            raise FileNotFoundError(f"App config file not found: '{self.CONFIG_PATH}'.")
        self.update_config(Path(self.CONFIG_PATH))

        if reader_class:
            self.READER_CLASS = reader_class
        if reader_config_path:
            self.READER_CONFIG_PATH = reader_config_path
        if loglevel:
            self.LOGLEVEL = loglevel


def create_app(name: str, config: AppConfig | None = None) -> Sanic:
    app = Sanic(name)

    # update app config with custom config
    if not config:
        config = AppConfig()
    app.update_config(config)

    # Register middlewares
    app.register_middleware(check_request_auth, "request")
    app.register_middleware(log_request, "request")
    app.register_middleware(log_response, "response")  # type: ignore

    # Register blueprints
    app.blueprint(router)

    return app
