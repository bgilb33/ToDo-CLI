#!/bin/bash

# Run the ToDo peer container, connecting to host machine's Redis/Postgres

docker run --rm -it \
  -e DB_HOST=10.0.0.249 \
  -e DB_USER=todo_user \
  -e DB_PASSWORD=todo_pass \
  -e DB_NAME=todo_db \
  -e REDIS_HOST=10.0.0.249 \
  todo-peer-image
