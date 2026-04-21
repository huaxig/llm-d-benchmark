"""Base client interface for result store storage backends."""

from abc import ABC, abstractmethod

class StorageClient(ABC):
    """Abstract base class for all storage clients.
    
    Operates purely on URIs and local paths, without knowledge of application logic.
    """

    @abstractmethod
    def ls(self, uri: str) -> list[str]:
        """Lists object names under the given URI."""
        pass

    @abstractmethod
    def push(self, uri: str, local_dir: str) -> int:
        """Pushes a local directory to the remote URI. Returns count of uploaded files."""
        pass

    @abstractmethod
    def exists(self, uri: str) -> bool:
        """Checks if the URI exists."""
        pass

    @abstractmethod
    def pull(self, uri: str, dest_dir: str) -> int:
        """Pulls objects from URI to dest_dir. Returns count of downloaded files."""
        pass

def get_storage_client(uri: str) -> StorageClient:
    """Factory to return appropriate StorageClient based on URI scheme."""
    if uri.startswith("gs://"):
        from llmdbenchmark.result_store.gcs import GCSClient
        return GCSClient()
    raise ValueError(f"Unsupported storage URI scheme: {uri}")

def get_fallback_client(primary_client: StorageClient) -> StorageClient:
    """Returns the appropriate fallback client for a given primary client."""
    from llmdbenchmark.result_store.gcs import GCSClient
    if isinstance(primary_client, GCSClient):
        from llmdbenchmark.result_store.gcs_proxy import GCSProxyClient
        return GCSProxyClient()
    return None
