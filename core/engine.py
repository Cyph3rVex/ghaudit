from .scanner import SecurityScanner
from ..api.client import VexClient
from typing import Dict, Any, List
from datetime import datetime

class AuditEngine:
    """Orquestador del sistema de puntuación Vex-Score."""
    
    def __init__(self, client: VexClient):
        self.client = client
        self.scanner = SecurityScanner()
        self.score = 100
        self.alerts = []

    def penalize(self, points: int, reason: str):
        self.score = max(0, self.score - points)
        self.alerts.append(reason)

    async def audit_user(self, username: str):
        try:
            data = await self.client.get_api(f"users/{username}")
            created_at = datetime.strptime(data['created_at'], "%Y-%m-%dT%H:%M:%SZ")
            days_old = (datetime.now() - created_at).days
            
            if days_old < 7: self.penalize(40, "Cuenta extremadamente nueva (< 1 semana)")
            elif days_old < 30: self.penalize(20, "Cuenta nueva (< 1 mes)")
            
            if data.get('followers', 0) < 2 and data.get('public_repos', 0) < 3:
                self.penalize(15, "Perfil sospechoso (pocos seguidores/repos)")
        except Exception as e:
            self.alerts.append(f"Error auditando usuario: {str(e)}")

    async def audit_repo(self, repo_path: str):
        files_to_scan = [".env", "requirements.txt", "package.json", "setup.py", "Dockerfile"]
        
        for file in files_to_scan:
            try:
                content = await self.client.get_raw(repo_path, file)
                if content:
                    findings = self.scanner.scan_content(content)
                    for f in findings:
                        weight = 30 if f['type'] == "MALWARE" else 20
                        self.penalize(weight, f"Detectado {f['name']} en {file}")
            except Exception:
                continue

    def get_stars(self) -> str:
        if self.score >= 80: return "★★★★★"
        if self.score >= 60: return "★★★★☆"
        if self.score >= 40: return "★★★☆☆"
        if self.score >= 20: return "★★☆☆☆"
        return "★☆☆☆☆"
