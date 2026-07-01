# SharePoint to Storage Connector

A Python server that transfers files from SharePoint to various storage backends.

## Features

- **No hardcoded tokens**: Uses OAuth 2.0 Client Credentials Flow - credentials passed at startup only
- **Simple API**: Single endpoint to transfer files by path
- **Auto token refresh**: Transparently handles access token expiration (~1 hour lifecycle)
- **Pluggable storage backends**: Support for IBM COS, S3, and extensible for others
- **Configurable**: All settings passed via CLI arguments or environment variables

## Architecture

```
┌─────────────────┐          ┌──────────────────┐         ┌─────────────────┐
│   SharePoint    │────────->│  Connector Server│────────>│  Storage Backend│
│                 │ Graph API│                  │         │  (COS / S3 /...)│
└─────────────────┘          └──────────────────┘         └─────────────────┘
                                   ▲
                                   │
                                   ▼
                            ┌─────────────┐
                            │   Client    │
                            │  (HTTP API) │
                            └─────────────┘
```

## Storage Backends

| Backend | Description | Requirements |
|---------|-------------|--------------|
| `cos` | IBM Cloud Object Storage | `pip install -r requirements-cos.txt` |
| `s3` | AWS S3 / MinIO / S3-compatible | `pip install -r requirements-s3.txt` |

## Prerequisites

### SharePoint App Registration

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **App registrations** → **New registration**
3. Register a new application with:
   - Supported account types: "Accounts in this organizational directory only"
   - Redirect URI: `http://localhost` (any valid URI for client credentials flow)

4. After registration, note:
   - **Application (client) ID** → `--sharepoint-client-id`
   - **Directory (tenant) ID** → `--sharepoint-tenant-id`

5. Go to **Certificates & secrets** → **New client secret**:
   - Create a new secret and copy the **Value** → `--sharepoint-client-secret`

6. Go to **API permissions** → **Add a permission** → **Microsoft Graph**:
   - Select **Application permissions** (NOT delegated)
   - Add: `Sites.Read.All` and `Files.Read.All`
   - Click **Grant admin consent** for your organization

### IBM COS Setup (if using `cos` backend)

1. Create an IBM Cloud Object Storage instance
2. Create a bucket in the desired region
3. Generate **HMAC Credentials** or **Service Credentials**:
   - Get the **API Key** → `--cos-api-key`
   - Get the **Endpoint URL** → `--cos-endpoint`
   - Note your **Bucket Name** → `--cos-bucket-name`

### S3 Setup (if using `s3` backend)

1. Create an S3 bucket (or use MinIO/Ceph/etc.)
2. Get access credentials:
   - **Access Key ID** → `--s3-access-key-id`
   - **Secret Access Key** → `--s3-secret-key`
   - **Bucket Name** → `--s3-bucket-name`

## Installation

```bash
# Install with core dependencies only
uv sync

# Install with IBM COS support
uv sync --extra cos

# Install with S3 support
uv sync --extra s3

# Install with all backends
uv sync --extra all
```

## Usage

### Start with IBM COS

```bash
python main.py \
    --sharepoint-client-id YOUR_CLIENT_ID \
    --sharepoint-client-secret YOUR_CLIENT_SECRET \
    --sharepoint-tenant-id YOUR_TENANT_ID \
    --sharepoint-site-url "https://yourtenant.sharepoint.com/sites/yoursite" \
    --storage-backend cos \
    --cos-api-key YOUR_COS_API_KEY \
    --cos-endpoint "https://s3.direct.us-south.cloud-object-storage.appdomain.cloud" \
    --cos-bucket-name your-bucket-name
```

### Start with S3

```bash
python main.py \
    --sharepoint-client-id YOUR_CLIENT_ID \
    --sharepoint-client-secret YOUR_CLIENT_SECRET \
    --sharepoint-tenant-id YOUR_TENANT_ID \
    --sharepoint-site-url "https://yourtenant.sharepoint.com/sites/yoursite" \
    --storage-backend s3 \
    --s3-access-key-id YOUR_ACCESS_KEY \
    --s3-secret-key YOUR_SECRET_KEY \
    --s3-bucket-name your-bucket-name
```

### Start with MinIO (S3-compatible)

```bash
python main.py \
    --sharepoint-client-id YOUR_CLIENT_ID \
    --sharepoint-client-secret YOUR_CLIENT_SECRET \
    --sharepoint-tenant-id YOUR_TENANT_ID \
    --sharepoint-site-url "https://yourtenant.sharepoint.com/sites/yoursite" \
    --storage-backend s3 \
    --s3-access-key-id MINIO_ACCESS_KEY \
    --s3-secret-key MINIO_SECRET_KEY \
    --s3-endpoint-url "http://localhost:9000" \
    --s3-bucket-name your-bucket-name
```

### API Endpoints

#### Health Check
```bash
curl http://localhost:8000/health
```

#### List Files in SharePoint Folder
```bash
curl http://localhost:8000/api/v1/list/"Shared Documents/folder"
```

#### Transfer a File

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/transfer \
    -H "Content-Type: application/json" \
    -d '{
        "sharepoint_path": "Shared Documents/folder/file.pdf",
        "storage_key": "uploaded/file.pdf",
        "preserve_path": true
    }'
