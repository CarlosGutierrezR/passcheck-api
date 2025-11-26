import time
import subprocess
import pytest
import httpx


@pytest.mark.network
def test_compose_cluster_end_to_end():
    # Apagar cualquier clúster previo
    subprocess.run(["docker", "compose", "down", "-v"], check=False)

    # Levantar clúster
    subprocess.run(["docker", "compose", "up", "-d", "--build"], check=True)

    # Esperar a que arranquen los contenedores
    time.sleep(10)

    # --- 1) Probar API principal ---
    with httpx.Client(timeout=15.0) as client:
        r = client.post(
            "http://localhost:8000/check",
            json={"password": "password"},
        )
    assert r.status_code == 200
    data = r.json()
    assert set(data.keys()) == {"pwned", "count"}

    # --- 2) Probar microservicio logger ---
    with httpx.Client(timeout=15.0) as client:
        r2 = client.post(
            "http://localhost:9000/log",
            json={"message": "cluster test OK"},
        )
    assert r2.status_code == 200
    assert r2.json()["status"] == "ok"
