# from prometheus_client import start_http_server, Counter
from encodings import utf_8
from time import sleep
import socket
import psutil
import json

HOST = "127.0.0.1"
PORT = 8080

def main():
        while True:
            sleep(3)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.connect((HOST, PORT))
                    print ("Socket successfully created")
                    counter = 1
                    with s:
                        info = {
                            'RAM': psutil.virtual_memory()[2],
                            'CPU': psutil.cpu_percent(4),
                            'DISK': psutil.disk_usage('/')[3]
                        }
                        data = json.dumps(info)       
                        s.send(data.encode("utf_8"))
                        print("Data "+ str(counter) +" sent to server.")
                        counter += 1
                        sleep(5)
                except socket.error as err:
                    print ("Socket creation failed %s" %(err))
                    print("Try again? y/n")
                    inp = input()
                    if(inp == "n"):
                        break
                    else:
                        continue
                
            

# c = Counter('process_failures_total', 'Total numbers of failures')

# def run_task(i):
#     print(1)
#     if i % 2 == 0:
#         c.inc()
#     time.sleep(1)

if __name__ == '__main__':
    main()

