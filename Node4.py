from threading import Thread
import node

if __name__ == '__main__':
    node = node.Node("Node_4", 4, "127.0.0.1", 3, 4003, [
        ('Node_2', '127.0.0.1', 4001),
        ('Node_3', '127.0.0.1', 4002),
        ('Node_1', '127.0.0.1', 4000),
        ]
    )
    print('Starting thread 1 (event listener):')
    worker_2 = Thread(target=node.receive, args=())
    worker_2.start()

    print('Starting thread 2 (sender):')
    worker_1 = Thread(target=node.run, args=())
    worker_1.start()