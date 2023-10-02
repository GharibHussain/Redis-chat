import redis
import group

users_db = redis.Redis(host="localhost", port=6379, db=2)
#p = group.groups_db.pubsub()



def create_user(user_name):
    """Create a new user."""
    group_name = ""
    users_db.sadd(user_name, group_name)
    print("Successful!")




def list_user_groups(user_name):
    """return a list of groups (string)"""
    groups = []
    for i in users_db.smembers(user_name):
        groups += [i.decode("utf-8")]

    return groups



def join_group(group_name, user_name, pubsub):
    #subscribe
    pubsub.subscribe(group_name)
    #add the group to user_db
    users_db.sadd(user_name, group_name)
    #add the member to the group_db
    group.add_member(group_name, user_name)

def leave_group(group_name, user_name, pubsub):
    #unsubscribe
    pubsub.unsubscribe(group_name)
    #remove the group from user_db
    users_db.srem(user_name, group_name)
    #rmove the member from the group_db
    group.remove_member(group_name, user_name)

    

def list_all_users():
    """return a list of all users (string)"""
    users = users_db.keys()
    users_list = []
    for i in users:
        users_list += [i.decode("utf-8")]
    return users_list