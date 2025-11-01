# app/service.py
from time import perf_counter
import logging
from app.hibp import pwned_count

logger = logging.getLogger("passcheck.service")

def check_password(password: str) -> dict:
    """
    Capa de servicio: orquesta la lógica de negocio.
    - Mide latencia de la consulta a HIBP.
    - Devuelve un dict estable para el API.
    """
    t0 = perf_counter()
    try:
        count = pwned_count(password)
        pwned = count > 0
        return {"pwned": pwned, "count": count}
    finally:
        elapsed = (perf_counter() - t0) * 1000.0
        logger.info("check_password completed in %.2f ms", elapsed)
