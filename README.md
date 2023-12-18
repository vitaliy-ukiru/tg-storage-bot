## Конфигурация
Путь до конфига передаётся через переменную окружения CONFIG_PATH.
При настройке приоритет отдаётся переменным окружения.
Настройка в конфиг файле yaml:
```yaml
env: "Среда запуска. Допустимы значения: dev, local, prod. По умолчанию local"
tgbot:
  bot_token: Токен бота 
database:
  password: Пароль [Необязательно]
  username: Пользователь БД
  database: Имя БД
  host: Хост [необязательно]
  port: Порт, должно быть числом [необязательно] 
```
Переменные окружения:
- BOT_TOKEN - токен бота
- DB_PASSWORD
- DB_USERNAME
- DB_DATABASE
- DB_HOST
- DB_PORT

## Запуск
### Установите зависимости и конфигурацию приложения.
```
pip install -r requirements
```
### Установите миграции.
[Подброные инструкции](./app/infrastructure/db/migrations/README.md)
```
alembic upgrade head
```
### Запустите
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
