
import threading

def datta():
       while True:
                 print("aaa")

def neha():
       while True:
                 print("bbb")
thread1 = threading.Thread(target=datta)
thread2 = threading.Thread(target=neha)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
