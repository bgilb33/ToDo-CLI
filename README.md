We developed a multi-user console-based task manager in Python. The application uses Redis Pub/Sub for real-time communication between users and PostgreSQL to store task data. 
Users interact through a command-line interface to add tasks, mark them as complete, view all tasks, and delete tasks. When a task is modified, a message is published to Redis, 
and all connected peers update immediately.The system is containerized with Docker and managed using Docker Compose. It includes services for Redis, PostgreSQL, and two peers running the CLI application. 
Environment variables are used inside each container to configure database access. The PostgreSQL service is initialized with a default database, user, and password defined in the docker-compose.yml file.
The main application code is in todo-cli.py, which handles the CLI loop and user inputs. task_db.py manages the PostgreSQL connection and implements operations such as inserting, updating, deleting, and querying tasks. 
redis_pubsub.py handles subscribing to the Redis channel and publishing notifications when tasks are changed. A separate listener thread is started for Redis Pub/Sub to allow the CLI to receive updates while waiting for user input.
Helper scripts (run-peer.sh, run-peer.bat, and wait-for-it.sh) are used to start the application cleanly after verifying that Redis and PostgreSQL are reachable.
To run the system, Docker and Docker Compose are required. Running docker compose up --build starts all services and launches interactive terminals for each peer. 
Each peer connects to the shared PostgreSQL database and Redis server, allowing real-time task synchronization across multiple users.
