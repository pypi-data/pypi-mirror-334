from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    DEBUG: bool = False
    RUN_PORT: int = 5000
    TIME_ZONE: str = "Asia/Taipei"

    OPEN_API_URL: str = "/openapi.json"

    # Request
    REQUEST_VERIFY_SSL: bool = True
    REQUEST_PROXY: str = ''
    REQUEST_RETRY: int = 5
    REQUEST_CONN_TIMEOUT: float = 5
    REQUEST_READ_TIMEOUT: float = 5
    REQUEST_WRITE_TIMEOUT: float = 5
    REQUEST_POOL_TIMEOUT: float = 5

    # AWS
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_KEY: str = ""
    AWS_REGION: str = ""
    AWS_PARAMETER_PATH_PREFIX: str = ""
    AWS_LOGGROUP_NAME: str = ""

    # MariaDB
    DATABASE_HOST: str = ''
    DATABASE_USERNAME: str = ''
    DATABASE_PASSWORD: str = ''
    DATABASE_PORT: int = 3306
    DATABASE_NAME: str = ""

    # Exception Notify
    WEBHOOK_BASE_URL: str = ""

    class Config:
        case_sensitive = False
