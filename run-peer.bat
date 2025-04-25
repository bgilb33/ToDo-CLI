@echo off

REM Run the ToDo peer container, connecting to host machine's Redis/Postgres

docker run --rm -it ^
  -e DB_HOST=host.docker.internal ^
  -e DB_USER=todo_user ^
  -e DB_PASSWORD=todo_pass ^
  -e DB_NAME=todo_db ^
  -e REDIS_HOST=host.docker.internal ^
  todo-peer-image
