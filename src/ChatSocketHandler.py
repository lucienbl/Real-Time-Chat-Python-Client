import socketio
from pyeventdispatcher import dispatch, Event


class ChatSocketHandler(socketio.ClientNamespace):
    def on_connect(self):
        self.emit('join', {'user_id': "1", 'room_id': '1'})
        self.emit('message_add', {'room_id': '1', 'user_id': '1', 'message': "Hello!!"})

    def on_disconnect(self):
        pass

    @staticmethod
    def on_message_add(data):
        dispatch(Event("event_message_add", data))
