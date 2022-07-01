from .containers import AppContainer

APP_CONTAINER = AppContainer()
APP_CONTAINER.config.from_yaml("./configs/test.yml")
APP_CONTAINER.check_dependencies()
