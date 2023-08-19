import time
import threading
from Logs_Handler import logs_handler
import datetime


class IDController:

    ID = []

    @staticmethod
    def check(id_to_check: int):

        if id_to_check in IDController.ID:
            new_id = max(IDController.ID)+1
            print(f"ID {id_to_check} is already in use, instead ID {new_id} is going to be set")
            return new_id
        else:
            IDController.ID.append(id_to_check)
            return id_to_check

            

class TokenBucket(threading.Thread):
    def __init__(self, id: int = 1, check_time: int = 2, lostPacketsMeasure: bool = False):
        super().__init__()
        self.ID = IDController.check(id)
        self.LostPacketsMeasure = lostPacketsMeasure
        self.Capacity = 0
        self.Rate = 0
        self.Rate_p = 0
        self.Tokens = 0
        self.Last_refill_time = time.perf_counter()
        self._stop_event = threading.Event()
        self.lock = threading.Lock()
        self.Stream_num = 0 
        self.Refill = 0
        self.Lock_set = False
        self.Last_check = time.perf_counter()
        self.Check_time = check_time
        self.Writer = None
        self.Lost = 0

    def set_logs_handler(self):
        self.Writer = logs_handler(self.ID)
        self.Writer.clear_logs()

    def consume(self, tokens: int):
        self.lock.acquire()
        if tokens <= self.Tokens:
            self.Tokens -= tokens
        else:
            self.Writer.write_log(f"Not enough tokens:")
        self.lock.release()

    def measurement(self):
        self.lock.acquire()
        self.Writer.write_log(f"Tokens: {self.Tokens}")
        self.Refill=0
        self.Consumed = 0
        self.lock.release()

    def set_with_lock(self, rate: int, capacity: int):
        self.lock.acquire()
        self.Capacity = capacity
        self.Rate = rate
        self.Rate_p = 1 / self.Rate
        self.Tokens=self.Capacity
        self.Stream_num += 1
        print(f"Parameters of bucket: rate {self.Rate}, 1/rate {self.Rate_p}, capacity {self.Capacity}")
        self.Lock_set = True
        self.lock.release()

    def release(self):
         self.Lock_set=False

    def add(self, rate, size: int, on_time: int, time_off: int):
        self.lock.acquire()
        if self.Lock_set == False:
            if self.Stream_num == 0:
                self.Capacity = rate * size * 10
                self.Rate = rate * size / (on_time + time_off)
                self.Rate_p = 1 / self.Rate
                self.Tokens = self.capacity - size
                self.Stream_num += 1
                print(f"Parameters of bucket {self.ID}: rate {self.Rate}, 1/rate {self.Rate_p}, capacity {self.Capacity}")
                self.Writer.write_log(f"First current added")
            else:
                self.Capacity += rate * size
                self.Rate += rate * size / (on_time + time_off)
                self.Rate_p = 1/self.Rate
                self.Stream_num += 1
                print(f"Parameters of updated bucket {self.ID}: rate {self.Rate}, 1/rate {self.Rate_p}, capacity {self.Capacity}")
                self.writer.write_log(f"New current added")
        self.lock.release()

        
    def run(self):
                if self.LostPacketsMeasure:
                    pom = 0
                    while not self._stop_event.is_set():
                        if time.perf_counter() > self.Last_refill_time:
                            if self.Tokens < self.Capacity:
                                    self.Tokens += 1
                                    self.Last_refill_time += self.Rate_p
                            else:
                                pom += 1
                                self.Last_refill_time += self.Rate_p
                        if time.perf_counter() > self.Last_check + self.Check_time:
                                    if pom > 0:
                                        print(f"Excess tokens: {pom} {datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')}")
                                        self.Lost += pom
                                    self.Last_check=time.perf_counter()
                                    pom = 0
                else:
                    while not self._stop_event.is_set():

                        if time.perf_counter()>self.Last_refill_time:
                            if self.Tokens < self.Capacity:
                                    self.Tokens += 1
                                    self.Last_refill_time += self.rate_p

    def stop(self):
        self._stop_event.set()
