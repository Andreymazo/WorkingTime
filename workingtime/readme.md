Проект 2-го модуля бэкенда платформы для тестирования учеников.

**Запуск Dev из-под Ubuntu**

В проекте используется Python 3.8.3, поэтому если не установлена вышеуказанная версия, следует ее установить и создать виртуальное окружение. Это может быть исполнено разными способами, один из них это библиотека 
Pyenv, которая во-первых, позволяет переключаться между версиями Python, во-вторых, управлять виртуальным окружением. 

**Installation Pyenv in Ubuntu** 

- sudo apt update
- curl https://pyenv.run | bash (Подразумевается, что curl, shell установлены)
- Вставим три строчки в ~/.bashrc и три строчки в ~/.profile 

1. echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc 
2. echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc 
3. echo 'eval "$(pyenv init -)"' >> ~/.bashrc 


1. echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile 
2. echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile 
3. echo 'eval "$(pyenv init -)"' >> ~/.profile
- перезапустите консоль и проверьте работу Pyenv, например, командой pyenv virtualenvs (покажет список возможных виртуальных окружений)

**Clone repozitory and installing virtual environment**

- склонируйте репозитоорий Dev: ...
- Проверьте следующие настройки проекта:

  1. <path_to_project>/phoenix-backend/src/phoenix/settings/components/logger_settings.py  должно быть True
  2. <path_to_project>/phoenix-backend/dockers/envs/.env.dev.db  должно быть (POSTGRES_PASSWORD=)
     3. <path_to_project>/phoenix-backend/src/phoenix/settings/components/settings.py 
     ...
"NAME": os.environ.get("SQL_DATABASE"), 
"USER": os.environ.get("SQL_USER"), 
"PASSWORD": os.environ.get("SQL_PASSWORD"),
     ...
      данные в .env файл по запросу
        SECRET_KEY=
        BASE_URL=
        SQL_DATABASE=
        SQL_USER=
        SQL_PASSWORD=
  4. <path_to_project>/phoenix-backend/src/phoenix/settings/components/redis_settings.py 5 строчка ("LOCATION": ["redis://localhost:6379/1", ],)


- перейдите в каталог src (в нем должен быть manage.py)
- Создайте виртуальное окружение: pyenv virtualenv 3.8.3 phoenix-backend 
- Активируйте его: pyenv activate phoenix-backend ыгвщ (должны увидеть что-то такое: (phoenix-backend) ivan_ivanov@ivanivanov:~/PycharmProjects/phoenix-backend/src$ )
- pip install --upgrade pip
- pip install -r requirements.txt 
- Запускаем поочереди контейнеры Postgres и Redis (если они сейчас активированы, то лучше отключите их, чтобы не занимали порты):
  1. docker-compose -f docker-compose.yml up redis
  2. docker-compose -f docker-compose.prod.yml up db/docker-compose -f docker-compose.production.yml up -d db

  3. sudo docker start db redis

- python3 manage.py makemigrations
- python3 manage.py migrate
- python3 manage.py createsuperuser (создаем суперюзера, чтобы сразу можно было в админке работать)
- python3 manage.py runserver

**Loaddata (Заполняем базу)**

 1.    Cкопировать файл phoenix_db_2023-06-20.dump.gz и распаковать его в консоли: gzip -d file.gz 

    docker cp phoenix_db_2023-06-20.dump db:/phoenix_db_2023-06-20.dump
    docker exec -it db bash
    psql -U phoenix_user -d phoenix_prod -f /phoenix_db_2023-06-20.dump 


