#!/usr/bin/env python3
"""
SharePoint to Storage Connector Server

A server that provides file transfer from SharePoint to various storage backends:
- IBM Cloud Object Storage (COS)
- Generic S3-compatible storage (AWS S3, MinIO, etc.)
- Extensible for additional backends

Usage (with IBM COS):
    python main.py \\
        --sharepoint-client-id YOUR_CLIENT_ID \\
        --sharepoint-client-secret YOUR_CLIENT_SECRET \\
        --sharepoint-tenant-id YOUR_TENANT_ID \\
        --sharepoint-site-url "https://yourtenant.sharepoint.com/sites/yoursite" \\
        --storage-backend cos \\
        --cos-api-key YOUR_COS_API_KEY \\
        --cos-endpoint "https://s3.direct.us-south.cloud-object-storage.appdomain.cloud" \\
        --cos-bucket-name your-bucket-name

Usage (with S3):
    python main.py \\
        --sharepoint-client-id YOUR_CLIENT_ID \\
        --sharepoint-client-secret YOUR_CLIENT_SECRET \\
        --sharepoint-tenant-id YOUR_TENANT_ID \\
        --sharepoint-site-url "https://yourtenant.sharepoint.com/sites/yoursite" \\
        --storage-backend s3 \\
        --s3-access-key-id YOUR_ACCESS_KEY \\
        --s3-secret-key YOUR_SECRET_KEY \\
        --s3-bucket-name your-bucket-name
"""

import os
import json
import logging
import argparse
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse

# HTTP requests
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# SharePoint Configuration
# ============================================================================

class SharePointConfig:
    """SharePoint OAuth 2.0 Configuration"""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        tenant_id: str,
        site_url: str,
        redirect_url: Optional[str] = "http://localhost:8080/callback"
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.site_url = site_url
        self.redirect_url = redirect_url

        # Derive authentication endpoints
        self.authorize_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize"
        self.token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

        # SharePoint API scopes
        self.scopes = ["https://graph.microsoft.com/.default"]


# ============================================================================
# SharePoint Authentication (OAuth 2.0 - Client Credentials Flow)
# ============================================================================

class SharePointAuthenticator:
    """
    Handles SharePoint authentication using OAuth 2.0 Client Credentials Flow.
    No hardcoded tokens - refreshes automatically.
    """

    def __init__(self, config: SharePointConfig):
        self.config = config
        self._access_token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None

    def get_access_token(self) -> str:
        """Get valid access token, refreshing if necessary"""
        if self._access_token and self._token_expiry and datetime.now() < self._token_expiry:
            return self._access_token

        return self._refresh_token()

    def _refresh_token(self) -> str:
        """Refresh access token using client credentials"""
        data = {
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
            "scope": " ".join(self.config.scopes),
            "grant_type": "client_credentials"
        }

        response = requests.post(self.config.token_url, data=data)
        response.raise_for_status()

        token_data = response.json()
        self._access_token = token_data["access_token"]

        # Set expiry (subtract 5 minutes buffer)
        expires_in = token_data.get("expires_in", 3600)
        self._token_expiry = datetime.now() + timedelta(seconds=expires_in - 300)

        logger.info("Access token refreshed successfully")
        return self._access_token


# ============================================================================
# SharePoint File Operations
# ============================================================================

