from concurrent.futures import thread
from encodings import utf_8
import json
import socket
import threading
from prometheus_client import start_http_server, Counter, Gauge

HOST = "127.0.0.1"
PORT = 8080

ram = Gauge('process_ram_usage', 'ram usage', ['client_number'])
cpu = Gauge('process_cpu_usage', 'cpu usage', ['client_number'])
disk = Gauge('process_disk_usage', 'disk usage', ['client_number'])


def recv_data(conn, num, addr, PORT):
    print(f"Connected by {addr}")
    data = conn.recv(1024).decode("utf_8")
    print(f"[{addr}] {data}")

    client_datas = json.loads(data)
    print(client_datas)
    datas = []
    datas.append(client_datas['RAM'])
    datas.append(client_datas['CPU'])
    datas.append(client_datas['DISK'])

    ram.labels("agent" + str(num)).set(datas[0])
    cpu.labels("agent" + str(num)).set(datas[1])
    disk.labels("agent" + str(num)).set(datas[2])
    conn.close()


def main():
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen(10)
            start_http_server(8000)
            num = 1
            while True:
                conn, addr = s.accept()
                thread = threading.Thread(target = recv_data, args = (conn, num, addr, PORT))
                thread.start()
                print(f"[active clients] {num}")
                num += 1
            
if __name__ == '__main__':
    main()
