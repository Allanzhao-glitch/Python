import socket
import example_pb2

def server():
    while 1:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 8888))
        server_socket.listen(1)

        print("Waiting for connection...")
        conn, addr = server_socket.accept()

        print(f"Connected by {addr}")
        data = conn.recv(1024)
        print(f"Received data: {data}")
        person = example_pb2.Person()
        person.ParseFromString(data)

        print(f"Received: Name={person.name}, Age={person.age}, Hobbies={person.hobbies}")
    
        conn.close()
        server_socket.close()
 
if __name__ == "__main__":
    import threading
    server_thread = threading.Thread(target=server)

    server_thread.start()

