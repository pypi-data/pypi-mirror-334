import logging
from api_client import WetroCloudClient
from rag import WetroRAG
from toolkit import WetroTools


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("wetrocloud")

class WetroCloud:
    """
    Client that allows setting the API key only once.
    
    Usage:
        client = WetroCloud(api_key="your_api_key")
        rag_client = client.rag
        tools_client = client.tools
    """
    def __init__(
            self, 
            api_key: str, 
            base_url: str = "https://api.wetrocloud.com", 
            timeout: int = 30
        ):
        self._client = WetroCloudClient(api_key, base_url, timeout)
        self.rag = WetroRAG(client=self._client)
        self.tools = WetroTools(client=self._client)

if __name__ == "__main__":
    pass
    