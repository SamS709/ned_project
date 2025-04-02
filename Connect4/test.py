import multiprocessing
import time

def main():
    print("Hello")
    time.sleep(1)
    print("...world")

p = multiprocessing.Process(target=main)
__name__ = "coucou"
if __name__=="__main__":
    p.start()
    print("coucou")
