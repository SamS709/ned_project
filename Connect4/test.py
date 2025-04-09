import multiprocessing
import time


def hello():
    p1 = multiprocessing.Process(target=main)
    p1.start()
    p1.join()
    p2 = multiprocessing.Process(target=main)
    p2.start()

    p2.join()
    print("hellooo")

def main():
    print("Hello")

    time.sleep(1)
    print("...world")

if __name__=="__main__":
    hello()
#__name__ = "coucou"
