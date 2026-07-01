"""
Abstract storage backend interface.

Storage backends implement this interface to provide file upload capabilities.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class StorageBackend(ABC):
    """Abstract base class for storage backends"""

    @abstractmethod
    def upload_file(
        self,
        content: bytes,
        key: str,
        metadata: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Upload a file to storage.

        Args:
            content: File content as bytes
            key: Destination key/path in storage
            metadata: Optional metadata to attach

        Returns:
            Dict with at least: key, bucket, size_bytes
        """
        pass

    @abstractmethod
    def get_location_info(self) -> Dict[str, str]:
        """
        Get storage location information.

        Returns:
            Dict with backend-specific location info (e.g., bucket, endpoint)
        """
        pass

    @property
    @abstractmethod
    def backend_name(self) -> str:
        """Return the name of this storage backend"""
        pass
