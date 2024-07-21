import socket
import datetime
import json
import pymongo

client = pymongo.MongoClient("mongodb://mongo:27017/")
db = client['mydatabase']
collection = db['messages']

PORT = 5000

def handle_client(connection):
    data = connection.recv(1024)
    if data:
        message = data.decode('utf-8')
        message_dict = json.loads(message)
        message_dict['date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        collection.insert_one(message_dict)
        print(f"Received and saved: {message_dict}")

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', PORT))
        s.listen()
        print(f'Starting socket server on port {PORT}...')
        while True:
            conn, addr = s.accept()
            with conn:
                print(f'Connected by {addr}')
                handle_client(conn)

if __name__ == '__main__':
    run_server()