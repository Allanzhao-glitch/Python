from db import models_sqlalchemy,user_data
import datetime,os
from libs.common import *
from conf import settings

@login_auth
def pay_vip_interface(user_dic,conn):
    user_obj = models_sqlalchemy.db.session.query(models_sqlalchemy.User).filter_by(user_id=user_dic.get("user_id")).first()
    user_obj.is_vip = 1
    models_sqlalchemy.db.session.commit()
    send_dic = {
        "flag": True,
        "msg": "会员充值成功",
    }
    send_msg(send_dic, conn)


@login_auth
def download_movie_interface(user_dic,conn):
    movie_obj = models_sqlalchemy.db.session.query(models_sqlalchemy.Movie).filter_by(movie_id=user_dic.get("movie_id")).first()
    movie_path = movie_obj.path
    send_dic = {
        "movie_name": movie_obj.movie_name,
        "movie_size": os.path.getsize(movie_path)
    }
    send_msg(send_dic, conn, movie_path)

    download_obj = models_sqlalchemy.DownloadRecord(
        user_id = user_dic.get("user_id"),
        movie_id = user_dic.get("movie_id"),
        download_time = datetime.datetime.now()
    )
    models_sqlalchemy.db.session.add(download_obj)
    models_sqlalchemy.db.session.commit()


@login_auth
def show_movie_record_interface(user_dic,conn):
    movie_list = models_sqlalchemy.db.session.query(models_sqlalchemy.DownloadRecord).filter_by(user_id=user_dic.get("user_id")).all()
    if movie_list:
        movie_info = []
        for obj in movie_list:
            movie_obj = models_sqlalchemy.db.session.query(models_sqlalchemy.Movie).filter_by(movie_id=obj.movie_id).first()
            movie_info.append(
                [movie_obj.movie_name, str(obj.download_time)]
            )
        send_dic = {
            "flag": True,
            "msg": movie_info,
        }
        send_msg(send_dic, conn)
    else:
        send_dic = {
            "flag": False,
            "msg": "没有记录",
        }
        send_msg(send_dic, conn)


@login_auth
def show_notice_interface(user_dic,conn):
    notice_list = models_sqlalchemy.db.session.query(models_sqlalchemy.Notice).all()
    if notice_list:
        notice_info = []
        for obj in notice_list:
            notice_info.append(
                [obj.title, obj.content]
            )
        send_dic = {
            "flag": True,
            "msg": notice_info,
        }
        send_msg(send_dic, conn)
    else:
        send_dic = {
            "flag": False,
            "msg": "没有公告",
        }
        send_msg(send_dic, conn)
