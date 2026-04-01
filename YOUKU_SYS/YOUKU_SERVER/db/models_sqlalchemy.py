from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class Database:
    def __init__(self, db_url='mysql+mysqldb://root:991227@localhost:3306/youku_db'):
        self.engine = create_engine(db_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
    
    def create_tables(self):
        Base.metadata.create_all(self.engine)
    
    def close(self):
        self.session.close()

db = Database()

class User(Base):
    __tablename__ = 'user'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(50), unique=True, nullable=False)
    pwd = Column(String(100), nullable=False)
    register_time = Column(DateTime, default=datetime.now)
    is_vip = Column(Integer, default=0)
    is_locked = Column(Integer, default=0)
    user_type = Column(String(20), default='user')
    
    movies = relationship('Movie', back_populates='user')
    notices = relationship('Notice', back_populates='user')
    download_records = relationship('DownloadRecord', back_populates='user')
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'pwd': self.pwd,
            'register_time': self.register_time.strftime('%Y-%m-%d %H:%M:%S') if self.register_time else None,
            'is_vip': self.is_vip,
            'is_locked': self.is_locked,
            'user_type': self.user_type
        }

class Movie(Base):
    __tablename__ = 'movie'
    
    movie_id = Column(Integer, primary_key=True, autoincrement=True)
    movie_name = Column(String(100), nullable=False)
    is_free = Column(Integer, default=0)
    is_delete = Column(Integer, default=0)
    file_md5 = Column(String(32), unique=True)
    path = Column(String(255))
    upload_time = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    
    user = relationship('User', back_populates='movies')
    download_records = relationship('DownloadRecord', back_populates='movie')
    
    def to_dict(self):
        return {
            'movie_id': self.movie_id,
            'movie_name': self.movie_name,
            'is_free': self.is_free,
            'is_delete': self.is_delete,
            'file_md5': self.file_md5,
            'path': self.path,
            'upload_time': self.upload_time.strftime('%Y-%m-%d %H:%M:%S') if self.upload_time else None,
            'user_id': self.user_id
        }

class Notice(Base):
    __tablename__ = 'notice'
    
    n_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    content = Column(String(500))
    create_time = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    
    user = relationship('User', back_populates='notices')
    
    def to_dict(self):
        return {
            'n_id': self.n_id,
            'title': self.title,
            'content': self.content,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None,
            'user_id': self.user_id
        }

class DownloadRecord(Base):
    __tablename__ = 'download_record'
    
    download_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    movie_id = Column(Integer, ForeignKey('movie.movie_id'))
    download_time = Column(DateTime, default=datetime.now)
    
    user = relationship('User', back_populates='download_records')
    movie = relationship('Movie', back_populates='download_records')
    
    def to_dict(self):
        return {
            'download_id': self.download_id,
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'download_time': self.download_time.strftime('%Y-%m-%d %H:%M:%S') if self.download_time else None
        }

if __name__ == '__main__':
    db.create_tables()
    print('数据库表创建成功！')
    
    session = db.session
    
    user = User(user_name='test', pwd='123456', is_vip=1, user_type='admin')
    session.add(user)
    session.commit()
    
    users = session.query(User).filter_by(user_name='test').all()
    for u in users:
        print(u.to_dict())
    
    db.close()