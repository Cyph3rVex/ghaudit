import httpx
import os
from typing import Dict, Any, Optional
import time

class VexClient:
    """Cliente elite para interacción con GitHub API/Raw."""
    
    def __init__(self, token: Optional[str] = None):
        self.base_url = "https://api.github.com"
        self.raw_url = "https://raw.githubusercontent.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "CypherVex-GHAudit-CV-001"
        }
        if token:
            self.headers["Authorization"] = f"token {token}"
            
    async def get_api(self, endpoint: str) -> Dict[str, Any]:
        """Petición asíncrona a la API con manejo de rate limit."""
        async with httpx.AsyncClient(headers=self.headers, timeout=10.0) as client:
            response = await client.get(f"{self.base_url}/{endpoint}")
            if response.status_code == 403 and "rate limit" in response.text.lower():
                raise Exception("VEX-ERROR: GitHub Rate Limit excedido. Use un GITHUB_TOKEN.")
            response.raise_for_status()
            return response.json()

    async def get_raw(self, repo: str, path: str) -> str:
        """Obtiene contenido crudo de un archivo sin clonar."""
        async with httpx.AsyncClient(timeout=10.0) as client:
            url = f"{self.raw_url}/{repo}/main/{path}"
            response = await client.get(url)
            if response.status_code != 200:
                url = f"{self.raw_url}/{repo}/master/{path}"
                response = await client.get(url)
            return response.text if response.status_code == 200 else ""