class SharePointClient:
    """Client for interacting with SharePoint via Microsoft Graph API"""

    BASE_GRAPH_URL = "https://graph.microsoft.com/v1.0"

    def __init__(self, config: SharePointConfig):
        self.config = config
        self.auth = SharePointAuthenticator(config)
        self._parse_site_info()

    def _parse_site_info(self):
        """Parse hostname and site path from site URL"""
        # Extract host and path from URL like:
        # https://contoso.sharepoint.com/sites/mysite
        from urllib.parse import urlparse
        parsed = urlparse(self.config.site_url)
        self.hostname = parsed.hostname  # contoso.sharepoint.com
        self.site_path = parsed.path.strip("/")  # sites/mysite

    def _get_headers(self) -> Dict[str, str]:
        """Get headers with fresh access token"""
        return {
            "Authorization": f"Bearer {self.auth.get_access_token()}",
            "Accept": "application/json"
        }

    def _get_site_id(self) -> str:
        """Get SharePoint site ID from hostname and path"""
        url = f"{self.BASE_GRAPH_URL}/sites/{self.hostname}:{self.site_path}"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()["id"]

    def get_file_by_path(self, file_path: str) -> bytes:
        """
        Download a file from SharePoint by its relative path.

        Args:
            file_path: Relative path within the site (e.g., "Shared Documents/folder/file.pdf")

        Returns:
            File content as bytes
        """
        logger.info(f"Downloading file from SharePoint: {file_path}")

        # Get site ID (cached for performance)
        if not hasattr(self, '_site_id'):
            self._site_id = self._get_site_id()

        # Encode the path for URL
        encoded_path = file_path.replace("/", ":/")

        # Get download URL
        url = f"{self.BASE_GRAPH_URL}/sites/{self._site_id}/drive/root:/{encoded_path}"
        response = requests.get(url, headers=self._get_headers())

        if response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
        response.raise_for_status()

        download_url = response.json()["@microsoft.graph.downloadUrl"]

        # Download the actual file
        file_response = requests.get(download_url)
        file_response.raise_for_status()

        logger.info(f"Downloaded {len(file_response.content)} bytes")
        return file_response.content

    def list_files(self, folder_path: str = "") -> list:
        """List files in a SharePoint folder"""
        if not hasattr(self, '_site_id'):
            self._site_id = self._get_site_id()

        if folder_path:
            encoded_path = folder_path.replace("/", ":/")
            url = f"{self.BASE_GRAPH_URL}/sites/{self._site_id}/drive/root:/{encoded_path}:/children"
        else:
            url = f"{self.BASE_GRAPH_URL}/sites/{self._site_id}/drive/root/children"

        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()

        items = response.json().get("value", [])
        return [{"name": i["name"], "type": "file" if "file" in i else "folder"} for i in items]


# ============================================================================
# Storage Backend Factory
# ============================================================================

def create_storage_backend(backend_type: str, args) -> 'StorageBackend':
    """
    Factory function to create storage backend based on type.

    Args:
        backend_type: 'cos' or 's3'
        args: Parsed CLI arguments

    Returns:
        StorageBackend instance
    """
    if backend_type == "cos":
        try:
            from storage.cos import COSStorage, COSConfig
            config = COSConfig(
                api_key=args.cos_api_key,
                endpoint=args.cos_endpoint,
                bucket_name=args.cos_bucket_name,
                instance_crn=getattr(args, 'cos_instance_crn', None)
            )
            return COSStorage(config)
        except ImportError as e:
            raise ImportError(
                "IBM COS dependencies not installed. "
                "Install with: pip install -r requirements-cos.txt"
            ) from e

    elif backend_type == "s3":
        try:
            from storage.s3 import S3Storage, S3Config
            config = S3Config(
                access_key_id=args.s3_access_key_id,
                secret_access_key=args.s3_secret_key,
                bucket_name=args.s3_bucket_name,
                endpoint_url=getattr(args, 's3_endpoint_url', None),
                region=getattr(args, 's3_region', 'us-east-1'),
                session_token=getattr(args, 's3_session_token', None)
            )
            return S3Storage(config)
        except ImportError as e:
            raise ImportError(
                "S3 dependencies not installed. "
                "Install with: pip install -r requirements-s3.txt"
            ) from e

    else:
        raise ValueError(f"Unknown storage backend type: {backend_type}")


# ============================================================================
# Main Connector Service
# ============================================================================

