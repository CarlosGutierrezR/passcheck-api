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
