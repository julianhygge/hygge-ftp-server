import os
from pathlib import Path
from dynaconf import Dynaconf

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        app_env = kwargs.get('app_env', None)
        key = (cls, app_env)

        if key not in cls._instances:
            cls._instances[key] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[key]


class ApiConfiguration(metaclass=Singleton):
    def __init__(self, app_env=None):
        if app_env is None:
            app_env = os.environ.get("APP_ENV") or "local"
        base_dir = Path(__file__).resolve().parent.parent
        config_file_path = base_dir / 'config' / '{}.ini'.format(app_env)

        self.settings = Dynaconf(
            envvar_prefix="DYNACONF",
            settings_files=[config_file_path]
        )

    @property
    def db(self):
        return self._get_postgres_config()

    @property
    def logging(self):
        return self.get("logging")

    @property
    def ftp_secret(self):
        return self.get("ftp_secret")

    def get(self, setting, default=None):
        return self.settings.get(setting, default)

    def _get_postgres_config(self):
        db_config = self.get("postgres")
        db_config['port'] = int(db_config.port)
        return db_config