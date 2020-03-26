import socketio
from src.ChatSocketHandler import ChatSocketHandler

# Connect to the gateway
sio = socketio.Client()
sio.connect('http://localhost:5000', namespaces=['/chat'])
print('Connected! SID:', sio.sid)

# Register namespaces
sio.register_namespace(ChatSocketHandler('/chat'))
