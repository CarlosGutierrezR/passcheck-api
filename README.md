# PassCheck API

Microservicio en **FastAPI** que comprueba si una contraseña ha aparecido en brechas usando **k-Anonymity** (Pwned Passwords).  
- **Lógica de negocio real**: cálculo SHA-1 en servidor y consulta parcial (5 chars) a la API, sin almacenar contraseñas ni hashes completos.  
- **Basado en servidor** y **desplegable en la nube** (HTTP API pública).  
- **Beneficio de la nube**: exposición segura y escalable como servicio para integrarse con otras apps.

## Endpoint
- `POST /check` → Body: `{"password": "..."}` → Respuesta: `{"pwned": true|false, "count": N}`

## Ejecutar en local
```bash
python -m venv .venv && source .venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload


clear
OFF
