# P2P ToDo TaskBoard (EC530 Final Project)

## Overview
This project is a distributed peer-to-peer (P2P) collaborative To-Do list application built using Docker containers, Redis pub/sub for real-time updates, and PostgreSQL for persistent task storage.

Each peer (user) runs their own containerized CLI application and connects to a central server hosting Redis and PostgreSQL. The system supports real-time global alerts, direct task assignment, task status updates, and user management.

---

## Architecture

- **PostgreSQL**: Stores users, tasks, and task logs.
- **Redis**: Manages real-time messaging (global task updates, direct messages).
- **Peers (Users)**: Run inside lightweight Docker containers and connect to the central server.

> Central server must expose ports `5432` (Postgres) and `6379` (Redis).

---

## Setup

### 1. Server Setup (Redis + Postgres)

On the central server machine:

```bash
docker-compose up db redis
```

Make sure `docker-compose.yml` exposes:
- Postgres on port `5432`
- Redis on port `6379`

### 2. Peer Setup (Mac/Linux/Windows)

On each user's machine:

1. Install **Docker Desktop**.
2. Clone or download the project files.
3. Open a terminal inside the project folder.
4. Build the peer Docker image:

```bash
docker build -t todo-peer-image .
```

5. Configure the correct server IP (the server's Wi-Fi IP address, e.g., `10.0.0.249`).

6. **Mac/Linux Users**:
- Edit `run-peer.sh` to use the correct server IP.
- Make it executable:

```bash
chmod +x run-peer.sh
```

- Run it:

```bash
./run-peer.sh
```

**Windows Users**:
- Edit `run-peer.bat` to use the correct server IP.
- Double-click `run-peer.bat` or run from CMD:

```bash
run-peer.bat
```

---

## Important Notes

- **Everyone must be on the same network** (or server ports must be forwarded if remote).
- **Server IP** must match the IP address of the machine running Postgres + Redis.
- Peers automatically wait for Postgres to become available before starting.
- Tasks are globally visible once created.
- Real-time alerts require working Redis pub/sub.

---

## Commands

| Action | Command |
|:------|:-------|
| Start server | `docker-compose up db redis` |
| Reset database completely | `docker-compose down -v` then `docker-compose up db redis` |
| Build peer image | `docker build -t todo-peer-image .` |
| Run peer (Mac/Linux) | `./run-peer.sh` |
| Run peer (Windows) | `run-peer.bat` |

---

## Folder Structure

```plaintext
/ToDo-CLI
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── task_db.py
├── todo-peer.py
├── redis_pubsub.py
├── wait-for-it.sh
├── run-peer.sh (for Mac/Linux)
├── run-peer.bat (for Windows)
└── README.md
```

---

## Project Demo Flow

1. Server: Start Postgres + Redis.
2. User A: Runs peer container, signs up/logs in.
3. User B: Runs peer container, signs up/logs in.
4. User A creates task assigned to User B.
5. User B gets real-time direct alert.
6. Both can view/update tasks in real-time.

✅ Full real-time, multi-user, containerized collaborative task management!

---
