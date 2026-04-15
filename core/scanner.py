import re
import math
from typing import List, Dict

class SecurityScanner:
    """Motor de detección de firmas maliciosas y secretos."""
    
    PATTERNS = {
        "MALWARE": {
            "reverse_shell": r"(sh|bash|nc|php|perl|python|ruby|socat)\s+-e\s+.*",
            "dangerous_curl": r"(curl|wget)\s+.*\s*\|\s*(sh|bash|python)",
            "crypto_miner": r"(stratum|xmrig|nicehash|minerd|cryptonight)",
            "persistence": r"(\.bashrc|\.profile|crontab|systemctl|launchctl)",
            "obfuscation": r"(eval\(|exec\(|base64\.b64decode|atob\(|fromCharCode)"
        },
        "SECRETS": {
            "openai": r"sk-[a-zA-Z0-9]{48}",
            "aws": r"AKIA[0-9A-Z]{16}",
            "github": r"(ghp|gho|ghu|ghs|ghr)_[a-zA-Z0-9]{36}",
            "slack": r"xox[baprs]-[0-9a-zA-Z]{10,48}",
            "private_key": r"-----BEGIN (RSA|OPENSSH|DSA|EC) PRIVATE KEY-----"
        }
    }

    @staticmethod
    def calculate_entropy(data: str) -> float:
        """Calcula la entropía de Shannon para detectar claves ofuscadas."""
        if not data: return 0
        entropy = 0
        for x in range(256):
            p_x = float(data.count(chr(x))) / len(data)
            if p_x > 0:
                entropy += - p_x * math.log(p_x, 2)
        return entropy

    def scan_content(self, content: str) -> List[Dict[str, str]]:
        findings = []
        for category, rules in self.PATTERNS.items():
            for name, pattern in rules.items():
                if re.search(pattern, content, re.IGNORECASE):
                    findings.append({"type": category, "name": name, "severity": "HIGH"})
        
        for word in re.findall(r'[A-Za-z0-9+/=]{20,}', content):
            if self.calculate_entropy(word) > 4.5:
                findings.append({"type": "SUSPICIOUS", "name": "high_entropy_string", "severity": "MEDIUM"})
                
        return findings
