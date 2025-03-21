from ascender.core import Provider
from .minio_service import MinioService

def provideMinio(
    minio_endpoint: str,
    minio_access_key: str,
    minio_secret_key: str,
    minio_secure: bool | None = None,
    minio_verify_ssl: bool | None = None,
    **additional_configurations
) -> list[Provider]:
    return [
        {
            "provide": "MINIO_CONFIGURATION",
            "value": {
                "minio_endpoint": minio_endpoint,
                "minio_access_key": minio_access_key,
                "minio_secret_key": minio_secret_key,
                "minio_secure": minio_secure,
                "minio_verify_ssl": minio_verify_ssl,
                **additional_configurations
            }
        },
        MinioService
    ]