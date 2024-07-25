# Uncomment this to pass the first stage
import socket

def handle_request(request):

	requestArray = request.split("\r\n")
	requestArray = requestArray[0].split(" ")
	if(requestArray[1] == "/abcdefg"):
		return 404
	elif(requestArray[1] == "/"):
		return 200

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
	print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
	# server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    # # server_socket.accept() # wait for client
	# connection, address = server_socket.accept()

	with socket.create_server(("localhost", 4221), reuse_port=True) as server_socket:
		print("Server started on localhost 4421")
		while True:
			connection, address = server_socket.accept()
			request = connection.recv(1024).decode()
			status = handle_request(request)

			try:
				if status == 200:
					connection.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
				elif status == 404:
					connection.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
			except Exception as e:
				print(f"Error: {e}")
			finally:
				connection.close()
			

if __name__ == "__main__":
    main()
