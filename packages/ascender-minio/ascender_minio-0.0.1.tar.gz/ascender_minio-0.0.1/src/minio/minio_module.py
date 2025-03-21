from typing import Self
from ascender.core import AscModule

from .minio_provider import provideMinio
from .minio_service import MinioService


class MinioModule:
    @staticmethod
    def forRoot(
        minio_endpoint: str,
        minio_access_key: str,
        minio_secret_key: str,
        minio_secure: bool | None = None,
        minio_verify_ssl: bool | None = None,
        **additional_configurations
    ) -> "MinioModule":
        return AscModule(
            providers=[
                provideMinio(
                    minio_endpoint,
                    minio_access_key,
                    minio_secret_key,
                    minio_secure,
                    minio_verify_ssl,
                    **additional_configurations
                )
            ],
            exports=[
                MinioService
            ]
        )(MinioModule)