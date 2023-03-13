from concurrent import futures

import grpc
import time

import chat_pb2
import chat_pb2_grpc

class ChatServer(chat_pb2_grpc.ChatServerServicer): 

    def __init__(self):
        self.chats = []

    def ChatStream(self, request_iterator, context):

        lastindex = 0
        while True:
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                lastindex += 1
                yield n

    def SendMessage(self, request: chat_pb2.Message, context):
        print("[{}] {}".format(request.name, request.message))
        self.chats.append(request)
        return chat_pb2.Empty()


if __name__ == '__main__':
    port = 50015  
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServerServicer_to_server(ChatServer(), server)
    print('Starting server. Listening...')
    server.add_insecure_port('[::]:50015')
    server.start()

    while True:
        time.sleep(64 * 64 * 100)