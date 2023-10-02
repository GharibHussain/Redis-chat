import redis
from datetime import datetime
import message



groups_db = redis.Redis(host="localhost", port=6379, db=0)



def create_group(group_name, creator, description):
    group = {
              "creator": creator,
              "created_at": datetime.now().__str__(), 
              "description": description,
              "members": "", 
              "load_last_n_hour_messages": ""
              }
    groups_db.hmset(group_name, group)
    #print(groups_database.hgetall("group_name"))


def group_details(group_name):
    number_of_members = 0
    #Get the group details
    creator = groups_db.hget(group_name, "creator")
    if creator != None:
        creator = creator.decode("utf-8")
    created_at = groups_db.hget(group_name, "created_at")
    if created_at != None:
        created_at = created_at.decode("utf-8")
    description = groups_db.hget(group_name, "description")
    if description != None:
        description = description.decode("utf-8")
    members = groups_db.hget(group_name, "members")
    if members != None:
        members = members.decode("utf-8")
        number_of_members = len(members.split("/"))
    #load_last_n_hour_messages = groups_db.hget(group_name, "load_last_n_hour_messages").decode("utf-8")

    #number_of_members = len(members.split("/"))

    #print group details
    print(f'{group_name} Creator: {creator} Created at: {created_at} #Members: {number_of_members}')
    print(f'Description: {description}')
    

    #print(members)
    #print(load_last_n_hour_messages)



def list_group_members(group_name):
    members = groups_db.hget(group_name, "members").decode("utf-8")
    listed_members = []
    if len(members) != 0:
        listed_members = members.split("/")
        return listed_members



def add_member(group_name, user_name):
    members = groups_db.hget(group_name, "members").decode("utf-8")
    if user_name in members:
        print('You are already a member!')
    else:
        members += "/" + user_name
        groups_db.hset(group_name, "members", members)
        print('SUCCESSFUL!')

    #subscribe


def remove_member(group_name, user_name):
    all_members = list_group_members(group_name)
    members = ""

    if user_name in all_members:
        all_members.remove(user_name)

        for m in all_members:
            members += "/" + m
            groups_db.hset(group_name, "members", members)

    else:
        print("Youa are not a member of this group!")    

# return a list of groups (string)
def list_all_groups():
    groups = groups_db.keys()
    groups_list = []
    for i in groups:
        groups_list += [i.decode("utf-8")]
    return groups_list


def load_group_messages(group_name):

    message_keys = get_group_message_keys(group_name) #hh
    all_messages = []

    if len(message_keys) > 0:
        for mk in message_keys:
            all_messages += [message.load_message_from_db(mk)]

    return all_messages


# add a message to the group
def save_message(group_name, message_key):
    message_keys_str = groups_db.hget(group_name, "load_last_n_hour_messages").decode('utf-8')
    message_keys_str += "/" + message_key
      
    
    groups_db.hset(group_name, "load_last_n_hour_messages", message_keys_str)



# return a list of message_keys
def get_group_message_keys(group_name):
    
    message_keys = groups_db.hget(group_name, "load_last_n_hour_messages")
    if message_keys != None:
        message_keys = message_keys.decode("utf-8").split("/")
        return message_keys #list