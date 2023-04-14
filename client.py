import asyncio
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import multiprocessing
import time


frame_recv, frame_send = multiprocessing.Pipe(duplex=False)
frame_recv2, frame_send2 = multiprocessing.Pipe(duplex=False)

class EchoServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        frame_send.send_bytes(data)
        frame_send2.send_bytes(data)

async def main():
    loop = asyncio.get_running_loop()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: EchoServerProtocol(),
        local_addr=("127.0.0.1", 5005))

    executor = ProcessPoolExecutor()
    await asyncio.wait([
        loop.run_in_executor(executor, save_msg, frame_recv),
        loop.run_in_executor(executor, compute_msg, frame_recv2)
    ])

def save_msg(frame_recv):
    while True:
        if frame_recv.poll():
            data = frame_recv.recv_bytes()

            arr = np.frombuffer(data, dtype=np.float32)
            print('saved', arr.shape)

            #print('saved', int.from_bytes(data, 'little', signed=False))
            #time.sleep(0.01)

def compute_msg(frame_recv):
    while True:
        latest_data = None
        while frame_recv.poll():
            latest_data = frame_recv.recv_bytes()
        if not latest_data:
            continue

        arr = np.frombuffer(latest_data, dtype=np.float32)
        print('processed', arr.shape)
        #print('processed', int.from_bytes(data, 'little', signed=False))
        time.sleep(1) # model inference; doesn't block other threads since pytorch releases the GIL in C

if __name__ == "__main__":
    asyncio.run(main())
