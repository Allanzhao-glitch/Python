from db import models_sqlalchemy,user_data
import datetime
from libs.common import *

def register_interface(user_dic,conn):
    user_list = models_sqlalchemy.db.session.query(models_sqlalchemy.User).filter_by(user_name=user_dic.get("user_name")).all()
    pwd = user_dic.get("pwd")
    if not user_list:
        user_obj = models_sqlalchemy.User(
            user_name = user_dic.get("user_name"),
            pwd = get_pwd_md5(pwd),
            register_time = datetime.datetime.now(),
            is_vip=0,
            is_locked = 0,
            user_type = user_dic.get("user_type"),
        )
        models_sqlalchemy.db.session.add(user_obj)
        models_sqlalchemy.db.session.commit()
        send_dic = {
            "flag": True,
            "msg": "注册成功",
        }
        send_msg(send_dic, conn)
    else:
        send_dic = {
            "flag": False,
            "msg": "注册失败",
        }
        send_msg(send_dic, conn)


def login_interface(user_dic,conn):
    user_list = models_sqlalchemy.db.session.query(models_sqlalchemy.User).filter_by(user_name=user_dic.get("user_name")).all()
    if user_list:
        user_obj = user_list[0]
        user_name = user_obj.user_name
        pwd = user_dic.get("pwd")
        if user_obj.pwd == get_pwd_md5(pwd):
            session = get_session(user_name)
            addr = user_dic.get("addr")
            user_data.mutex.acquire()
            user_data.online_user[addr] = [session,user_obj.user_id]
            user_data.mutex.release()
            print(user_data.online_user)
            send_dic = {
                "flag": True,
                "msg": "登陆成功",
                "session":session,
                "is_vip":user_obj.is_vip
            }
            send_msg(send_dic, conn)
        else:
            send_dic = {
                "flag": False,
                "msg": "登陆失败",
            }
            send_msg(send_dic, conn)
    else:
        send_dic = {
            "flag": False,
            "msg": "登陆失败",
        }
        send_msg(send_dic, conn)


@login_auth
def check_movie_interface(user_dic,conn):
    movie_list = models_sqlalchemy.db.session.query(models_sqlalchemy.Movie).filter_by(file_md5=user_dic.get("movie_md5")).all()
    if not movie_list:
        send_dic = {
            "flag": True,
            "msg": "可以上传",
        }
        send_msg(send_dic, conn)
    else:
        send_dic = {
            "flag": False,
            "msg": "电影已经存在",
        }
        send_msg(send_dic, conn)


@login_auth
def get_movie_list_interface(user_dic,conn):
    movie_list = models_sqlalchemy.db.session.query(models_sqlalchemy.Movie).filter_by(is_delete=0).all()
    if movie_list:
        movie_info = []
        for obj in movie_list:
            if obj.is_free == user_dic.get("is_free") or user_dic.get("is_free")==2:
                movie_info.append(
                    [obj.movie_id,
                     obj.movie_name,
                     "免费" if obj.is_free else "收费"]
                )
        if movie_info:
            send_dic = {
                "flag": True,
                "msg": movie_info
            }
            send_msg(send_dic, conn)
        else:
            send_dic = {
                "flag": False,
                "msg": "没有电影",
            }
            send_msg(send_dic, conn)

    else:
        send_dic = {
            "flag": False,
            "msg": "没有电影",
        }
        send_msg(send_dic, conn)
