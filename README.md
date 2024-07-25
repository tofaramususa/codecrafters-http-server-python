[![progress-banner](https://backend.codecrafters.io/progress/http-server/8ffde7bc-69d4-4220-8665-1bb2cac894b9)](https://app.codecrafters.io/users/codecrafters-bot?r=2qF)

["Build Your Own HTTP server" Challenge](https://app.codecrafters.io/courses/http-server/overview).

[HTTP](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol) is the
protocol that powers the web. l have built a HTTP/1.1 server
that is capable of serving multiple clients.

## Features

- **Echo Route**: The server can echo back any message sent to the `/echo` route, demonstrating basic request handling.
- **User-Agent Detection**: It detects and returns the `User-Agent` string of the client, showcasing header parsing.
- **File Handling**: Capable of serving files from a specified directory and handling `GET` and `POST` requests to read and write file contents.
- **Concurrent Connections**: Uses non-blocking sockets to handle multiple connections concurrently.

## How to Use

To get the server up and running, follow these steps:

1. Ensure you have Python 3.11 installed on your system.
2. Clone the repository to your local machine.
3. Ensure you have `python (3.11)` installed locally
4. Navigate to the project directory and run the server using the command: `./your_program.sh` or `python3 main.py`
