import socket
import pickle

sock = socket.socket()
sock.bind(('', 8080))
sock.listen(1)
conn, addr = sock.accept()

print('Connected', addr)

data = []
header = conn.recv(16)

msg_len = int.from_bytes(header, byteorder='big')

#print('target_packet_count', target_packet_count)
print('bytes expected', msg_len)

bytes_recd = 0
while bytes_recd < msg_len:
#while True:
#for i in range(target_packet_count+3):
    #print("true, continuing")
    packet = conn.recv(min(msg_len - bytes_recd,
                                  1024))
    #print("caught something!")
    if not packet:
        raise RuntimeError("ERROR сука сука")

    data.append(packet)
    bytes_recd += len(packet)



#print(packet_count, "pacets received, loading original file.")
p = pickle.loads(b"".join(data))
#p = pickle.loads(data)

print("Original file restored, starting transcribtion")
p.Transcribe()
print("Transcribtion finished, sending back!")





data = pickle.dumps(p)

num_parts = (len(data)//1024)
if len(data)%1024!=0: num_parts+=1

conn.send(num_parts.to_bytes(16, byteorder='big') + data)
#sock.send(b'0')
print("sent", num_parts, "packets that's all, sleeping")




conn.close()
print("Thats all folks!")