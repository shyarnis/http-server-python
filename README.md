# HTTP Server

A multi-threaded HTTP Sever using python socket library, capable of handling GET, POST and DELETE requests.

## Features

-   **GET** /echo/{text}
-   **GET** /user-agent
-   **GET** /files/{filename}
-   **POST** /files/{filename}
-   **DELETE** /files/{filename}
-   Supports for the Accept-Encoding and Content-Encoding headers
-   Supports gzip compression scheme

## Requirements

-   python3

## Usage

Run the server with the `--directory` option to specify the directory to where files will be served from.

```bash
./http_server.sh --directory /tmp
```

## Example Requests

The http server should be kept running in a terminal or kept in background, while running following requests.

#### GET /echo/{text}

-   Implementation of `/echo/{str}` which accepts string and returns a response body.

```bash
curl -v http://localhost:8000/echo/helloo
```

#### GET /user-agent

-   Implementation of `/user-agent` endpoint, which reads the User-Agent request header and returns it in the response body.

```bash
curl -v --header "User-Agent: foobar/1.2.3.4" http://localhost:8000/user-agent
```

#### GET /files/{filename}

-   Implementation of `/files/{filename}` endpoint, which returns a requested file to the client.
-   To get `HTTP/1.1 200 OK` as a response, create a file name `filename` under that `--directory`.

```bash
curl -v http://localhost:8000/files/some_file_123
```

#### POST /files/{filename}

-   Implement `POST` method of the `/files/{filename}` endpoint, which accepts text from the client and creates a new file with that text under that `--directory`
-   In this example, this should create a file `file_123` with content of `12345` in `/tmp` directory.

```bash
curl -v --data "12345" -H "Content-Type: application/octet-stream" http://localhost:8000/files/file_123
```

#### DELETE /files/{filename}

-   Implement `DELETE` method of the `/files/{filename}` endpoint, which deletes an existing file under that `--directory`

```bash
curl -v -X DELETE http://localhost:8000/files/file_123
```

#### Accept-Encoding and Content-Encoding headers

-   Support for Accept-Encoding headers that contain multiple compression schemes
-   This http server only supports the `gzip` compression scheme.

```bash
curl -v -H "Accept-Encoding: gzip" http://localhost:8000/echo/abc
```

```bash
curl -v -H "Accept-Encoding: invalid-encoding" http://localhost:8000/echo/abc
```

#### Gzip Compression

```bash
curl -v -H "Accept-Encoding: gzip" http://localhost:8000/echo/any_string | hexdump -C
```

-   To check that your compressed body is correct, you can run
    `echo -n <uncompressed-str> | gzip | hexdump -C`
    -   `<uncompressed-str>` can be any string after endpoint `/echo`
