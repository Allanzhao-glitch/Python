from db.models_sqlalchemy import db,Notice,Movie
import datetime,os
from libs.common import *
from conf import settings


@login_auth
def upload_movie_interface(user_dic,conn):
    movie_name = user_dic.get("movie_name")
    movie_path = os.path.join(settings.DOWNLOAD_MOVIES_PATH,movie_name)
    movie_size = user_dic.get("movie_size")
    recv_len = 0
    with open(movie_path,"wb")as f:
        while recv_len<movie_size:
            recv_data = conn.recv(1024)
            f.write(recv_data)
            recv_len += len(recv_data)
    
    movie_obj = Movie(
        movie_name = movie_name,
        is_free=user_dic.get("is_vip"),
        is_delete = 0,
        file_md5 = user_dic.get("movie_md5"),
        path = movie_path,
        upload_time = datetime.datetime.now(),
        user_id = user_dic.get("user_id"),
    )
    db.session.add(movie_obj)
    db.session.commit()

    send_dic = {
        "flag": True,
        "msg": "上传成功",
    }
    send_msg(send_dic, conn)



@login_auth
def delete_movie_interface(user_dic,conn):
    movie_name = user_dic.get("movie_name")
    movie_obj = db.session.query(Movie).filter_by(movie_name=movie_name).first()
    movie_obj.is_delete = 1
    db.session.commit()
    send_dic = {
        "flag": True,
        "msg": "删除成功",
    }
    send_msg(send_dic, conn)


@login_auth
def send_notice_interface(user_dic,conn):
    notice_obj = Notice(
        title = user_dic.get("title"),
        content = user_dic.get("content"),
        user_id = user_dic.get("user_id"),
        create_time = datetime.datetime.now()
    )
    db.session.add(notice_obj)
    db.session.commit()
    send_dic = {
        "flag": True,
        "msg": "发布成功",
    }
    send_msg(send_dic,conn)
