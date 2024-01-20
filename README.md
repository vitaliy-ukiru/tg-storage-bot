## Configuration
The path to the config is passed through the command line args.
When configuring, priority is given to environment variables.
Settings in the yaml config file:
```yaml
env: "Launch environment. Valid values: dev, local, prod. Default local"
bot:
  token: Token of BotAPI
db:
  password: Password [Optional]
  username: DB User
  database: DB name
  host: Host [Optional]
  port: Port, must be integer [Optional] 
```
Environment variables:
- BOT_TOKEN
- DB_PASSWORD
- DB_USERNAME
- DB_DATABASE
- DB_HOST
- DB_PORT

## How to run
### Create and activate venv
```
python -m venv venv
source venv/bin/activate
```
### Install dependencies
```
pip install -r requirements
```
### Apply migrations
[Details](./app/infrastructure/db/migrations/README.md)
```
alembic upgrade head
```
### Run
#### Command line args
```
usage: app [-h] [--config CONFIG]

Telegram bot for stores files

options:
  -h, --help       show this help message and exit
  --config CONFIG  path to config file

```
```
python -m app
```

## Структура директории app

- core: Содержит ядро и домен приложения
  - domain:
    - dto: Разные объекты для транспорта DTO
    - exceptions: Ошибки доменного уровня
    - models: Доменные модели данных
    - services: Реализация сервисов приложения (бизнес логика)
  - interfaces: Интерфейсы используемые в домене
    - repository: Интерфейсы репозиториев данных
    - usecase: Интерфейсы бизнес логики
- infrastructure:
  - db: для SQL СУБД
    - migrations: Миграции alembic
    - models: Модели sqlalchemy
    - repo: Адаптеры для БД, реализующие интерфейсы core/interfaces/repo
- bot: Реализация бота
  - widgets: Виджеты для диалогов
  - handlers:
    - dialogs: Все диалоги лежат здесь
      - execute.py: Для удобного запуска диалогов
