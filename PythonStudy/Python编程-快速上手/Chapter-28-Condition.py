import threading
import time

num = 0
condition = threading.Condition()


class Producer(threading.Thread):
    """ 生产者 ，生产商品，5个后等待消费"""

    def run(self):
        global num
        # 获取锁
        condition.acquire()
        while True:
            num += 1
            print(f'生产了1个，现在有{num}个')
            time.sleep(1)
            if num >= 5:
                print('已达到5个，停止生产')
                # 唤醒消费者费线程
                condition.notify()
                # 等待-释放锁 或者 被唤醒-获取锁
                condition.wait()


class Customer(threading.Thread):
    """ 消费者 抢购商品，每人初始10元，商品单价1元"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 每人初始10块钱
        self.money = 10

    def run(self):
        global num
        while self.money > 0:
            condition.acquire()
            if num <= 0:
                print(f'没货了，{threading.current_thread().name}通知生产者')
                condition.notify()
                condition.wait()
            self.money -= 1
            num -= 1
            print(f'{threading.current_thread().name}消费了1个, 剩余{num}个')
            condition.release()
            time.sleep(1)
        print(f'{threading.current_thread().name}没钱了-停止消费')


if __name__ == '__main__':
    p = Producer(daemon=True)
    c1 = Customer(name='消费者-1')
    c2 = Customer(name='消费者-2')
    p.start()
    c1.start()
    c2.start()
