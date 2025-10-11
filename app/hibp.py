import hashlib
import httpx

def sha1_hex(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest().upper()

def pwned_count(password: str) -> int:
    full = sha1_hex(password)
    prefix, suffix = full[:5], full[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    headers = {"User-Agent": "passcheck-api/0.1 (+github.com/CarlosGutierrezR)"}
    with httpx.Client(timeout=10.0), headers=headers) as client:
        r = client.get(url)
        r.raise_for_status()
        for line in r.text.splitlines():
            h, cnt = line.split(":")
            if h.strip().upper() == suffix:
                return int(cnt)
    return 0
