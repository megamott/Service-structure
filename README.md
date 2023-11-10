# Service-structure
## Общая информация
Структура сервиса на aiohttp с базой данных, poetry, тестами и линтерами.

### Локальное развертывание и тестирование

1. Поднимаем postgres на docker-compose
```bash
docker-compose up -d
```

2. Копируем содержимое `etc/config.tmpl.yaml` в какой-нибудь файл `/path/to/config.yaml`. Подставляем в `/path/to/config.yaml` свои значения. Делаем
```bash
export CDM_API_CONFIG_PATH=/path/to/config.yaml
```

3. Создаем виртуальное окружение и ставим зависимости при помощи poetry
```bash
mkdir -p ~/.virtualenvs
python3 -m venv ~/.virtualenvs/service-structure
. ~/.virtualenvs/cdm-api/bin/activate
pip install poetry
poetry install
```

4. Накатываем миграции
```bash
alembic upgrade head
```

5. Запускаем приложение
```bash
make start
```

6. Запускаем тесты
```bash
make test
```

7. Настраиваем pre-commit хуки
```bash
poetry run pre-commit install
```