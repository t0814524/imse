docker mariadb in ps:
docker exec -it mariadb1 mariadb -u root -p

rebuild docker:

```
docker-compose down
docker volume rm imse_mariadb_volume
docker volume rm imse_mongo_volume
docker-compose up --build
```

start webpack watcher to build ts (not rlly necessary probably cs i put most scripts directly into the templates)

```
cd demo
npm run dev
```

install node modules first (npm i) and py dependencies: pip install -r requirements.txt in the folders where package.json and requirements.txt are
start server:

```
cd demo/server
venv/Scripts/activate
python app.py
```

report:
source ./docker-entrypoint-initdb.d/sql/report.sql
