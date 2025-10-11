PassCheck API






Microservicio en FastAPI que comprueba si una contraseña ha aparecido en brechas públicas usando el método de k-Anonymity de Pwned Passwords.
No almacena contraseñas ni hashes completos. Ideal para integrarlo como servicio HTTP en aplicaciones web/desktop o pipelines de seguridad.

Por qué en la nube: exposición como API pública, escalado sencillo, observabilidad y actualización continua (CI/CD).

Tabla de Contenidos

Características

Arquitectura

Stack

Empezar (Local)

Tests

Docker

API

Despliegue

Seguridad

CI/CD

Estructura del Repo

Roadmap

Contribuir

Licencia

Créditos

Doc del Hito

Características

🔒 Privacidad: el hash SHA-1 solo se usa en memoria para consultar el rango (k-Anonymity).

⚡ Rápido y simple: un único endpoint POST /check.

🧪 Tests unitarios y de integración (marca @network).

🛡️ Calidad y seguridad: CI, CodeQL, Dependabot, Secret scanning.

🐳 Listo para contenedor: Dockerfile minimal.

Arquitectura

Flujo (k-Anonymity)

Cliente -> PassCheck API (FastAPI)
        -> SHA1(password) en servidor
        -> Consulta a HIBP: GET /range/<PREFIX_5C>
        <- Respuesta: pares <SUFFIX>:COUNT
        -> Búsqueda de SUFFIX local
        <- Respuesta final: { pwned: bool, count: int }


No se loggea la contraseña ni el hash completo. Solo se consulta el prefijo (5 caracteres) del SHA-1.

Stack

Backend: Python 3.11+, FastAPI, httpx, Uvicorn

Testing: pytest

CI/CD: GitHub Actions (tests + CodeQL), Dependabot

Contenedor: Docker (Debian slim)

Empezar (Local)
Requisitos

Python 3.11+ (con py launcher en Windows, recomendado)

Git

Pasos
# clonar
git clone git@github.com:CarlosGutierrezR/passcheck-api.git
cd passcheck-api

# entorno virtual
py -3.11 -m venv .venv
source .venv/Scripts/activate   # Git Bash/PowerShell; en CMD: .venv\Scripts\activate.bat

# instalar deps
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# levantar API
python -m uvicorn app.main:app --reload
# abrir http://127.0.0.1:8000/docs

Tests

Unit (sin red, lo mismo que corre el CI):

python -m pytest -q -m "not network"


Integración (usa Internet):

python -m pytest -q -m network


El marcador network está registrado en pytest.ini y se excluye en CI para evitar falsos fallos por red.

Docker
# build
docker build -t passcheck-api:latest .

# run
docker run -p 8000:8000 passcheck-api:latest
# abrir http://127.0.0.1:8000/docs

API
POST /check

Body

{ "password": "string" }


Response 200

{ "pwned": true, "count": 12345 }


Ejemplo con curl

curl -X POST http://127.0.0.1:8000/check \
  -H "Content-Type: application/json" \
  -d "{\"password\":\"password\"}"

Despliegue
Render (usando Dockerfile)

Conecta el repo y crea un Web Service.

Runtime: Docker (Render detecta el Dockerfile).

Expone el puerto 8000.

Deploy.

Fly.io (alternativa rápida)
fly launch --now   # detecta Dockerfile

Seguridad

Uso de SHA-1: requerido por la API Pwned Passwords para k-Anonymity.
No se almacena ni usa para autenticación. Para almacenamiento de contraseñas: Argon2 / bcrypt / scrypt.
(CodeQL está suprimido con comentario justificado en app/hibp.py).

Headers/Timeouts: cliente httpx con timeout y User-Agent explícito.

Secret scanning habilitado en el repo.

CI/CD

CI: pytest -m "not network" en cada push/PR.

CodeQL: análisis estático semanal y en cada push.

Dependabot: revisa dependencias pip semanalmente.

Badges arriba del README 👆

Estructura del Repo
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

 Healthcheck (GET /health)

 Rate limiting básico

 Métricas Prometheus

 Contenedor multi-stage aún más pequeño

Contribuir

Las contribuciones son bienvenidas. Abre un issue/PR siguiendo commits descriptivos.
Para cambios funcionales, añade tests.

Licencia

MIT — ver LICENSE.

Créditos

Have I Been Pwned – Pwned Passwords (k-Anonymity)

Doc del Hito

Toda la evidencia del Hito 1 está en:
➡️ docs/hito1.md

## Seguridad
Este proyecto usa **SHA-1** únicamente para el método **k-Anonymity** de *Pwned Passwords*.
No se almacena ni usa para autenticación. Para almacenamiento de contraseñas se recomiendan **Argon2/bcrypt/scrypt**.
