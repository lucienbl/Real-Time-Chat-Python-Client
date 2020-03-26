import socketio


class ChatSocketHandler(socketio.ClientNamespace):
    def on_connect(self):
        self.emit('join', {'user_id': "1", 'room_id': '1'})
        self.emit('message_add', {'room_id': '1', 'message': "Hello!!"})

    def on_disconnect(self):
        pass

    def on_message_add(self, data):
        print(str(data))
