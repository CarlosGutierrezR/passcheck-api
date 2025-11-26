# Hito 4 — Composición de Servicios

## Cloud Computing: Fundamentos e Infraestructuras

### Carlos Alberto Gutiérrez Rondón

---

# 1. Introducción

En este hito se construye un entorno completo basado en **contenedores** utilizando **Docker Compose**, cumpliendo los requisitos del proyecto:

* Implementar **múltiples servicios** que trabajen de forma coordinada.
* Incorporar un contenedor cuyo propósito sea **almacenar datos exclusivamente**.
* Documentar la arquitectura, configuración, ejecución y pruebas.
* Crear un **test de clúster** que valide el funcionamiento global.
* Opcional pero recomendado: implementar un workflow que construya imágenes del proyecto.

Este hito amplía y consolida la arquitectura definida en los hitos anteriores.

---

# 2. Arquitectura general del clúster

El clúster implementado está compuesto por **tres servicios**:

| Servicio   | Rol                     | Tecnología       | Descripción                                 |
| ---------- | ----------------------- | ---------------- | ------------------------------------------- |
| **api**    | Microservicio principal | FastAPI (Python) | Expone `/check` y ejecuta consultas a HIBP. |
| **logger** | Microservicio auxiliar  | FastAPI + Redis  | Recibe logs y los almacena.                 |
| **cache**  | Contenedor de datos     | Redis 7          | Almacena logs y datos de caché.             |

### ✔ Cumplimiento del requisito académico:

> "Uno de los contenedores debe tener como contenido exclusivo almacenar datos"

Ese contenedor es **Redis**, configurado únicamente para persistencia.

---

# 3. Docker Compose del clúster

Archivo implementado: `compose.yaml`

```yaml
version: "3.9"

services:
  api:
    build: .
    image: ghcr.io/carlosgutierrezr/passcheck-api:latest
    container_name: passcheck-api
    ports:
      - "8000:8000"
    depends_on:
      - cache
      - logger

  cache:
    image: redis:7-alpine
    container_name: passcheck-cache
    command: ["redis-server", "--save", "60", "1", "--loglevel", "warning"]
    volumes:
      - redis-data:/data

  logger:
    build: ./logger
    image: ghcr.io/carlosgutierrezr/passcheck-logger:latest
    container_name: passcheck-logger
    ports:
      - "9000:9000"
    environment:
      - "REDIS_URL=redis://cache:6379/0"
    depends_on:
      - cache

volumes:
  redis-data:
```

### Justificación técnica

* **Redis** es ideal como contenedor de datos: rápido, ligero y persistente.
* **FastAPI** ofrece rendimiento, validación automática y compatibilidad con OpenAPI.
* **Docker Compose** facilita la coordinación entre servicios y la creación de redes internas.
* La definición de **volúmenes** garantiza persistencia de logs.

---

# 4. Microservicio adicional: `logger`

Este servicio demuestra la existencia de múltiples microservicios cooperando.

Archivo: `logger/main.py`

```python
import logging
import os
from fastapi import FastAPI
from pydantic import BaseModel
import redis

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [logger] %(message)s",
)

REDIS_URL = os.getenv("REDIS_URL", "redis://cache:6379/0")
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

app = FastAPI(title="PassCheck Logger", version="0.1.0")

class LogEntry(BaseModel):
    level: str = "INFO"
    message: str

@app.post("/log")
def log(entry: LogEntry):
    level = getattr(logging, entry.level.upper(), logging.INFO)
    logging.log(level, entry.message)
    r.lpush("passcheck:logs", f"{entry.level.upper()} {entry.message}")
    return {"status": "ok"}
```

---

# 5. Dockerfile del microservicio logger

Archivo: `logger/Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py main.py

EXPOSE 9000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
```

---

# 6. Workflow de construcción de imágenes (GHCR)

Archivo: `.github/workflows/docker.yml`

```yaml
name: docker

on:
  push:
    branches: [ main ]
  workflow_dispatch:

permissions:
  contents: read
  packages: write

jobs:
  build-and-push:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build & push API image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ghcr.io/carlosgutierrezr/passcheck-api:latest

      - name: Build & push Logger image
        uses: docker/build-push-action@v5
        with:
          context: ./logger
          push: true
          tags: |
            ghcr.io/carlosgutierrezr/passcheck-logger:latest
```

---

# 7. Test del clúster

Implementado en: `tests/test_cluster_compose.py`

```python
import time
import subprocess
import pytest
import httpx

@pytest.mark.network
def test_compose_cluster_end_to_end():
    subprocess.run(["docker", "compose", "down", "-v"], check=False)
    subprocess.run(["docker", "compose", "up", "-d", "--build"], check=True)
    time.sleep(10)

    with httpx.Client(timeout=15.0) as client:
        r = client.post(
            "http://localhost:8000/check",
            json={"password": "password"},
        )
    assert r.status_code == 200
    data = r.json()
    assert set(data.keys()) == {"pwned", "count"}

    with httpx.Client(timeout=15.0) as client:
        r2 = client.post(
            "http://localhost:9000/log",
            json={"message": "cluster test OK"},
        )
    assert r2.status_code == 200
    assert r2.json()["status"] == "ok"
```

### Resultado real de la ejecución

```
1 passed in 21.75s
```

---

# 8. Comprobación manual

### API principal:

[http://localhost:8000/docs](http://localhost:8000/docs)

### Microservicio logger:

[http://localhost:9000/docs](http://localhost:9000/docs)

---

# 9. Conclusión

El hito 4 demuestra:

* La correcta **composición de microservicios**.
* El uso de **Redis** como contenedor exclusivo de datos.
* La definición de **Docker Compose** con dependencias y redes internas.
* La integración con **Docker Hub / GHCR** mediante workflows.
* Un **test funcional de clúster** end-to-end.

El sistema queda completamente preparado para despliegues y ampliaciones futuras.

---


