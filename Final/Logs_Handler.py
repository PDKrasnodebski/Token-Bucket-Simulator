import threading
import time, datetime
import os


class logs_handler:

    def __init__(self, id: int):
        self.id = id
        self.lock = threading.Lock()
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.relative_path = os.path.join(self.current_dir,"logs","txt")
        self.clear_logs()
       

    def clear_logs(self):
        try:
            self.lock.acquire() 
            with open(f"{self.relative_path}/logs_{self.id}.txt", 'w') as file:
                    file.truncate(0)
            self.lock.release()  
        except IOError as e:
            print("Error occured, could not clear previous logs", str(e))   

    def write_log(self, log: str):
        try:
            self.lock.acquire() 
            with open(f"{self.relative_path}/logs_{self.id}.txt", 'a') as file:
                file.write(f"{log}  {datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')}\n")

            self.lock.release()  
        except IOError as e:
            print("Error occured, could not save logs to file", str(e))