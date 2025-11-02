\# Hito 3 — Microservicio con API REST, diseño por capas y registros (PassCheck API)



\## 1) Objetivo

Implementar un servicio HTTP con \*\*API REST\*\*, \*\*diseño por capas\*\* (API → Servicio → Integración), \*\*pruebas del API\*\* sin red y \*\*logging\*\*. Se muestra además el fichero de automatización (CI).



\## 2) Arquitectura por capas

\- \*\*Capa API\*\* (`app/main.py`): expone `POST /check` con FastAPI; valida el body y registra eventos.

\- \*\*Capa de Servicio\*\* (`app/service.py`): orquesta la lógica, mide latencia y retorna `{pwned, count}`.

\- \*\*Capa de Integración\*\* (`app/hibp.py`): acceso a HIBP (k-Anonymity) con `httpx`; \*\*manejo de timeout/errores\*\* y retorno seguro `0`.



\*\*Evidencia (estructura de capas):\*\*  

!\[capas](img/h3\_capas.png)



\## 3) API REST — Endpoint

\- \*\*POST\*\* `/check`  

&nbsp; \*\*Body:\*\* `{"password": "string"}` (min 1)  

&nbsp; \*\*Resp 200:\*\* `{"pwned": bool, "count": int}`  

&nbsp; \*\*Resp 422:\*\* validación por campo faltante o vacío.



\*\*Swagger (docs):\*\*  

!\[swagger](img/h3\_swagger.png)



\*\*Ejecución en Swagger (200 OK):\*\*  

!\[swagger post ok](img/h3\_swagger\_post\_ok.png)



\## 4) Pruebas del API (sin red)

\- `tests/test\_api\_endpoint.py`: 200 OK + contrato `{pwned, count}`.

\- `tests/test\_api\_422.py`: 422 por body inválido.

\- Se ejecutan sin Internet con `pytest -m "not network"` para estabilidad también en CI.



\*\*Pytest local (OK):\*\*  

!\[pytest ok](img/h3\_pytest\_ok.png)



\## 5) Logging

\- Configurado en `app/main.py` (API) y `app/service.py` (latencia) y `app/hibp.py` (errores de red/timeout).

\- Formato: `%(asctime)s %(levelname)s \[%(name)s] %(message)s` — nivel `INFO`.



\*\*Ejemplo (consola):\*\*  

!\[logging](img/h3\_logging.png)



\## 6) Automatización (fichero de construcción)

\- \*\*GitHub Actions\*\* (`.github/workflows/ci.yml`) instala dependencias y ejecuta `pytest -m "not network"` en cada push/PR.



\*\*CI YAML:\*\*  

!\[ci yaml](img/h3\_ci\_yaml.png)



\## 7) Enlaces

\- Actions: https://github.com/CarlosGutierrezR/passcheck-api/actions  

\- CI: https://github.com/CarlosGutierrezR/passcheck-api/blob/main/.github/workflows/ci.yml  

\- README: https://github.com/CarlosGutierrezR/passcheck-api/blob/main/README.md



\## 8) Entrega (Fork + PR)

\- Enlace a este documento: https://github.com/CarlosGutierrezR/passcheck-api/blob/main/docs/hito3.md  

\- \*\*URL del PR al repo de la asignatura:\*\* \_(añadir cuando se cree)\_




**Entrega:** PR #56 — https://github.com/cvillalonga/CC-25-26/pull/56