class SharePointToStorageConnector:
    """Main connector service - SharePoint to pluggable storage backend"""

    def __init__(self, sharepoint_config: SharePointConfig, storage_backend: 'StorageBackend'):
        self.sharepoint = SharePointClient(sharepoint_config)
        self.storage = storage_backend

    def transfer_file(
        self,
        sharepoint_path: str,
        storage_key: Optional[str] = None,
        preserve_path: bool = True
    ) -> Dict[str, Any]:
        """
        Transfer a file from SharePoint to storage backend.

        Args:
            sharepoint_path: Path to file in SharePoint (relative to site root)
            storage_key: Optional storage key (default: uses SharePoint filename)
            preserve_path: Whether to preserve folder structure in storage

        Returns:
            Transfer result with storage location
        """
        # Download from SharePoint
        content = self.sharepoint.get_file_by_path(sharepoint_path)

        # Determine storage key
        if storage_key is None:
            filename = os.path.basename(sharepoint_path)
            if preserve_path:
                folder = os.path.dirname(sharepoint_path)
                storage_key = f"{folder}/{filename}" if folder else filename
            else:
                storage_key = f"{datetime.now().strftime('%Y/%m/%d')}/{filename}"

        # Upload to storage
        result = self.storage.upload_file(
            content=content,
            key=storage_key,
            metadata={
                "source": "sharepoint",
                "original_path": sharepoint_path,
                "transferred_at": datetime.now().isoformat()
            }
        )

        location_info = self.storage.get_location_info()

        return {
            "success": True,
            "sharepoint_path": sharepoint_path,
            "storage_key": result.get("key", storage_key),
            "storage_backend": result.get("backend", "unknown"),
            "storage_location": location_info,
            "size_bytes": len(content),
            "transferred_at": datetime.now().isoformat()
        }


# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(title="SharePoint to Storage Connector")

# Add CORS middleware - allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global connector instance (initialized at startup)
connector: Optional[SharePointToStorageConnector] = None


class TransferRequest(BaseModel):
    sharepoint_path: str
    storage_key: Optional[str] = None
    preserve_path: bool = True


class TransferResponse(BaseModel):
    success: bool
    sharepoint_path: str
    storage_key: str
    storage_backend: str
    storage_location: Dict[str, str]
    size_bytes: int
    transferred_at: str


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "sharepoint-storage-connector",
        "storage_backend": connector.storage.backend_name if connector else "not_initialized",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/v1/transfer", response_model=TransferResponse)
async def transfer_file(request: TransferRequest):
    """
    Transfer a file from SharePoint to the configured storage backend.

    Request body:
        sharepoint_path: Path to file in SharePoint (e.g., "Shared Documents/folder/file.pdf")
        storage_key: Optional destination key in storage
        preserve_path: Whether to preserve folder structure (default: true)
    """
    if connector is None:
        raise HTTPException(status_code=503, detail="Connector not initialized")

    try:
        result = connector.transfer_file(
            sharepoint_path=request.sharepoint_path,
            storage_key=request.storage_key,
            preserve_path=request.preserve_path
        )
        return result
    except Exception as e:
        logger.error(f"Transfer failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/list/{folder_path:path}")
