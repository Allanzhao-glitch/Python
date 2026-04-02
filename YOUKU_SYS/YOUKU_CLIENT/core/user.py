from conf import settings
from libs.common import *
import os,time

user_info = {
    "cookies":None
}

def register(conn):
    username = input("请输入用户名:\n")
    pwd = input("请输入密码:\n")
    re_pwd = input("请确认密码:\n")
    
    if pwd != re_pwd:
        print("两次密码不一致")
        return
    send_dic = {
        "type":"register",
        "user_type":"user",
        "user_name":username,
        "pwd":pwd,
    }
    back_dic = send_msg(send_dic, conn)
    print(back_dic.get("msg"))


def login(conn):
    username = input("请输入用户名:\n")
    pwd = input("请输入密码:\n")
    send_dic = {
        "type":"login",
        "user_type":"user",
        "user_name":username,
        "pwd":pwd,
    }
    back_dic = send_msg(send_dic, conn)
    if back_dic.get("flag"):
        user_info["cookies"] = back_dic.get("session")
        user_info["is_vip"] = back_dic.get("is_vip")
    print(back_dic.get("msg"))


def pay_vip(conn):
    if user_info.get("is_vip"):
        print("已经是会员了")
        return

    send_dic = {
        "type": "pay_vip",
        "session": user_info.get("cookies"),
    }
    back_dic = send_msg(send_dic, conn)
    print(back_dic.get("msg"))
    if back_dic.get("flag"):
        user_info["is_vip"] = 1


def show_movie(conn):
    send_dic = {
        "type": "get_movie_list",
        "session": user_info.get("cookies"),
        "is_free": 2
    }
    back_dic = send_msg(send_dic, conn)
    if back_dic.get("flag"):
        movie_list = back_dic.get("msg")
        for index, movie in enumerate(movie_list):
            print(index, movie)
    else:
        print(back_dic.get("msg"))


def download_free_movie(conn):
    send_dic = {
        "type": "get_movie_list",
        "session": user_info.get("cookies"),
        "is_free": 1
    }
    back_dic = send_msg(send_dic, conn)
    if back_dic.get("flag"):
        movie_list = back_dic.get("msg")
        for index, movie in enumerate(movie_list):
            print(index, movie)
        choice = input("请输入要下载的电影编号:\n")
        if choice.isdigit() and int(choice) in range(len(movie_list)):
            choice = int(choice)

            if not user_info.get("is_vip"):
                print("开通会员，跳过广告")
                time.sleep(5)

            movie_info = movie_list[choice-1]
            movie_id = movie_info[0]
            send_dic = {
                "type": "download_movie",
                "session": user_info.get("cookies"),
                "movie_id": movie_id,
            }
            back_dic = send_msg(send_dic, conn)
            movie_name = back_dic.get("movie_name")
            movie_path = os.path.join(settings.UPLOAD_MOVIE_PATH, movie_name)
            movie_size = back_dic.get("movie_size")
            print(f"正在下载{movie_name}，大小为{movie_size}字")
            recv_len = 0
            with open(movie_path, "wb")as f:
                while recv_len < movie_size:
                    recv_data = conn.recv(1024)
                    f.write(recv_data)
                    recv_len += len(recv_data)
            print("下载成功")
        else:
            print("输入错误")
    else:
        print(back_dic.get("msg"))



def download_pay_movie(conn):
    if not user_info.get("is_vip"):
        print("会员才可以下载收费电影")
        return

    send_dic = {
        "type": "get_movie_list",
        "session": user_info.get("cookies"),
        "is_free": 2
    }

    back_dic = send_msg(send_dic, conn)
    if back_dic.get("flag"):
        movie_list = back_dic.get("msg")
        for index, movie in enumerate(movie_list):
            print(index, movie)
        choice = input("请输入要下载的电影编号:\n")
        if choice.isdigit() and int(choice) in range(len(movie_list)):
            choice = int(choice)
            movie_info = movie_list[choice-1]
            movie_id = movie_info[0]
            send_dic = {
                "type": "download_movie",
                "session": user_info.get("cookies"),
                "movie_id": movie_id,
            }
            back_dic = send_msg(send_dic, conn)
            movie_name = back_dic.get("movie_name")
            movie_path = os.path.join(settings.UPLOAD_MOVIE_PATH, movie_name)
            movie_size = back_dic.get("movie_size")
            recv_len = 0
            with open(movie_path, "wb")as f:
                while recv_len < movie_size:
                    recv_data = conn.recv(1024)
                    f.write(recv_data)
                    recv_len += len(recv_data)
            print("下载成功")
        else:
            print("输入错误")
    else:
        print(back_dic.get("msg"))
           

def show_movie_record(conn):
    send_dic = {
        "type": "show_movie_record",
        "session": user_info.get("cookies"),
    }
    back_dic = send_msg(send_dic, conn)
    if back_dic.get("flag"):
        record_list = back_dic.get("msg")
        for index, record in enumerate(record_list):
            print(index, record)
    else:
        print(back_dic.get("msg"))

def show_notice(conn):
    send_dic = {
        "type": "show_notice",
        "session": user_info.get("cookies"),
    }
    back_dic = send_msg(send_dic, conn)
    if back_dic.get("flag"):
        movie_list = back_dic.get("msg")
        for index, movie in enumerate(movie_list):
            print(index, movie)
    else:
        print(back_dic.get("msg"))

def view(conn):
    func_dic = {
        "1":register,
        "2":login,
        "3":pay_vip,
        "4":show_movie,
        "5":download_free_movie,
        "6":download_pay_movie,
        "7":show_movie_record,
        "8":show_notice,
    }
    while 1:
        print(settings.user_msg)
        choice = input("请输入功能编号")
        if choice == "q":
            user_info["cookies"] = None
            user_info["is_vip"] = None
            break
        if choice in func_dic:
            func_dic[choice](conn)