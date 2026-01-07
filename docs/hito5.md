# Hito 5 – Despliegue de la aplicación en un entorno PaaS

## 1. Introducción

En este quinto hito he realizado el despliegue de la aplicación **PassCheck API** en un entorno **PaaS (Platform as a Service)**, con el objetivo de publicar el servicio en un entorno cloud real y accesible desde Internet.

El propósito de este hito es validar que la aplicación desarrollada en los hitos anteriores no solo funciona en local, sino que es **desplegable, operativa y verificable en un entorno de producción**, siguiendo prácticas habituales en entornos profesionales.

---

## 2. Descripción de la aplicación desplegada

La aplicación desplegada es **PassCheck API**, una API REST desarrollada con **FastAPI** que permite comprobar si una contraseña ha aparecido en brechas de seguridad conocidas, utilizando el servicio externo *Have I Been Pwned*.

La API expone los siguientes endpoints principales:

- `POST /check`: comprueba si una contraseña ha sido comprometida.
- `GET /health`: endpoint de estado para verificar que el servicio está operativo.

Además, la aplicación genera automáticamente documentación **OpenAPI** accesible mediante Swagger UI.

---

## 3. Plataforma PaaS seleccionada

Para el despliegue se ha seleccionado **Render** como plataforma PaaS.

Esta elección se ha basado en los siguientes criterios:

- Soporte nativo para aplicaciones contenarizadas con **Docker**.
- Integración directa con **GitHub** para despliegue automático.
- Disponibilidad de un **plan gratuito**, adecuado para proyectos académicos.
- Facilidad de configuración y monitorización.
- Posibilidad de desplegar el servicio en una región europea (**Frankfurt – EU Central**).

---

## 4. Proceso de despliegue

### 4.1 Preparación de la aplicación

Antes del despliegue se realizaron ajustes para garantizar la compatibilidad con un entorno PaaS:

- Uso de **puerto dinámico** proporcionado por la plataforma.
- Definición de un endpoint `/health` para monitorización.
- Ejecución de la aplicación mediante **Uvicorn** dentro de un contenedor Docker.

La imagen Docker fue validada previamente en local para asegurar su correcto funcionamiento.

---

### 4.2 Despliegue en Render

El despliegue se realizó conectando el repositorio GitHub a Render y configurando un **Web Service** con runtime Docker.  
La plataforma se encargó automáticamente de la construcción de la imagen y del despliegue del servicio.

**Evidencia del servicio desplegado en Render:**

![Render Dashboard](img/hito5/01-render-dashboard.png)

---

## 5. Arquitectura final en producción

La arquitectura final del sistema desplegado es la siguiente:

- Cliente HTTP
- Plataforma PaaS Render
- Contenedor Docker
- FastAPI + Uvicorn
- Servicio externo Have I Been Pwned

Toda la infraestructura es gestionada por la plataforma PaaS, sin necesidad de administrar servidores manualmente.

---

## 6. Verificación del servicio desplegado

Una vez completado el despliegue, se verificó el correcto funcionamiento del servicio mediante las siguientes URLs públicas:

- **URL base del servicio**  
  https://passcheck-api.onrender.com

- **Healthcheck**  
  https://passcheck-api.onrender.com/health

**Respuesta obtenida:**
```json
{ "status": "ok" }

