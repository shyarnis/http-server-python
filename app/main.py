import socket
import concurrent.futures
import sys
import os
import gzip


def client_request(client_socket: socket.socket) -> None:
    request: str = client_socket.recv(1024).decode("utf-8")
    request_data: list[str] = request.split("\r\n")
    path: str = request_data[0].split(" ")[1]
    body: str = request_data[-1]
    request_method: str = request_data[0].split(" ")[0]

    if request_method == "GET":
        response: bytes = get_request_method(path, request_data)

    elif request_method == "POST":
        response: bytes = post_request_method(path, body)

    elif request_method == "DELETE":
        response: bytes = delete_request_method(path)

    else:
        response: bytes = f"HTTP/1.1 405 Method Not Allowed\r\n\r\n".encode()

    client_socket.send(response)
    client_socket.close()


def get_request_method(path: str, request_data: list[str]) -> bytes:
    if path == "/":
        return f"HTTP/1.1 200 OK\r\n\r\n".encode()

    elif path.startswith("/echo/"):
        string: str = path.split("/")[-1]
        # ['', 'echo', 'hello']
        compression_scheme: str = ""

        # find comppresion_scehme from header.
        for header in request_data:
            if header.startswith("Accept-Encoding:"):

                if "gzip" in header:
                    compression_scheme = "gzip"
                    break

        if compression_scheme == "gzip":
            compressed_content: bytes = gzip.compress(string.encode())
            return (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: text/plain\r\n"
                f"Content-Encoding: gzip\r\n"
                f"Content-Length: {len(compressed_content)}\r\n\r\n".encode()
                + compressed_content
            )

        else:
            return (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: text/plain\r\n"
                f"Content-Length: {len(string)}\r\n\r\n{string}".encode()
            )

    elif path.startswith("/user-agent"):
        user_agent: str = request_data[2].split(": ")[1]
        # ['GET /user-agent HTTP/1.1', 'Host: localhost:4221', 'Accept: */*', 'User-Agent: foobar/1.2.3', '', '']
        # ['Accept', '*/*']
        # */*
        return (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Type: text/plain\r\n"
            f"Content-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode()
        )

    elif path.startswith("/files"):
        directory: str = sys.argv[2]
        filename: str = path.split("/")[-1]

        try:
            with open(f"/{directory}/{filename}", "r") as file:
                response_body: str = file.read()
                return (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Type: application/octet-stream\r\n"
                    f"Content-Length: {len(response_body)}\r\n\r\n{response_body}".encode()
                )

        except FileNotFoundError as e:
            return f"HTTP/1.1 404 Not Found\r\n\r\n".encode()

    else:
        return "HTTP/1.1 404 Not Found\r\n\r\n".encode()


def post_request_method(path: str, body: str) -> bytes:
    if path.startswith("/files"):
        directory: str = sys.argv[2]
        filename: str = path.split("/")[-1]
        file_path: str = os.path.join(directory, filename)

        try:
            # with open(f"/{directory}/{filename}", "w") as file:
            with open(file_path, "w") as file:
                file.write(body)
                return f"HTTP/1.1 201 Created\r\n\r\n".encode()

        except FileNotFoundError as e:
            return f"HTTP/1.1 404 Not Found\r\n\r\n".encode()

    return f"HTTP/1.1 400 Bad Request\r\n\r\n".encode()


def delete_request_method(path: str) -> bytes:
    if path.startswith("/files"):
        directory: str = sys.argv[2]
        filename: str = path.split("/")[-1]
        file_path: str = os.path.join(directory, filename)

        if os.path.exists(file_path):
            os.remove(file_path)
            return f"HTTP/1.1 200 OK\r\n\r\n".encode()
        else:
            return f"HTTP/1.1 404 Not Found\r\n\r\n".encode()


def main() -> None:
    server_socket: socket.socket = socket.create_server(
        ("localhost", 8000), reuse_port=True
    )

    with concurrent.futures.ThreadPoolExecutor() as executor:

        while True:
            client_socket, _ = server_socket.accept()
            executor.submit(client_request, client_socket)


if __name__ == "__main__":
    main()
