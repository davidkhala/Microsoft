"""
Generic S3-compatible storage backend.

Supports AWS S3, MinIO, Ceph, and any S3-compatible storage.
Requires: boto3
Install with: pip install sharepoint-connector[s3]
"""

import logging
from typing import Optional, Dict, Any

try:
    import boto3
    from botocore.client import Config as BotoConfig
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False

from .base import StorageBackend

logger = logging.getLogger(__name__)


class S3Config:
    """S3-compatible storage configuration"""

    def __init__(
        self,
        access_key_id: str,
        secret_access_key: str,
        bucket_name: str,
        endpoint_url: Optional[str] = None,  # If None, uses AWS default
        region: str = "us-east-1",
        session_token: Optional[str] = None
    ):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.bucket_name = bucket_name
        self.endpoint_url = endpoint_url
        self.region = region
        self.session_token = session_token


class S3Storage(StorageBackend):
    """
    Generic S3-compatible storage backend.

    Works with:
    - AWS S3 (default)
    - MinIO
    - Ceph RGW
    - Any S3-compatible storage
    """

    def __init__(self, config: S3Config):
        if not BOTO3_AVAILABLE:
            raise ImportError(
                "boto3 not installed. "
                "Install with: pip install sharepoint-connector[s3]"
            )

        self.config = config
        self._client = None
        self._resource = None
        self._init_client()

    @property
    def backend_name(self) -> str:
        return "s3"

    def _init_client(self):
        """Initialize S3 client"""
        boto_config = BotoConfig(
            max_pool_connections=200,
            user_agent_extra="sharepoint-connector"
        )

        client_kwargs = {
            "aws_access_key_id": self.config.access_key_id,
            "aws_secret_access_key": self.config.secret_access_key,
            "region_name": self.config.region,
            "config": boto_config
        }

        if self.config.endpoint_url:
            client_kwargs["endpoint_url"] = self.config.endpoint_url
        if self.config.session_token:
            client_kwargs["aws_session_token"] = self.config.session_token

        self._resource = boto3.resource("s3", **client_kwargs)

        # Verify bucket access
        try:
            self._resource.Bucket(self.config.bucket_name).load()
            logger.info(f"Connected to S3 bucket: {self.config.bucket_name}")
        except Exception as e:
            logger.error(f"Failed to access bucket: {e}")
            raise

    def upload_file(
        self,
        content: bytes,
        key: str,
        metadata: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Upload file to S3"""
        logger.info(f"Uploading to S3: {key}")

        self._resource.Bucket(self.config.bucket_name).put_object(
            Key=key,
            Body=content,
            Metadata=metadata or {}
        )

        logger.info(f"Upload complete: {key}")
        return {
            "key": key,
            "bucket": self.config.bucket_name,
            "size_bytes": len(content),
            "backend": self.backend_name
        }

    def get_location_info(self) -> Dict[str, str]:
        """Get S3 location information"""
        info = {
            "backend": self.backend_name,
            "bucket": self.config.bucket_name,
            "region": self.config.region
        }
        if self.config.endpoint_url:
            info["endpoint"] = self.config.endpoint_url
        return info

    @property
    def resource(self):
        """Get the raw boto3 resource for advanced operations"""
        return self._resource
