from conf import settings
from libs.common import *
import os,time


user_info = {
    "cookies":None
}

def register(conn):
    user_name = input("请输入账号:\n")
    pwd = input("请输入密码:\n")
    re_pwd = input("请确认密码:\n")
    if pwd != re_pwd:
        print("两次密码不一致")
        return
    
    send_dic = {
        "type":"register",
        "user_type":"admin",
        "user_name":user_name,
        "pwd":pwd,
    }
    back_dic = send_msg(send_dic,conn)
    print(back_dic.get("msg"))


def login(conn):
    user_name = input("请输入账号:\n")
    pwd = input("请输入密码:\n")
    send_dic = {
        "type":"login",
        "user_type":"admin",
        "user_name":user_name,
        "pwd":pwd,
    }
    back_dic = send_msg(send_dic, conn)
    if back_dic.get("flag"):
        user_info["cookies"] = back_dic.get("session")
    print(back_dic.get("msg"))
   