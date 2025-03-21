import aiobotocore.session

from types_aiobotocore_s3 import S3Client
from types_aiobotocore_s3.type_defs import GetObjectOutputTypeDef, PutObjectOutputTypeDef, DeleteObjectOutputTypeDef, ListObjectsOutputTypeDef

from datetime import timedelta
from typing import Annotated, Any, Mapping

from ascender.common import Injectable
from ascender.core import Service, Inject


@Injectable(provided_in=None)
class MinioService(Service):
    """
    Minio service to interact with Minio storage.

    An Ascender Framework refined version of MinioService. 
    This service is used to interact with Minio storage asynchronously.
    """
    def __init__(
        self, 
        settings: Annotated[Mapping[str, Any], Inject("MINIO_CONFIGURATION")], 
    ):
        self.session = aiobotocore.session.get_session()
        self.config = {
            "service_name": "s3",
            "endpoint_url": settings["minio_endpoint"],
            "aws_access_key_id": settings["minio_access_key"],
            "aws_secret_access_key": settings["minio_secret_key"],
            "use_ssl": settings.get("minio_secure", False),
            "verify": settings.get("minio_verify_ssl", None),
        }
    
    def create_client(self, **additional_configs):
        """
        Creates a new aiobotocore client object.

        Args:
            **additional_configs: Additional configurations to add to the session
        """
        return self.session.create_client(**{**self.config, **additional_configs})

    async def get_object(self, Bucket: str, Key: str, **kwargs) -> GetObjectOutputTypeDef:
        """
        Get data of an object. Returned response should be closed after use to release network resources. To reuse the connection, it's required to call response.release_conn() explicitly

        Args:
            Bucket (str): Directory (bucket) name where the object is stored
            Key (str): Name of the object to get

        Returns:
            [Response]: [Response object]
        """
        async with self.session.create_client(**self.config) as minio:
            minio: S3Client
            response = await minio.get_object(Bucket=Bucket, Key=Key, **kwargs)
        
        return response
    
    async def read_object(self, Bucket: str, Key: str, **kwargs) -> bytes:
        """
        Read data of an object

        Args:
            Bucket (str): Directory (bucket) name where the object is stored
            Key (str): Name of the object to read

        Returns:
            [Response]: [Response object]
        """
        async with self.session.create_client(**self.config) as minio:
            minio: S3Client
            response = await minio.get_object(Bucket=Bucket, Key=Key, **kwargs)

            return await response["Body"].read()
    
    async def put_object(self, Bucket: str, Key: str, Data: Any, ContentLength: int, ContentType: str, **kwargs) -> PutObjectOutputTypeDef:
        """
        Put an object into bucket

        Args:
            Bucket (str): Directory (bucket) name where the object is stored
            Key (str): Name of the object to put
            Data ([type]): Data to put
            length (int): Length of the data
            content_type (str): Content type of the data

        Returns:
            [Response]: [Response object]
        """
        async with self.session.create_client(**self.config) as minio:
            minio: S3Client
            response = await minio.put_object(Bucket=Bucket, Key=Key, Body=Data, ContentLength=ContentLength, ContentType=ContentType, **kwargs)
        
        return response
    
    async def remove_object(self, Bucket: str, Key: str, **kwargs) -> DeleteObjectOutputTypeDef:
        """
        Remove an object from bucket

        Args:
            Bucket (str): Directory (bucket) name where the object is stored
            Key (str): Name of the object to remove

        Returns:
            [Response]: [Response object]
        """
        async with self.session.create_client(**self.config) as minio:
            minio: S3Client
            response = await minio.delete_object(Bucket=Bucket, Key=Key, **kwargs)
        
        return response
    
    async def list_objects(self, Bucket: str, Prefix: str = "", **kwargs) -> ListObjectsOutputTypeDef:
        """
        List objects in a bucket

        Args:
            Bucket (str): Directory (bucket) name where the object is stored
            prefix ([type], optional): Prefix to filter objects. Defaults to None.

        Returns:
            [Response]: [Response object]
        """
        async with self.session.create_client(**self.config) as minio:
            minio: S3Client
            objects = await minio.list_objects(Bucket=Bucket, Prefix=Prefix, **kwargs)
        
        return objects
    
    async def download_file(self, Bucket: str, Key: str, Filename: str, **kwargs) -> None:
        """
        Download an object from bucket

        Args:
            Bucket (str): Directory (bucket) name where the object is stored
            Key (str): Name of the object to download
            Filename ([type]): Destination to save the file

        Returns:
            [Response]: [Response object]
        """
        async with self.session.create_client(**self.config) as minio:
            minio: S3Client
            await minio.download_file(Bucket=Bucket, Key=Key, Filename=Filename, **kwargs)
    
    async def generate_presigned_url(self, Bucket: str, Key: str, ExpiresIn: timedelta = timedelta(days=7)) -> str:
        """
        Generate a pre-signed URL for an object in the bucket.

        Args:
            Bucket (str): The bucket where the object is stored.
            Key (str): The name of the object.
            ExpiresIn (int): Expiration time in seconds (default 3600).

        Returns:
            Observable[str]: An observable emitting the pre-signed URL.
        """
        async with self.session.create_client(**self.config) as minio:
            minio: S3Client
            response = await minio.generate_presigned_url("get_object", Params={"Bucket": Bucket, "Key": Key}, ExpiresIn=ExpiresIn.total_seconds())
        
        return response