async def list_files(folder_path: str = ""):
    """List files in a SharePoint folder"""
    if connector is None:
        raise HTTPException(status_code=503, detail="Connector not initialized")

    try:
        files = connector.sharepoint.list_files(folder_path or "")
        return {"files": files, "path": folder_path or "/"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# CLI Entry Point
# ============================================================================

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="SharePoint to Storage Connector Server",
        epilog="Storage backends: cos (IBM COS), s3 (AWS S3/MinIO)"
    )

    # SharePoint configuration
    parser.add_argument(
        "--sharepoint-client-id",
        required=True,
        help="SharePoint OAuth Client ID"
    )
    parser.add_argument(
        "--sharepoint-client-secret",
        required=True,
        help="SharePoint OAuth Client Secret"
    )
    parser.add_argument(
        "--sharepoint-tenant-id",
        required=True,
        help="SharePoint Tenant ID"
    )
    parser.add_argument(
        "--sharepoint-site-url",
        required=True,
        help="SharePoint Site URL (e.g., https://tenant.sharepoint.com/sites/mysite)"
    )
    parser.add_argument(
        "--sharepoint-redirect-url",
        default="http://localhost:8080/callback",
        help="OAuth redirect URL (default: http://localhost:8080/callback)"
    )

    # Storage backend selection
    parser.add_argument(
        "--storage-backend",
        required=True,
        choices=["cos", "s3"],
        help="Storage backend type: 'cos' for IBM COS, 's3' for S3-compatible storage"
    )

    # IBM COS configuration (required if --storage-backend=cos)
    cos_group = parser.add_argument_group("IBM COS options (required when --storage-backend=cos)")
    cos_group.add_argument(
        "--cos-api-key",
        help="IBM COS API Key"
    )
    cos_group.add_argument(
        "--cos-endpoint",
        help="IBM COS Endpoint URL (e.g., https://s3.direct.us-south.cloud-object-storage.appdomain.cloud)"
    )
    cos_group.add_argument(
        "--cos-bucket-name",
        help="IBM COS Bucket Name"
    )
    cos_group.add_argument(
        "--cos-instance-crn",
        help="IBM COS Instance CRN (optional)"
    )

    # S3 configuration (required if --storage-backend=s3)
    s3_group = parser.add_argument_group("S3 options (required when --storage-backend=s3)")
    s3_group.add_argument(
        "--s3-access-key-id",
        help="AWS S3 Access Key ID"
    )
    s3_group.add_argument(
        "--s3-secret-key",
        help="AWS S3 Secret Access Key"
    )
    s3_group.add_argument(
        "--s3-bucket-name",
        help="S3 Bucket Name"
    )
    s3_group.add_argument(
        "--s3-endpoint-url",
        help="S3 Endpoint URL (for S3-compatible services like MinIO, defaults to AWS)"
    )
    s3_group.add_argument(
        "--s3-region",
        default="us-east-1",
        help="S3 Region (default: us-east-1)"
    )
    s3_group.add_argument(
        "--s3-session-token",
        help="S3 Session Token (for temporary credentials, optional)"
    )

    # Server configuration (host hardcoded to 0.0.0.0 for all access)
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Server port (default: 8000)"
    )

    return parser.parse_args()


def validate_arguments(args):
    """Validate that required arguments are present for the selected backend"""
    if args.storage_backend == "cos":
        if not all([args.cos_api_key, args.cos_endpoint, args.cos_bucket_name]):
            parser.error("--cos-api-key, --cos-endpoint, and --cos-bucket-name are required when --storage-backend=cos")

    elif args.storage_backend == "s3":
        if not all([args.s3_access_key_id, args.s3_secret_key, args.s3_bucket_name]):
            parser.error("--s3-access-key-id, --s3-secret-key, and --s3-bucket-name are required when --storage-backend=s3")


def main():
    global connector

    args = parse_arguments()

    # Validate arguments
    validate_arguments(args)

    # Initialize SharePoint configuration
    sharepoint_config = SharePointConfig(
        client_id=args.sharepoint_client_id,
        client_secret=args.sharepoint_client_secret,
        tenant_id=args.sharepoint_tenant_id,
        site_url=args.sharepoint_site_url,
        redirect_url=args.sharepoint_redirect_url
    )

    # Initialize storage backend
    try:
        storage_backend = create_storage_backend(args.storage_backend, args)
        logger.info(f"Storage backend initialized: {storage_backend.backend_name}")
    except Exception as e:
        logger.error(f"Failed to initialize storage backend: {e}")
        return 1

    # Initialize connector
    try:
        connector = SharePointToStorageConnector(sharepoint_config, storage_backend)
        logger.info("Connector initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize connector: {e}")
        return 1

    # Start server (host hardcoded to 0.0.0.0)
    import uvicorn
    host = "0.0.0.0"
    logger.info(f"Starting server on {host}:{args.port}")
    uvicorn.run(app, host=host, port=args.port)


if __name__ == "__main__":
    main()
