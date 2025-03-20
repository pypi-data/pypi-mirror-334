import threading
import time

class Timer:
    __targetMiliSeconds = 0
    __elapsedTime = 0.0
    __elapsed = False
    def __init__(self, miliseconds = float("inf")):
        self.__targetMiliSeconds = float(miliseconds)
    def Start(self):
        self.__elapsed = True
        timerThread = threading.Thread(target=self.__StartThreadTimer)
        timerThread.start()
    def __StartThreadTimer(self):
        while self.__elapsed:
            self.__elapsedTime = round(self.__elapsedTime + 0.1, 1)
            if self.__elapsedTime >= self.__targetMiliSeconds:
                self.__elapsed = False
            time.sleep(0.1)
    def GetElapsedTime(self):
        return self.__elapsedTime
    def Stop(self):
        self.__elapsed = False