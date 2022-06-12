import threading


def work(barrier):
    print("n_waiting = {}".format(barrier.n_waiting))  # 等待的线程数
    bid = barrier.wait()  # 参与者的id，返回0到线程数减1的数值
    print("障碍后运行 {}".format(bid))  # 障碍之后


barrier = threading.Barrier(3)  # 3个参与者，每3个开闸放行

for x in range(6):  # 这里启动线程只能是3的倍数,你可以试5
    threading.Thread(target=work, args=(barrier,)).start()
