# Uncomment this to pass the first stage
import socket
import select 
import gzip

def handleEchoRoute(requestMessage): #handle the echo route
	requestArray = requestMessage.split("\r\n") # split request into array
	firstLine = requestArray[0].split(" ") #take the first line with http method and split into array by space
	methodItems = firstLine[1].split("/") #take the line with the endpoint and split into array - get the route
	for line in requestArray:
		if("Accept-Encoding" in line):
			return(createResponse(methodItems[2],content_encoding=line.split(": ")[1]))
	return(createResponse(methodItems[2]))

def handleFileRoute(filename, request_type="GET", request_body=""): #handle the file route

	if(request_type == "POST"):
		newfile = open(f"/tmp/data/codecrafters.io/http-server-tester/{filename}", "a")
		newfile.write(request_body)
		newfile.close()
		return(createResponse(status=201)) #return 201 if post request
	else:
		try:
			with open(f"/tmp/data/codecrafters.io/http-server-tester/{filename}", "r") as file:
				content = file.read()
				return(createResponse(content, content_type="application/octet-stream"))
		except FileNotFoundError:
			return(createResponse(status=404))

def createResponse(content="", content_type="text/plain", status=200, content_encoding=""): #create a response body
	statusMessage = {200: "OK", 404: "Not Found", 201: "Created"}.get(status, "OK") # ok is the default is not found
	response = f"HTTP/1.1 {status} {statusMessage}\r\n"
	if"gzip" in content_encoding:
		content = gzip.compress(content.encode())
		response += f"Content-Encoding: gzip\r\n"
	response += f"Content-Type: {content_type}\r\n"
	response += f"Content-Length: {len(content)}\r\n"
	response += "\r\n"
	response += content
	return response.encode()

def handleRequest(request):
	requestArray = request.split("\r\n") # split request into array
	firstLine = requestArray[0].split(" ") #take the first line with http method and split into array by space
	methodItems = firstLine[1].split("/") #take the line with the endpoint and split into array - get the route
	route = methodItems[1] #get the route

	if(route == ""):
		return(createResponse())
	if(route == "echo" and len(methodItems) > 2):
		return(handleEchoRoute(request)) #return the endpoint if echo
	if(route == "user-agent"):
		for line in requestArray:
			if("User-Agent" in line):
				return(createResponse(line.split(": ")[1]))
	if(route == "files"):
		filename = methodItems[2] if len(methodItems) > 2 else "nonexistent"
		return(handleFileRoute(filename, firstLine[0], requestArray[-1]))

	return(createResponse(status=404)) #return 404 if route not found

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
