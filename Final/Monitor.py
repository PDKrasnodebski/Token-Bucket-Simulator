from TokenBucket import TokenBucket
from FlowCons import Bit_stream_cons
import time, datetime
from pathlib import Path
from Logs_Handler import logs_handler
import threading
from CleanerCSV import CleanerCSV


class Monitor(threading.Thread):

    def __init__(self, token_bucket: TokenBucket, currents: list[Bit_stream_cons] = [] , log_freq: int = 1, simulation_time: int = 0):
        super().__init__()
        self.LogFreq = log_freq
        self.SimulationTime = simulation_time
        self.StartTime = time.time()
        self.Bucket = token_bucket
        self.Currents = currents

        if self.Currents:
            for current in self.Currents:
                current.addBucket(self.Bucket)
        self._stop_event = threading.Event()

    def start_observation(self):
        self.Bucket.set_logs_handler()
        if not self.Currents:
            print("List of currents is empty")
            return False
        else:
            self.Bucket
            self.start()
            self.Bucket.start()
            for current in self.Currents:
                current.start()

    def stop_observation(self):
        self.stop()
        self.Bucket.stop()
        for current in self.Currents:
            current.stop()
        CleanerCSV.clean(self.Bucket.ID)
        

    def set_currents(self, currents: list[Bit_stream_cons]):
        self.Currents = currents
        for current in self.Currents:
                current.addBucket(self.Bucket)


    def run(self):
        if self.SimulationTime > 0:
            while not self._stop_event.is_set():
                if time.time() - self.StartTime >= self.SimulationTime:
                    self.stop_observation()
                else:
                    self.Bucket.measurement()
                    time.sleep(self.LogFreq)
        else:

            while not self._stop_event.is_set():
                    self.Bucket.measurement()
                    time.sleep(self.LogFreq)
        
    
    def stop(self):
        self._stop_event.set()

