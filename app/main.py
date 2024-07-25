# Uncomment this to pass the first stage
import socket
import select 

def createResponse(content="", content_type="text/plain", status=200): #create a response body
	statusMessage = {200: "OK", 404: "Not Found"}.get(status, "OK") # ok is the default is not found
	return f"HTTP/1.1 {status} {statusMessage}\r\nContent-Type: {content_type}\r\nContent-Length: {len(content)}\r\n\r\n{content}".encode()



def handle_request(request):
	requestArray = request.split("\r\n") # split request into array
	firstLine = requestArray[0].split(" ") #take the first line with http method and split into array by space
	methodItems = firstLine[1].split("/") #take the line with the endpoint and split into array - get the route
	route = methodItems[1] #get the route

	if(route == ""):
		return(createResponse())
	if(route == "echo" and len(methodItems) > 2):
		return(createResponse(methodItems[2])) #return the endpoint if echo
	if(route == "user-agent"):
		for line in requestArray:
			if("User-Agent" in line):
				return(createResponse(line.split(": ")[1]))
	if(route == "files"):
		filename = methodItems[2] if len(methodItems) > 2 else "nonexistent"
		try:
			with open(f"/tmp/{filename}", "r") as file:
				content = file.read()
				return(createResponse(content))
		except FileNotFoundError:
			return(createResponse(status=404))
	return(createResponse(status=404, content_type="application/octet-stream")) #return 404 if route not found

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
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
					response = handle_request(request)
					try:
						s.sendall(response)
					except Exception as e:
						print(f"Error: {e}")
					finally:
						s.close()
						inputs.remove(s)
			

if __name__ == "__main__":
    main()
