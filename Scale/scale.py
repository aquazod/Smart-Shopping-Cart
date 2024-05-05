
import socket,re


HOST = "0.0.0.0"
PORT = 80

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

while True:
    conn, addr = s.accept()
    data = conn.recv(1024)
    w=re.findall(r'\?weight\=(.*)HTTP',str(data))
    print(w[0])

    print("Received data:", data)

    conn.sendall(data)
    conn.close()