```

**Response (COS backend):**
```json
{
    "success": true,
    "sharepoint_path": "Shared Documents/folder/file.pdf",
    "storage_key": "uploaded/file.pdf",
    "storage_backend": "ibm-cos",
    "storage_location": {
        "backend": "ibm-cos",
        "bucket": "your-bucket-name",
        "endpoint": "https://s3.direct.us-south.cloud-object-storage.appdomain.cloud"
    },
    "size_bytes": 12345,
    "transferred_at": "2026-07-01T10:30:00"
}
```

**Response (S3 backend):**
```json
{
    "success": true,
    "sharepoint_path": "Shared Documents/folder/file.pdf",
    "storage_key": "uploaded/file.pdf",
    "storage_backend": "s3",
    "storage_location": {
        "backend": "s3",
        "bucket": "your-bucket-name",
        "region": "us-east-1"
    },
    "size_bytes": 12345,
    "transferred_at": "2026-07-01T10:30:00"
}
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `sharepoint_path` | Yes | Path to file in SharePoint (relative to site root) |
| `storage_key` | No | Destination key in storage (default: preserves original filename) |
| `preserve_path` | No | Whether to preserve folder structure (default: true) |

## Purpose

This server **replaces** the SharePoint connector functionality that GCP Data Fusion provides. Instead of configuring a connector within Data Fusion, you deploy this standalone server and call its API directly to transfer files from SharePoint to your chosen storage backend.

## How It Works

### OAuth 2.0 Flow (Client Credentials)

```
Connector Server                    Azure AD
     │                                  │
     │  client_id + client_secret       │
     │────────────────────────────────>│
     │                                  │
     │<─────────────────────────────────│
     │     access_token + expires_in    │
     │                                  │
```

1. Server requests access token using client credentials
2. Azure AD returns access token (expires in ~1 hour)
3. Server uses token to access SharePoint via Microsoft Graph API
4. Server automatically refreshes token 5 minutes before expiry

### File Transfer Process

```
1. Download file from SharePoint via Graph API
   GET https://graph.microsoft.com/v1.0/sites/{site-id}/drive/root:/{path}

2. Stream content to memory

3. Upload to storage backend via selected storage interface
   PUT {storage-endpoint}/{bucket-name}/{key}
```

## Extending with New Storage Backends

To add a new storage backend:

1. Create a new file in `storage/your_backend.py`
2. Import the base class: `from .base import StorageBackend`
3. Implement your backend class inheriting from `StorageBackend`
4. Add the backend type to `main.py`'s `create_storage_backend()` function
5. Create a requirements file `requirements-your_backend.txt`

Example:
```python
# storage/azure.py
from .base import StorageBackend

class AzureStorage(StorageBackend):
    @property
    def backend_name(self) -> str:
        return "azure-blob"

    def upload_file(self, content: bytes, key: str, metadata=None):
        # Your implementation
        pass

    def get_location_info(self):
        # Your implementation
        pass
```

## Docker Deployment

### IBM COS
```bash
docker build -t sharepoint-connector .
docker run -p 8000:8000 \
    -e SHAREPOINT_CLIENT_ID=$SP_ID \
    -e SHAREPOINT_CLIENT_SECRET=$SP_SECRET \
    -e SHAREPOINT_TENANT_ID=$SP_TENANT \
    -e SHAREPOINT_SITE_URL=$SP_SITE \
    -e STORAGE_BACKEND=cos \
    -e COS_API_KEY=$COS_KEY \
    -e COS_ENDPOINT=$COS_ENDPOINT \
    -e COS_BUCKET_NAME=$COS_BUCKET \
    sharepoint-connector
```

### S3
```bash
docker run -p 8000:8000 \
    -e SHAREPOINT_CLIENT_ID=$SP_ID \
    -e SHAREPOINT_CLIENT_SECRET=$SP_SECRET \
    -e SHAREPOINT_TENANT_ID=$SP_TENANT \
    -e SHAREPOINT_SITE_URL=$SP_SITE \
    -e STORAGE_BACKEND=s3 \
    -e S3_ACCESS_KEY_ID=$S3_KEY \
    -e S3_SECRET_KEY=$S3_SECRET \
    -e S3_BUCKET_NAME=$S3_BUCKET \
    sharepoint-connector
```

## Troubleshooting

### Common Errors

**401 Unauthorized**
- Check client credentials are correct
- Ensure admin consent was granted for API permissions

**404 File Not Found**
- Verify the file path is correct relative to site root
- Use the `/list` endpoint to browse available files

**403 Forbidden**
- Verify API permissions include `Sites.Read.All` and `Files.Read.All`
- Check admin consent was granted

**Storage Authentication Failed**
- For COS: Verify API key and endpoint URL
- For S3: Verify access key, secret key, and bucket name

## Project Structure

```
sharepoint-cos-connector/
├── main.py                   # Main server application
├── storage/                  # Storage backend implementations
│   ├── __init__.py
│   ├── base.py              # Abstract base class
│   ├── cos.py               # IBM COS implementation
│   └── s3.py                # S3 implementation
├── pyproject.toml           # Project dependencies with extras
├── docker-compose.yml
├── Dockerfile
└── README.md
```
