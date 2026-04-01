
from db.models_sqlalchemy import db, User, Movie, Notice, DownloadRecord


class SQLControl:
    sql_obj = None
    
    def __new__(cls, *args, **kwargs):
        if not cls.sql_obj:
            cls.sql_obj = object.__new__(cls)
        return cls.sql_obj
    
    def __init__(self):
        self.session = db.session
    
    def select(self, model, **kwargs):
        print(f"查询 {model.__tablename__}: {kwargs}")
        query = self.session.query(model)
        if kwargs:
            query = query.filter_by(**kwargs)
        res = query.all()
        return [obj.to_dict() for obj in res]
    
    def select_one(self, model, **kwargs):
        print(f"查询单条 {model.__tablename__}: {kwargs}")
        query = self.session.query(model)
        if kwargs:
            query = query.filter_by(**kwargs)
        obj = query.first()
        return obj.to_dict() if obj else None
    
    def execute(self, obj):
        print(f"插入/更新: {obj.__class__.__tablename__}")
        self.session.add(obj)
        self.session.commit()
    
    def delete(self, model, **kwargs):
        print(f"删除 {model.__tablename__}: {kwargs}")
        query = self.session.query(model)
        if kwargs:
            query = query.filter_by(**kwargs)
        query.delete()
        self.session.commit()
    
    def update(self, model, update_dict, **kwargs):
        print(f"更新 {model.__tablename__}: {kwargs} -> {update_dict}")
        query = self.session.query(model)
        if kwargs:
            query = query.filter_by(**kwargs)
        query.update(update_dict)
        self.session.commit()
    
    def close(self):
        self.session.close()
    
    def get_user(self, user_id=None, user_name=None):
        if user_id:
            return self.select_one(User, user_id=user_id)
        elif user_name:
            return self.select_one(User, user_name=user_name)
        return None
    
    def get_movie(self, movie_id=None, movie_name=None):
        if movie_id:
            return self.select_one(Movie, movie_id=movie_id)
        elif movie_name:
            return self.select_one(Movie, movie_name=movie_name)
        return None
    
    def get_notice(self, n_id=None):
        if n_id:
            return self.select_one(Notice, n_id=n_id)
        return None
    
    def get_all_movies(self, is_delete=0):
        return self.select(Movie, is_delete=is_delete)
    
    def get_all_notices(self):
        return self.select(Notice)
    
    def get_user_movies(self, user_id):
        return self.select(Movie, user_id=user_id, is_delete=0)
    
    def get_user_download_records(self, user_id):
        return self.select(DownloadRecord, user_id=user_id)
    
    def add_user(self, user_name, pwd, user_type='user', is_vip=0, is_locked=0):
        user = User(
            user_name=user_name,
            pwd=pwd,
            user_type=user_type,
            is_vip=is_vip,
            is_locked=is_locked
        )
        self.execute(user)
        return user.to_dict()
    
    def add_movie(self, movie_name, user_id, file_md5=None, path=None, is_free=0):
        movie = Movie(
            movie_name=movie_name,
            user_id=user_id,
            file_md5=file_md5,
            path=path,
            is_free=is_free
        )
        self.execute(movie)
        return movie.to_dict()
    
    def add_notice(self, title, content, user_id):
        notice = Notice(
            title=title,
            content=content,
            user_id=user_id
        )
        self.execute(notice)
        return notice.to_dict()
    
    def add_download_record(self, user_id, movie_id):
        record = DownloadRecord(
            user_id=user_id,
            movie_id=movie_id
        )
        self.execute(record)
        return record.to_dict()
    
    def update_user(self, user_id, **kwargs):
        return self.update(User, kwargs, user_id=user_id)
    
    def update_movie(self, movie_id, **kwargs):
        return self.update(Movie, kwargs, movie_id=movie_id)
    
    def delete_movie(self, movie_id):
        return self.update(Movie, {'is_delete': 1}, movie_id=movie_id)
    
    def delete_user(self, user_id):
        return self.delete(User, user_id=user_id)