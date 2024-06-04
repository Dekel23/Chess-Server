import threading
import time

class stop_watch():
    def __init__(self, initial_time):
        self.initial_time = initial_time
        self.current_time = initial_time
        self.is_running = False

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self.run)
            self.thread.start()
    
    def stop(self):
        if self.is_running:
            self.is_running = False
            self.thread.join()
    
    def run(self):
        while self.is_running and self.current_time > 0:
            elapse_time = time.perf_counter() - self.initial_time
            self.current_time = max(0, self.initial_time - elapse_time)
    
    def get_time(self):
        minutes = int(self.remaining_time // 60)
        seconds = int(self.remaining_time % 60)
        return f"{minutes:02d}:{seconds:02d}"
