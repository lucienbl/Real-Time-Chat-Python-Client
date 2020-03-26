import socketio
from pyeventdispatcher import register
from src.ChatSocketHandler import ChatSocketHandler

# Connect to the gateway
sio = socketio.Client()
sio.connect('http://localhost:5000', namespaces=['/chat'])
print('Connected! SID:', sio.sid)

# Event listeners
register("event_message_add", lambda event: print(f"{event.data['user_id']}::{event.data['message']}"))

# Register namespaces
sio.register_namespace(ChatSocketHandler('/chat'))
