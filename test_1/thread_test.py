import threading
import time


def A():
    for x in range(10):
        print('Doing task A', x)
        time.sleep(3)
    print('Task A done')


def B():
    for x in range(10):
        print('Doing task B', x)
        time.sleep(7)
    print('Task B done')


w = threading.Thread(target=A)
w.start()
time.sleep(2)
B()
print('Done')
