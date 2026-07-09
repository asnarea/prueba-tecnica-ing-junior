# Items API

API REST para gestionar un recurso de **tareas/items**, construida con **FastAPI** y **SQLite**, siguiendo una arquitectura por capas (Clean Architecture simplificada).

## Características

- CRUD de items con los 4 endpoints requeridos.
- Validación de datos y códigos HTTP apropiados (200, 201, 400, 404).
- Paginación en el listado (`?page=1&limit=10`).
- Persistencia en SQLite mediante SQLAlchemy.
- Tests de integración con pytest.
- Dockerfile funcional.

## Modelo

```json
{
  "id": "uuid",
  "title": "string",
  "priority": "low | medium | high",
  "status": "pending | in_progress | done",
  "createdAt": "ISO-8601",
  "description": "string"
}
```

Campos obligatorios al crear: `title` y `priority`.

## Endpoints

| Método | Ruta              | Descripción                              | Éxito |
|--------|-------------------|------------------------------------------|-------|
| GET    | `/items`          | Listar items (paginado: `?page=1&limit=10`) | 200   |
| GET    | `/items/{id}`     | Obtener un item por ID                   | 200   |
| POST   | `/items`          | Crear un item                            | 201   |
| PATCH  | `/items/{id}`     | Actualizar el estado del item            | 200   |
| GET    | `/health`         | Healthcheck                              | 200   |

Errores: `400` (validación), `404` (no encontrado).

## Estructura del proyecto

```
app/
├── main.py                  # Punto de entrada: crea la app, tablas y manejador 400
├── core/
│   └── config.py            # Configuración (DATABASE_URL por variable de entorno)
├── domain/
│   ├── models.py            # Entidad de negocio Item
│   └── enums.py             # Priority y Status
├── schemas/
│   └── item.py              # Modelos Pydantic (entrada/salida)
├── db/
│   ├── database.py          # Engine y sesión de SQLAlchemy
│   └── models_orm.py        # Modelo ORM (tabla items)
├── repositories/
│   ├── base.py              # Interfaz del repositorio (contrato)
│   └── sqlite_repository.py # Implementación con SQLite
├── services/
│   └── item_service.py      # Lógica de negocio (casos de uso)
└── api/
    ├── dependencies.py      # Wiring de dependencias (inyección del service)
    └── items.py             # Definición de las rutas
tests/
└── test_items.py            # Tests de integración de los endpoints
```

El flujo de dependencias va de afuera hacia adentro: `api → services → repositories → db`. El dominio no depende de ningún framework.

## Requisitos

- Python 3.11+ (probado con 3.13)
- (Opcional) Docker

## Ejecución local

```bash
# 1. Crear y activar el entorno virtual
python -m venv venv
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# Linux / macOS
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Levantar el servidor
uvicorn app.main:app --reload
```

La API queda disponible en `http://127.0.0.1:8000`.
Documentación interactiva (Swagger UI): `http://127.0.0.1:8000/docs`.

## Ejecución con Docker

```bash
# Construir la imagen
docker build -t items-api .

# Ejecutar el contenedor
docker run -p 8000:8000 items-api
```

## Configuración

| Variable       | Descripción                     | Valor por defecto        |
|----------------|---------------------------------|--------------------------|
| `DATABASE_URL` | URL de conexión a la base de datos | `sqlite:///./items.db`   |

## Tests

```bash
pytest
```

Los tests usan una base de datos SQLite en memoria, aislada y sin afectar la BD local.

## Ejemplos de uso

```bash
# Crear un item
curl -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{"title": "Comprar pan", "priority": "high", "description": "de la panadería"}'

# Listar con paginación
curl "http://127.0.0.1:8000/items?page=1&limit=10"

# Obtener por ID
curl http://127.0.0.1:8000/items/<id>

# Actualizar estado
curl -X PATCH http://127.0.0.1:8000/items/<id> \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'
```
