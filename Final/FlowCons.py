import time
import threading
from TokenBucket import TokenBucket


class Bit_stream_cons(threading.Thread):
    
    def __init__(self,rate: int, size: int, on_time: int, time_off: int):
        super().__init__()
        self.size = size
        self._stop_event = threading.Event()
        self.bucket = None
        self.on_time = on_time
        self.packet_number = rate
        self.rate = on_time / rate-on_time / rate * 0.005
        self.time_off = time_off

    def addBucket(self, bucket: TokenBucket):
        self.bucket = bucket
        bucket.add(self.packet_number, self.size, self.on_time, self.time_off)

    def run(self):
        while not self._stop_event.is_set():
            time_turned_on = time.perf_counter()
            time_pom = time.perf_counter()
            last_consume_time = time.perf_counter()
            while time_pom - time_turned_on < self.on_time:
                if time_pom >= last_consume_time + self.rate:
                    self.bucket.consume(self.size)
                    last_consume_time += self.rate
                time_pom = time.perf_counter()
            time.sleep(self.time_off)

    def stop(self):
        self._stop_event.set()

