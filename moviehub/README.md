# Introduction 

### MovieHub
    Modern Django webová aplikace pro správu a hodnocení filmů.
    Projekt běží v Docker prostředí s PostgreSQL a Redis.

# Technologie
    Python 3.13
    Django
    PostgreSQL
    Redis
    Django Channels
    Docker & Docker Compose


# Spuštění projektu (doporučeno – přes Docker)

### Requirements
###### Docker desktop
    docker --version
    docker compose version
###### Git/Git clone
    git clone https://github.com/JosefKaljanko/Django_Project_MovieHub.git
    cd Django_Project_MovieHub/moviehub

### Vytvoření .env:
    DEBUG = 1
    SECRET_KEY=super-secret-key
    POSTGRES_DB=moviehub
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_HOST=db
    POSTGRES_PORT=5432
    REDIS_HOST=redis
    REDIS_PORT=6379




[//]: # (## Installation)

[//]: # (    pip install -r requirements.txt)

[//]: # ()
[//]: # (## Run)

[//]: # (    cd moviehub)

[//]: # (    python manage.py runserver)




## Docker container

##### Spuštění
    • First Run
    docker compose up --build

    • After First Run
    docker compose up
          or
    docker compose up -d          # na pozadí

##### Zastavení
    • Stop project
    docker compose down

    • Stop and DELETE DB
    docker compose down -v

##### Restart
    • Restart
    docker compose restart web

### Database

    • Database
    docker compose exec web python manage.py migrate

    • create superuser
    docker compose exec web python manage.py createsuperuser

    • DB ze zálohy
    docker compose exec db pg_restore -U postgres -d moviehub_db2 --clean --if-exists /moviehub.dump
    docker compose exec -T db pg_restore -U postgres -d moviehub < moviehub.dump

### Open app
    http://localhost:8000
    http://localhost:8000/admin


### Vymazání cache:
    docker compose exec redis redis-cli FLUSHALL

### LOG:
    docker compose logs --tail=200 web
    docker compose logs -f


## Tests
    pytest -v

## Struktura projektu
    moviehub/
    │
    ├── accounts/
    ├── chat/
    ├── media/
    ├── moviehub/
    ├── movies/
    ├── pages/
    ├── reviews/
    │
    ├── docker-compose.yml
    ├── Dockerfile
    ├── requirements.txt
    ├── requirements_minimum.txt
    └── manage.py


### author
## Josef Kaljanko

## Run project with chat app

[//]: # (PowerShell:)
[//]: # (cd moviehub)
[//]: # (daphne -b 127.0.0.1 -p 8015 moviehub.asgi:application)

for .env file contact me
josefkaljanko@gmail.com
