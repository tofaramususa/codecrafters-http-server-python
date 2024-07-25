from response import createResponse

def handleEchoRoute(requestMessage): 
    requestArray = requestMessage.split("\r\n") 
    firstLine = requestArray[0].split(" ") 
    methodItems = firstLine[1].split("/") 
    for line in requestArray:
        if "Accept-Encoding" in line:
            return createResponse(methodItems[2], content_encoding=line.split(": ")[1])
    return createResponse(methodItems[2])

def handleFileRoute(filename, request_type="GET", request_body=""): 
    if request_type == "POST":
        newfile = open(f"/tmp/data/codecrafters.io/http-server-tester/{filename}", "a")
        newfile.write(request_body)
        newfile.close()
        return createResponse(status=201)
    else:
        try:
            with open(f"/tmp/data/codecrafters.io/http-server-tester/{filename}", "r") as file:
                content = file.read()
                return createResponse(content, content_type="application/octet-stream")
        except FileNotFoundError:
            return createResponse(status=404)

def handleRequest(request):
    requestArray = request.split("\r\n") 
    firstLine = requestArray[0].split(" ") 
    methodItems = firstLine[1].split("/") 
    route = methodItems[1] 

    if route == "":
        return createResponse()
    if route == "echo" and len(methodItems) > 2:
        return handleEchoRoute(request)
    if route == "user-agent":
        for line in requestArray:
            if "User-Agent" in line:
                return createResponse(line.split(": ")[1])
    if route == "files":
        filename = methodItems[2] if len(methodItems) > 2 else "nonexistent"
        return handleFileRoute(filename, firstLine[0], requestArray[-1])

    return createResponse(status=404)
