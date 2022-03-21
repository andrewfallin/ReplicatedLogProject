from threading import Thread
import node

if __name__ == '__main__':
    node = node.Node("Node_2", 2, "172.31.80.8", 1, 4000, [
        ('Node_1', '54.167.202.218', 4000),
        ('Node_3', '18.207.242.175', 4000),
        ('Node_4', '3.80.120.27', 4000),
        ]
    )
    print('Starting thread 1 (event listener):')
    worker_2 = Thread(target=node.receive, args=())
    worker_2.start()

    print('Starting thread 2 (sender):')
    worker_1 = Thread(target=node.run, args=())
    worker_1.start()