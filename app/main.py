# main.py
import socket
import select
from handlers import handleRequest

def main():
    print("Logs from your program will appear here!")
    with socket.create_server(("localhost", 4221), reuse_port=True) as server_socket:
        print("Server started on localhost 4221")
        server_socket.listen()
        server_socket.setblocking(False)

        inputs = [server_socket]

        while True:
            readable, _, _ = select.select(inputs, [], [])
            for s in readable:
                if s is server_socket:
                    connection, address = server_socket.accept()
                    connection.setblocking(False)
                    inputs.append(connection)
                else:
                    request = s.recv(1024).decode()
                    response = handleRequest(request)
                    try:
                        s.sendall(response)
                    except Exception as e:
                        print(f"Error: {e}")
                    finally:
                        s.close()
                        inputs.remove(s)

if __name__ == "__main__":
    main()
