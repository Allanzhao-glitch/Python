import json,struct,hashlib,uuid
from db import user_data

def recv_msg(conn):
    head = conn.recv(4)
    data_len = struct.unpack("i",head)[0]
    recv_data = conn.recv(data_len)
    back_dic = json.loads(recv_data)
    return back_dic