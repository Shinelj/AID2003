"""
process_server 多进程基础并发模型
重点代码
"""
from socket import *
from multiprocessing import Process
from signal import *

# 全局变量
HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST,PORT)

# 处理客户端的具体请求 子进程函数
def handle(connfd):
    while True:
        data = connfd.recv(1024)
        if not data:
            break
        print(data.decode())
        connfd.send(b'OK')
    connfd.close()


# 创建tcp套接字
sockfd = socket()
sockfd.bind(ADDR)
sockfd.listen(5)

signal(SIGCHLD,SIG_IGN) # 交给操作系统处理僵尸进程
print("Listen the port %d"%PORT)
# 循环处理客户端链接
while True:
    try:
        connfd,addr = sockfd.accept()
        print("Connect from",addr)
    except KeyboardInterrupt:
        print("服务结束")
        break

    # 为客户端创建进程
    p = Process(target = handle,args = (connfd,))
    p.daemon = True  # 子进程随父进程退出
    p.start()


sockfd.close()