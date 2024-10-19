# SF_MARKETING

---

env example
```text
BOT_TOKEN=<BOT_TOKEN>

DB_USER=<DB_USER>
DB_PASSWORD=<DB_PASSWORD>
DB_NAME=<DB_NAME>

# for local
#DB_HOST=localhost
#DB_PORT=5435

# for Docker
DB_HOST=telegram_postgres
DB_PORT=5432
```
BOT_TOKEN - Токен бота

DB_USER - Админ пользователь в бд

DB_PASSWORD - Пароль от базы данных

DB_NAME - Название базы данных

DB_HOST - для доккера его локальное название, для локального подключения localhost

DB_PORT - для доккера 5432 для локального подключения 5435