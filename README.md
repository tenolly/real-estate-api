# real-estate-api

# launch
```bash
docker-compose up --build
```

# proxy
Список находится в папке /app/parsers/core/browser/proxies.json. Пример:
```json
[
    {
        "server": "http://{ip}:{port}",
        "username": "{username}",
        "password": "{password}"
    },
    {
        "server": "http://{ip}:{port}",
        "username": "{username}",
        "password": "{password}"
    },
    ...
]
```

# full clean
```bash
docker system prune --all --volumes
```

# tests
```bash
pytest
```

# tests (docker)
```bash
docker-compose up test --build
```
