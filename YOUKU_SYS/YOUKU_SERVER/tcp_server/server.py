import socket
from concurrent.futures import ThreadPoolExecutor
from interface import common_interface,admin_interface,user_interface
from lib import common
from db import user_data
pool = ThreadPoolExecutor(100)


def run():
    server = socket.socket()
    server.bind(('127.0.0.1',8888))
    server.listen(5)
    while 1:
        conn,addr = server.accept()
        pool.submit(task_socket,conn,addr)

def task_socket(conn,addr):
    while 1:
        try:
            user_dic = common.recv_msg(conn)