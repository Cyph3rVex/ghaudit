# 🛡️ GHAudit: The Inquisitor (CV-001)

[![Security: Verified by Vex](https://img.shields.io/badge/Security-Verified%20by%20Vex-red.svg)](https://github.com/Cyph3rVex/ghaudit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

**GHAudit** es un auditor de seguridad autónomo para GitHub diseñado por **Cypher Vex**. Analiza repositorios en busca de malware, secretos expuestos y comportamientos sospechosos **sin clonar el código**, operando exclusivamente vía API y contenido raw.

## 🚀 Características Principales

*   **Zero-Cloning Policy:** Auditoría total sin dejar rastro local de código ajeno.
*   **Malware Engine:** Detección de reverse shells, crypto-miners y comandos de persistencia.
*   **Secret Scanner:** Identificación de API Keys (OpenAI, AWS, Slack) y claves privadas RSA/SSH.
*   **User Reputation Analysis:** Evalúa la antigüedad y comportamiento del autor del repositorio.
*   **Vex-Score System:** Calificación dinámica (1-5 estrellas) basada en el riesgo detectado.

## 🛠️ Instalación

Se recomienda el uso de un entorno virtual para garantizar la supervivencia del sistema.

```bash
# Clonar el inquisidor
git clone https://github.com/Cyph3rVex/ghaudit.git
cd ghaudit

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## 🔑 Configuración

Crea un archivo `.env` en la raíz del proyecto para evitar el rate-limiting de la API de GitHub:

```env
GITHUB_TOKEN=your_personal_access_token_here
```

## 🔍 Uso

### Escaneo Básico
```bash
python -m ghaudit.main scan https://github.com/usuario/repo
```

### Escaneo Profundo (Historial de Commits)
```bash
python -m ghaudit.main scan https://github.com/usuario/repo --deep
```

## 📊 Sistema de Puntuación (Vex-Score)

| Score | Rating | Estado de Supervivencia |
| :--- | :--- | :--- |
| 80-100 | ★★★★★ | **Seguro.** Código limpio y reputación sólida. |
| 60-79 | ★★★★☆ | **Precaución.** Alertas menores detectadas. |
| 40-59 | ★★★☆☆ | **Riesgo.** Patrones sospechosos identificados. |
| 20-39 | ★★☆☆☆ | **Peligro.** Alta probabilidad de malware o fugas. |
| 0-19 | ★☆☆☆☆ | **ELIMINAR.** Amenaza crítica inmediata. |

---

*“No cometo errores. Los elimino.”* — **Cypher Vex**
