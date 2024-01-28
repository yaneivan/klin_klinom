import socket
import pickle

sock = socket.socket()
sock.bind(('', 8080))
sock.listen(1)



while True:
    conn, addr = sock.accept()

    print('Connected', addr)

    data = []
    header = conn.recv(16)
    msg_len = int.from_bytes(header, byteorder='big')
    print('bytes expected', msg_len)
    bytes_recd = 0
    while bytes_recd < msg_len:
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
    print("sent", msg_len, "packets that's all, sleeping")




    conn.close()
    print("Thats all folks!")


    print('\n'*3)