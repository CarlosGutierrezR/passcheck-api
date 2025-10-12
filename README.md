<div align="center">

# PassCheck API

Microservicio en **FastAPI** que verifica si una contraseña apareció en brechas públicas usando **k-Anonymity** (Pwned Passwords).  
Privado por diseño: no almacena contraseñas ni hashes completos.

[![CI](https://github.com/CarlosGutierrezR/passcheck-api/actions/workflows/ci.yml/badge.svg)](https://github.com/CarlosGutierrezR/passcheck-api/actions/workflows/ci.yml)
[![CodeQL](https://github.com/CarlosGutierrezR/passcheck-api/actions/workflows/codeql.yml/badge.svg)](https://github.com/CarlosGutierrezR/passcheck-api/actions/workflows/codeql.yml)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

</div>

> **¿Por qué en la nube?** Para exponerlo como **servicio HTTP** reutilizable, escalable y observable, integrable en múltiples apps.

---

<details>
<summary><strong>Tabla de contenidos</strong></summary>

- [Características](#características)
- [Arquitectura](#arquitectura)
- [Requisitos](#requisitos)
- [Empezar (Local)](#empezar-local)
- [Tests](#tests)
- [Docker](#docker)
- [API](#api)
- [Seguridad](#seguridad)
- [CI/CD](#cicd)
- [Estructura del repo](#estructura-del-repo)
- [Roadmap](#roadmap)
- [Doc del Hito](#doc-del-hito)
- [Licencia](#licencia)

</details>

---

## Características

- 🔒 **Privacidad**: SHA-1 solo para el prefijo (k-Anonymity), nada se persiste.  
- ⚡ **Simple**: un endpoint `POST /check`.  
- 🧪 **Calidad**: tests unitarios y de integración (marca `@network`).  
- 🛡️ **Seguridad**: CodeQL, Secret Scanning, Dependabot.  
- 🐳 **Contenedor**: `Dockerfile` minimal listo para deploy.

---

## Arquitectura

```mermaid
sequenceDiagram
    autonumber
    participant C as Cliente
    participant API as PassCheck API (FastAPI)
    participant H as HIBP (Pwned Passwords)
    C->>API: POST /check {"password":"..."}
    API->>API: SHA1(password) → FULL_HASH
    API->>H: GET /range/PREFIX (5 chars)
    H-->>API: SUFFIX:COUNT\nSUFFIX:COUNT...
    API->>API: Buscar SUFFIX de FULL_HASH en la lista
    API-->>C: { "pwned": bool, "count": N }
Requisitos
Windows (PowerShell/Git Bash) o Linux/macOS

Python 3.11+ y Git

(Opcional) Docker

Empezar (Local)
bash
Copiar código
# 1) Clonar
git clone git@github.com:CarlosGutierrezR/passcheck-api.git
cd passcheck-api

# 2) Entorno
# Windows (PowerShell):  .\.venv\Scripts\Activate.ps1
# Git Bash:              source .venv/Scripts/activate
py -3.11 -m venv .venv
source .venv/Scripts/activate

# 3) Dependencias
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 4) Levantar API
python -m uvicorn app.main:app --reload
# → http://127.0.0.1:8000/docs
Tests
bash
Copiar código
# Unit (sin red) — lo que corre el CI
python -m pytest -q -m "not network"

# Integración (usa Internet)
python -m pytest -q -m network
La marca network está registrada en pytest.ini y se excluye del CI.

Docker
bash
Copiar código
# Build
docker build -t passcheck-api:latest .

# Run
docker run -p 8000:8000 passcheck-api:latest
# → http://127.0.0.1:8000/docs
API
POST /check
Body

json
Copiar código
{ "password": "string" }
200 OK

json
Copiar código
{ "pwned": true, "count": 12345 }
422 Unprocessable Entity — JSON inválido o campo ausente
500 Internal Server Error — fallo externo (timeout/HIBP no disponible)

curl

bash
Copiar código
curl -X POST http://127.0.0.1:8000/check \
  -H "Content-Type: application/json" \
  -d "{\"password\":\"password\"}"
Seguridad
SHA-1 se usa intencionalmente porque lo exige el endpoint de HIBP para k-Anonymity.
No se usa para almacenamiento/autenticación. Recomendado para credenciales: Argon2 / bcrypt / scrypt.
(CodeQL suprimido con comentario justificado en app/hibp.py.)

HTTPX con timeout y User-Agent explícito.

Secret scanning habilitado en el repo.

CI/CD
CI: pytest -m "not network" en push/PR.

CodeQL: análisis estático (push/PR + cron).

Dependabot: actualizaciones semanales para pip.

Badges arriba 👆

Estructura del repo
bash
Copiar código
passcheck-api/
  app/
    __init__.py
    hibp.py          # lógica HIBP k-Anonymity
    main.py          # FastAPI app
  tests/
    test_api.py
  .github/
    workflows/
      ci.yml
      codeql.yml
    dependabot.yml
  docs/
    hito1.md
  Dockerfile
  pytest.ini
  requirements.txt
  README.md
  LICENSE
Roadmap
 GET /health (healthcheck)

 Rate limiting básico

 Métricas Prometheus

 Imagen multi-stage aún más pequeña

Doc del Hito
Toda la evidencia del Hito 1:
➡️ docs/hito1.md

Licencia
MIT — ver LICENSE.
