import socket
import example_pb2

def client():
    while 1:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 8888))
    
        person = example_pb2.Person()
        person.name = "Bob"
        person.age = 30
        person.hobbies.extend(["running", "cycling"])
    
        serialized_data = person.SerializeToString()
        print(f"Serialized data: {serialized_data}")
        client_socket.sendall(serialized_data)
    
        client_socket.close()
 
if __name__ == "__main__":
    import threading

    client_thread = threading.Thread(target=client)
 

    client_thread.start()
 
