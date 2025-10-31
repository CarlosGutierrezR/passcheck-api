# app/hibp.py
import hashlib
import logging
import httpx

logger = logging.getLogger("passcheck.hibp")

def sha1_hex(s: str) -> str:
    # Se usa SHA-1 porque el endpoint de HIBP (k-Anonymity) lo exige.
    # No se usa para almacenar contraseñas.  # codeql[py/weak-sensitive-data-hashing]
    return hashlib.sha1(s.encode("utf-8")).hexdigest().upper()

def pwned_count(password: str) -> int:
    """
    Devuelve el número de apariciones de la contraseña en HIBP.
    En caso de error de red/timeout, **regresa 0** y loguea el fallo.
    """
    full = sha1_hex(password)
    prefix, suffix = full[:5], full[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    headers = {"User-Agent": "passcheck-api/0.2 (+github.com/CarlosGutierrezR/passcheck-api)"}

    try:
        with httpx.Client(timeout=10.0, headers=headers) as client:
            r = client.get(url)
            r.raise_for_status()
            for line in r.text.splitlines():
                h, cnt = line.split(":")
                if h.strip().upper() == suffix:
                    return int(cnt)
            return 0
    except Exception as e:
        # No propagamos: devolvemos 0 para que la API responda 200 con count=0
        logger.warning("HIBP request failed (%s): %s", type(e).__name__, e)
        return 0
