import os
import psycopg2
from datetime import datetime

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "todo_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "todo_pass")
DB_NAME = os.getenv("DB_NAME", "todo_db")

class TaskDB:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=5432
        )
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                description TEXT NOT NULL,
                assigned_to TEXT NOT NULL,
                status TEXT NOT NULL,
                created_by TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS task_log (
                id SERIAL PRIMARY KEY,
                task_id INTEGER REFERENCES tasks(id),
                action TEXT NOT NULL,
                username TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL
            )
        ''')

        self.conn.commit()

    def sign_up(self, username):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
            self.conn.commit()
            return True
        except psycopg2.IntegrityError:
            self.conn.rollback()
            return False  # Username already exists

    def log_in(self, username):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        return cursor.fetchone() is not None

    def get_all_users(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT username FROM users")
        return [row[0] for row in cursor.fetchall()]

    def add_task(self, description, assigned_to, created_by):
        now = datetime.utcnow()
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (description, assigned_to, status, created_by, created_at)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        ''', (description, assigned_to, "todo", created_by, now))
        task_id = cursor.fetchone()[0]
        self.conn.commit()
        return task_id

    def update_task_status(self, task_id, new_status, username):
        now = datetime.utcnow()
        cursor = self.conn.cursor()
        cursor.execute("UPDATE tasks SET status = %s WHERE id = %s", (new_status, task_id))
        cursor.execute("INSERT INTO task_log (task_id, action, username, timestamp) VALUES (%s, %s, %s, %s)",
                       (task_id, f"status -> {new_status}", username, now))
        self.conn.commit()

    def get_all_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        return cursor.fetchall()

    def get_task_log(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM task_log")
        return cursor.fetchall()