import threading
import redis
import json
from datetime import datetime

global_channel = "todo:updates"

class RedisPubSub:
    def __init__(self, username, redis_host="localhost"):
        self.username = username
        self.redis_client = redis.Redis(host=redis_host, port=6379, decode_responses=True)
        self.pubsub = self.redis_client.pubsub()

    def start_listener(self, on_global_message, on_direct_message):
        def listen():
            self.pubsub.subscribe(global_channel)
            self.pubsub.subscribe(f"todo:{self.username}")
            for message in self.pubsub.listen():
                if message['type'] == 'message':
                    channel = message['channel']
                    data = json.loads(message['data'])
                    if channel == global_channel:
                        on_global_message(data)
                    elif channel == f"todo:{self.username}":
                        on_direct_message(data)

        listener_thread = threading.Thread(target=listen, daemon=True)
        listener_thread.start()

    def publish_global_update(self, action):
        message = {
            "type": "task_update",
            "from": self.username,
            "action": action,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.redis_client.publish(global_channel, json.dumps(message))

    def publish_direct_message(self, target_user, message_text):
        message = {
            "type": "direct_message",
            "from": self.username,
            "message": message_text,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.redis_client.publish(f"todo:{target_user}", json.dumps(message))
