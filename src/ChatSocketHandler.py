import socketio
from pyeventdispatcher import dispatch, Event, register
from src import LocalEvents, SocketEvents


class ChatSocketHandler(socketio.ClientNamespace):
    def on_connect(self):
        self.emit(SocketEvents.join_channel, {'user_id': "michel", 'room_id': '1234'})
        register(LocalEvents.EVENT_MESSAGE_SEND, lambda event: self.send_message(event.data))

    def on_disconnect(self):
        pass

    def send_message(self, message):
        self.emit(SocketEvents.send_message, {'room_id': '1234', 'user_id': 'michel', 'message': message})

    @staticmethod
    def on_message_added(data):
        dispatch(Event(LocalEvents.EVENT_MESSAGE_ADDED, data))
