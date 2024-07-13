import multiprocessing
import bot1
import bot2
import bot3

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=bot1.check_rss)
    p2 = multiprocessing.Process(target=bot2.check_rss)
    p3 = multiprocessing.Process(target=bot3.check_rss)
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()