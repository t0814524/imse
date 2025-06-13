docker mariadb in ps:
docker exec -it mariadb1 mariadb -u root -p

rebuild docker:
docker-compose down
docker volume rm imse_mariadb_volume
docker-compose up --build
