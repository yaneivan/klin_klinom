import socket
import pickle
from datetime import datetime

sock = socket.socket()
sock.bind(('', 8080))
sock.listen(1)



whitelist = ['192.162.251.214', 
'192.162.250.228', 
'192.162.251.32', 
'192.162.251.233']

for ip3 in range(256):
    for ip4 in range(256):
        whitelist.append('192.168.'+str(ip3)+'.'+str(ip4))

print("Waiting for input...")

while True:
    conn, addr = sock.accept()
    print('Connected', addr, "Address[0] type is", type(addr[0]), "The time is now:", datetime.now().strftime(('%Y-%m-%d %H:%M:%S')))

    if not( addr[0] in whitelist):
        print("Pendos, detected, access denied, IP:", addr)
        conn.close()
        continue

    data = []
    header = conn.recv(16)
    msg_len = int.from_bytes(header, byteorder='big')
    print('MBytes expected', msg_len//1024//1024)
    bytes_recd = 0
    while bytes_recd < msg_len:
        print("Downloading...", round((bytes_recd/msg_len)*100), "%", end='\r')
        packet = conn.recv(min(msg_len - bytes_recd, 1024))
        if not packet:
            raise RuntimeError("NO packet error")

        data.append(packet)
        bytes_recd += len(packet)



    #print(packet_count, "pacets received, loading original file.")
    p = pickle.loads(b"".join(data))
    #p = pickle.loads(data)

    print("Original file restored, starting transcribtion")
    p.Transcribe()
    print("Transcribtion finished, sending back!")





    data = pickle.dumps(p)

    msg_len = len(data)

    conn.send(msg_len.to_bytes(16, byteorder='big') + data)
    print("sent", msg_len//1024//1024, "MBytes that's all, sleeping")




    conn.close()
    print("Thats all folks!")


    print('\n'*3)