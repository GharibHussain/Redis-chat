import redis
from datetime import datetime
import group



messages_db = redis.Redis(host="localhost", port=6379, db=1)



def create_message(group_name, sender_name, text, sent_at, message_key):

    #create message
    message = {"sender": sender_name, 
               "sent_at": sent_at,
               "text": text
               }

    #send
    messages_db.hmset(message_key, message)
    group.save_message(group_name, message_key)


def load_message_from_db(message_key):
    
    all_message_keys = get_all_message_keys()
    if len(all_message_keys) != 0 and message_key in all_message_keys:
    
        sender = messages_db.hget(message_key, 'sender').decode('utf-8')
        sent_at = messages_db.hget(message_key, 'sent_at').decode('utf-8')
        text = messages_db.hget(message_key, 'text').decode('utf-8')

        return sender, sent_at, text

    

def get_all_message_keys():
    all_message_keys = []
    for mk in messages_db.keys():
        all_message_keys += [mk.decode('utf-8')]

    return all_message_keys