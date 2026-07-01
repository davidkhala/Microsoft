"""
IBM Cloud Object Storage (COS) storage backend.

Requires: ibm-cos-sdk, ibm_boto3
Install with: pip install sharepoint-connector[cos]
"""

import logging
from typing import Optional, Dict, Any

try:
    import ibm_boto3
    from ibm_botocore.client import Config as BotoConfig
    IBM_COS_AVAILABLE = True
except ImportError:
    IBM_COS_AVAILABLE = False

from .base import StorageBackend

logger = logging.getLogger(__name__)


class COSConfig:
    """IBM Cloud Object Storage Configuration"""

    def __init__(
        self,
        api_key: str,
        endpoint: str,
        bucket_name: str,
        instance_crn: Optional[str] = None
    ):
        self.api_key = api_key
        self.endpoint = endpoint
        self.bucket_name = bucket_name
        self.instance_crn = instance_crn


class COSStorage(StorageBackend):
    """
    IBM Cloud Object Storage backend.

    S3-compatible storage provided by IBM Cloud.
    """

    def __init__(self, config: COSConfig):
        if not IBM_COS_AVAILABLE:
            raise ImportError(
                "IBM COS dependencies not installed. "
                "Install with: pip install sharepoint-connector[cos]"
            )

        self.config = config
        self._client = None
        self._init_client()

    @property
    def backend_name(self) -> str:
        return "ibm-cos"

    def _init_client(self):
        """Initialize IBM COS client"""
        self._client = ibm_boto3.resource(
            "s3",
            ibm_api_key_id=self.config.api_key,
            ibm_endpoint_url=self.config.endpoint,
            config=BotoConfig(
                signature_version="oauth",
                max_pool_connections=200,
                user_agent_extra="sharepoint-connector"
            )
        )

        # Verify bucket access
        try:
            self._client.Bucket(self.config.bucket_name).load()
            logger.info(f"Connected to COS bucket: {self.config.bucket_name}")
        except Exception as e:
            logger.error(f"Failed to access bucket: {e}")
            raise

    def upload_file(
        self,
        content: bytes,
        key: str,
        metadata: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Upload file to IBM COS.

        Args:
            content: File content as bytes
            key: Destination key/path in bucket
            metadata: Optional metadata to attach

        Returns:
            Dict with upload results
        """
        logger.info(f"Uploading to COS: {key}")

        self._client.Bucket(self.config.bucket_name).put_object(
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

    def get_object_url(self, key: str) -> str:
        """Get the object URL reference"""
        return f"{self.config.endpoint}/{self.config.bucket_name}/{key}"

    def get_location_info(self) -> Dict[str, str]:
        """Get COS location information"""
        return {
            "backend": self.backend_name,
            "bucket": self.config.bucket_name,
            "endpoint": self.config.endpoint
        }

    @property
    def client(self):
        """Get the raw IBM COS client for advanced operations"""
        return self._client
