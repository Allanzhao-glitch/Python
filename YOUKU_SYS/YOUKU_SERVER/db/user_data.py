from threading import Lock

online_user = {}
mutex = Lock()

def add_online_user(user_id, conn):
    with mutex:
        online_user[user_id] = conn

def remove_online_user(user_id):
    with mutex:
        if user_id in online_user:
            del online_user[user_id]

def get_online_user(user_id):
    with mutex:
        return online_user.get(user_id)

def is_user_online(user_id):
    with mutex:
        return user_id in online_user

def get_all_online_users():
    with mutex:
        return list(online_user.keys())