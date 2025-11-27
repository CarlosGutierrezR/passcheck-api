# PassCheck API 🔐

Este proyecto implementa un sistema de verificación de contraseñas mediante **microservicios**, **Docker**, **Redis** y **FastAPI**. Está desarrollado como parte de los hitos del curso *Cloud Computing: Fundamentos e Infraestructuras*.

A continuación se muestra la documentación visual del sistema.

---

## 🚀 Arquitectura del clúster (Docker Compose)

![Compose](img/compose.png)

---

## 🐳 Arranque del clúster

![Arranque](img/arranque.png)

---

## 📦 Microservicio principal (API)

![API](img/docker.png)

---

## 📝 Microservicio Logger

![Logger](img/logger.png)

---

## 🔧 Estructura del microservicio Logger

![Micro Logger](img/micro_logger.png)

---

## 🧪 Test End-to-End del clúster

![Test Cluster](img/test_cluster_compose.png)

---

## 📄 Descripción general del proyecto

PassCheck API permite verificar si una contraseña ha sido filtrada previamente en bases de datos públicas mediante la técnica **k-Anonymity HIBP**.

Este proyecto está compuesto por:

* **API principal:** expone el endpoint `/check`.
* **Logger service:** recibe logs vía POST y los almacena en Redis.
* **Redis:** contenedor dedicado exclusivamente al almacenamiento de datos.
* **Workflow CI/CD:** pruebas automáticas y construcción de imágenes Docker.
* **Test del clúster:** levanta todo el entorno y prueba funcionamiento real.

---

## 📚 Hitos del proyecto

* [Hito 1](docs/hito1.md)
* [Hito 2](docs/hito2.md)
* [Hito 3](docs/hito3.md)
* [Hito 4](docs/hito4.md)

---

## 🛠 Tecnologías usadas

* Python 3.11
* FastAPI
* Docker / Docker Compose
* GitHub Actions
* Redis
* Pytest
* httpx

---

## 📜 Licencia

Este proyecto está bajo la licencia MIT.




