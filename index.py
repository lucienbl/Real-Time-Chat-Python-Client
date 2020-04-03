import socketio
from tkinter import *
from pyeventdispatcher import register, dispatch, Event
from tkinterhtml import HtmlFrame
import markdown
from src import LocalEvents
from src.ChatSocketHandler import ChatSocketHandler


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        # Global vars
        self.messages = []

        # Create Widgets
        self.btn_connect = Button(self, text="Connect", command=self.connect)
        self.chat_messages = HtmlFrame(self, horizontal_scrollbar="auto")
        self.message_entry_value = StringVar()
        self.message_entry = Entry(self, textvariable=self.message_entry_value)
        self.btn_send_msg = Button(self, text="Send", command=self.send_msg)
        self.label_status = Label(self, text="Disconnected")

        # Pack widgets
        self.pack_widgets()

    def pack_widgets(self):
        self.btn_connect.pack(side="top")
        self.chat_messages.pack(side="bottom")
        self.message_entry_value.set("")
        self.message_entry.pack(side="bottom")
        self.btn_send_msg.pack(side="bottom")
        self.label_status.pack(side="bottom")

    def connect(self):
        self.label_status['text'] = "Connecting..."

        try:
            # Connect to the gateway
            sio = socketio.Client()
            sio.connect('http://localhost:5000', namespaces=['/chat'])
            self.label_status['text'] = "Connected. SID : " + sio.sid

            # Event listeners
            register(LocalEvents.EVENT_MESSAGE_ADDED, lambda event: self.on_message_added(event.data))

            # Register namespaces
            sio.register_namespace(ChatSocketHandler('/chat'))
        except Exception as e:
            self.label_status['text'] = e

    def send_msg(self):
        dispatch(Event(LocalEvents.EVENT_MESSAGE_SEND, self.message_entry_value.get()))
        self.message_entry_value.set("")

    def on_message_added(self, data):
        self.messages.append(data)

        chat_messages = ""

        for message in self.messages:
            chat_messages = markdown.markdown(
                "**" + message['user_id'] + "**: " + message['message'] + '\n'
            ) + chat_messages

        self.chat_messages.set_content("""
            <html>
                <body style="font-size: 20px;">
                    {0}
                </body>
            </html>    
        """.format(chat_messages))


# Start the app
if __name__ == '__main__':
    root = Tk()
    root.geometry("1000x750")
    app = Application(master=root)
    app.mainloop()
