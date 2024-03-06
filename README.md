## Configuration
The path to the config is passed through the command line args.
When configuring, priority is given to environment variables.
Settings in the yaml config file:
```yaml
env: "Launch environment. Valid values: dev, local, prod. Default local"
bot:
  token: Token of BotAPI
  locales_data_path: Path to locales data (not locales folder). Default "data/locales.yaml"
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

## App directory structure

- core: Contains the core and application domain
  - domain:
    - dto: Miscellaneous transport Objects (DTO)
    - exceptions: Domain level errors
    - models: Domain data models
    - services:Implementation of application services (business logic)
  - interfaces: Interfaces used in the domain
    - repository: Data Repository Interfaces
    - usecase: Business logic interfaces
- infrastructure:
  - db: for SQL DBMS
    - migrations: Migrations alembic
    - models: sqlalchemy models
    - repo: Adapters for databases that implement core/interfaces/repo interfaces
- bot: Bot implementation
  - widgets: Widgets for aiogram-dialogs
  - - handlers:
    - dialogs: All dialogs are here
      - execute.py: For convenient dialogs launch 
