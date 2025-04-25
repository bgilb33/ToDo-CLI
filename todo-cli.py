import os
from task_db import TaskDB
from redis_pubsub import RedisPubSub
import threading

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

def main():
    db = TaskDB()

    print("\n👋 Welcome to P2P TaskBoard!")
    print("1. Sign Up")
    print("2. Log In")

    choice = input("Select an option (1 or 2): ").strip()

    if choice == "1":
        username = input("Choose a username: ").strip()
        if not username:
            print("❌ Username cannot be empty.")
            return

        success = db.sign_up(username)
        if success:
            print(f"✅ User '{username}' created. You're signed in!")
            current_user = username
        else:
            print("❌ Username already exists. Try logging in instead.")
            return

    elif choice == "2":
        username = input("Enter your username: ").strip()
        if not username:
            print("❌ Username cannot be empty.")
            return

        if db.log_in(username):
            print(f"✅ Logged in as '{username}'")
            current_user = username
        else:
            print("❌ Username not found. Try signing up.")
            return

    else:
        print("❌ Invalid choice.")
        return

    # Start Redis pub/sub listener
    pubsub = RedisPubSub(current_user, REDIS_HOST)

    def on_global(msg):
        print(f"\n🌐 [GLOBAL] {msg['from']} {msg['action']} @ {msg['timestamp']}")

    def on_direct(msg):
        print(f"\n📬 [DM from {msg['from']}] {msg['message']} @ {msg['timestamp']}")

    pubsub.start_listener(on_global, on_direct)

    # Proceed to menu
    main_menu(db, pubsub, current_user)

def main_menu(db, pubsub, current_user):
    while True:
        print(f"\n🛒 {current_user}'s Dashboard:")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Update Task")
        print("4. View Log")
        print("5. View Users")
        print("6. Exit")

        choice = input("> ").strip()

        if choice == "1":
            tasks = db.get_all_tasks()
            if not tasks:
                print("No tasks yet.")
            else:
                print("\n📋 All Tasks:")
                for task in tasks:
                    print(f"#{task[0]}: {task[1]} (to {task[2]}, status: {task[3]})")

        elif choice == "2":
            description = input("Enter task description: ").strip()
            assignee = input("Assign to (username): ").strip()

            # Check if assignee exists
            users = db.get_all_users()
            if assignee not in users:
                print(f"❌ Error: User '{assignee}' does not exist.")
                continue

            task_id = db.add_task(description, assignee, current_user)
            print(f"✅ Task #{task_id} created and assigned to {assignee}.")
            pubsub.publish_global_update(f"added task #{task_id} for {assignee}")
            pubsub.publish_direct_message(assignee, f"You were assigned task #{task_id}: {description}")

        elif choice == "3":
            try:
                task_id = int(input("Enter task ID to update: "))
                status = input("New status (todo/in_progress/done): ").strip()
                db.update_task_status(task_id, status, current_user)
                print("✅ Task updated.")
                pubsub.publish_global_update(f"marked task #{task_id} as {status}")
            except Exception as e:
                print(f"❌ Error: {e}")

        elif choice == "4":
            logs = db.get_task_log()
            if not logs:
                print("No task activity yet.")
            else:
                print("\n📜 Task Log:")
                for log in logs:
                    print(f"Task #{log[1]} {log[2]} by {log[3]} at {log[4]}")

        elif choice == "5":
            users = db.get_all_users()
            print("\n👥 Known Users:")
            for u in users:
                print(f"- {u}")

        elif choice == "6":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()
