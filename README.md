# Как с этим взлетать

Основа бота:

    aiogram 3
    PostgreSQL + SQLAlchemy

## Предварительная настройка

    в bot/data внести свои данные в файл env.template и затем сделать его просто .env

Далее

    в файле docker-compose.yml
    в строке 10 "postgres" заменить на нормальный пароль, который записали в .env в предыдущем шаге

    а также проконтролировать, чтобы совпадали порты тут и в .env-файле 
    (нет времени объяснять, можно оставить порты как есть, НО обязательно сменить имя пользователя и задать сложный пароль)

## Запуск бота
Запуск производится следующей командой

    docker-compose up -d

Остановить бота можно командой

    docker-compose down

## Иметь ввиду

в /backups будут сгружаться бэкапы базы данных

    Нужно скорректировать скрипт, добавить его в crontab на сервере, где будет лежать бот
        Добавить в crontab отправку файла бэкапа на другой сервер
        В данном скрипте сохраняется только 2 последних месяца, потом перезаписываются
    Либо как угодно по-своему сделать бэкапы

В bot/data/bot_cfg 25 строка - устанавливает время для отправки отложенных сообщений по Гринвичу

Ключ от гугл-api https://console.cloud.google.com/ нужно сделать и сюда добавить

    bot/data/bot_cfg.py строка 73 	
    sheet_key = ТУТ ДОЛЖЕН БЫТЬ КЛЮЧ ОТ СЕРВИСА ГУГЛ-API https://console.cloud.google.com/

в bot/db

    bot/db/migrations - будут у вас свои, тк база данных своя у вас (это SQLAlchemy)

запросы в Базу прописаны (там куча мусора, который хранится, как подсказка - после строки #######)
    
    async_request_db_postgres.py - асинхронные
    sync_request_db_postgres.py - синхронные

написать свои модели

    в bot/db/models_db_postgres

в фильтрах есть проверка роли пользователя, но тут она нигде не используется

    bot/filters/check_role

в хендлерах до админских команд я не дошёл
    
    bot/handlers/admins.py

