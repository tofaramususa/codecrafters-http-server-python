import gzip

def createResponse(content="", content_type="text/plain", status=200, content_encoding=""):
    statusMessage = {200: "OK", 404: "Not Found", 201: "Created"}.get(status, "OK")
    response = f"HTTP/1.1 {status} {statusMessage}\r\n"
    if "gzip" in content_encoding:
        content = gzip.compress(content.encode())
        response += "Content-Encoding: gzip\r\n"
    response += f"Content-Type: {content_type}\r\n"
    response += f"Content-Length: {len(content)}\r\n"
    response += "\r\n"
    response = response.encode() + (content if isinstance(content, bytes) else content.encode())
    return response
