import numpy as np
import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

FPS = 10

i = 0
while True:
    print(i)
    #sock.sendto(i.to_bytes(4, 'little', signed=False), ("127.0.0.1", 5005))
    sock.sendto(np.random.rand(32, 10), ("127.0.0.1", 5005))
    time.sleep(1./FPS) # 30fps

    i += 1
