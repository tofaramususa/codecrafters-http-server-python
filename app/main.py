# Uncomment this to pass the first stage
import socket
import select 

def create_response(string): #create a response body
	
	if(string == "404"):
		response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 0\r\n\r\n".encode()
		return (response)
	response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()
	return response



def handle_request(request):
	requestArray = request.split("\r\n") # split request into array
	firstLine = requestArray[0].split(" ") #take the first line with http method and split into array by space
	methodItems = firstLine[1].split("/") #take the line with the endpoint and split into array - get the route
	route = methodItems[1] #get the route
	if(route == ""):
		return("")
	if(route == "echo" and len(methodItems) > 2):
		return(methodItems[2]) #return the endpoint if echo
	if(route == "user-agent"):
		for line in requestArray:
			if("User-Agent" in line):
				return(line.split(": ")[1])
	return("404")

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
	print("Logs from your program will appear here!")
	with socket.create_server(("localhost", 4221), reuse_port=True) as server_socket:
		print("Server started on localhost 4421")
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
					endpointStr = handle_request(request)
					response = create_response(endpointStr)
					try:
						s.sendall(response)
					except Exception as e:
						print(f"Error: {e}")
					finally:
						s.close()
						inputs.remove(s)
			

if __name__ == "__main__":
    main()
