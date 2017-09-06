from multiprocessing import Process, Pipe, Queue
from time import sleep

def f(conn, queue):
    print('starting...')
    sleep(2)
    conn.send([42, None, 'hello'])
    sleep(2)
    queue.put('Q hello')
    sleep(2)
    b = conn.recv()
    print(b)

if __name__ == '__main__':
    q = Queue()
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn, q))
    p.start()
    print(q.get())
    print(parent_conn.recv())   # prints "[42, None, 'hello']"
    parent_conn.send('HEllo')
    p.join()