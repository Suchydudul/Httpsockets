import socket
from _thread import start_new_thread
import threading
import sys

lock = threading.Lock()

def handle_client(conn):
    request = (conn.recv(4221)).decode()
    start_request_line = request.index("GET")
    end_request_line = request.index("\r\n")

    ##start_header_host = end_request_line + 2
    end_header_host = request.find("\r\n",end_request_line+2)
    start_header_user_agent = end_header_host +2 
    end_header_user_agent = request.find("\r\n",end_header_host+3)


    request_line = request[start_request_line:end_request_line].split(" ")
    request_target = request_line[1]

    user_agent = request[start_header_user_agent:end_header_user_agent].split(" ")
    if len(user_agent) >= 2:
        user_agent_target = user_agent[1]


    
    if request_target.startswith("/echo/"):
        target = request_target[6:]
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(target)}\r\n\r\n{target}"
    elif request_target.startswith("/user-agent"):
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent_target)}\r\n\r\n{user_agent_target}/1.2.3"
    elif request_target.startswith("/files"):
        
        file_path = sys.argv[2] + request_target[6:]  
        try:
            with open(file_path) as file:
                file_content = file.read()
            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(file_content)}\r\n\r\n{file_content}"
        except FileNotFoundError:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
    elif request_target == "/":
        response = "HTTP/1.1 200 OK\r\n\r\n"
    else: 
        response = "HTTP/1.1 404 Not Found\r\n\r\n"

    conn.send(response.encode())
    conn.close()


    

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        conn, addr =  server_socket.accept() # wait for client
        start_new_thread(handle_client, (conn,))
    
if __name__ == "__main__":
    main()

