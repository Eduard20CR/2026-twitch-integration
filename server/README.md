# UV cheat sheet
https://gemini.google.com/share/302dd29dd997


    

# Modules folder structure

auth/
├── router.py
├── controller.py        # Define endpoints HTTP y maneja requests/responses

├── services/
│   └── auth_service.py  # Lógica de negocio (login, OAuth, sesiones)

├── repositories/
│   ├── user_repository.py
│   └── session_repository.py  # Acceso a base de datos (CRUD)

├── infrastructure/
│   ├── twitch_client.py
│   └── exceptions.py    # Integraciones externas y errores de servicios externos

├── models/
│   ├── user_model.py
│   └── session_model.py # Modelos ORM (estructura de base de datos)

├── domain/
│   ├── entities.py
│   └── exceptions.py    # Entidades de negocio puras y errores del dominio

└── schemas/
    ├── requests.py
    └── responses.py     # DTOs: estructuras de entrada y salida de la API