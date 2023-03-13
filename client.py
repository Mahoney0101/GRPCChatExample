import grpc
import chat_pb2
import chat_pb2_grpc
import queue
import threading

class Client:
    def __init__(self, u: str):
        self.username = u
        channel = grpc.insecure_channel('localhost:50051')
        self.conn = chat_pb2_grpc.ChatServerStub(channel)
        self.message_queue = queue.Queue()
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()
        threading.Thread(target=self.__send_messages, daemon=True).start()

    def __listen_for_messages(self):
        for message in self.conn.ChatStream(chat_pb2.Empty()):
            if message.name != self.username:
                print("R[{}] {}".format(message.name, message.message))

    def __send_messages(self):
        while True:
            message = self.message_queue.get()
            n = chat_pb2.Message()
            n.name = self.username
            n.message = message
            print("S[{}] {}".format(n.name, n.message))
            self.conn.SendMessage(n)

if __name__ == '__main__':
    username = input("What's your username? ")
    c = Client(username)

    while True:
        message = input("> ")
        c.message_queue.put(message)

