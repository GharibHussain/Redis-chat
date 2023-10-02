import redis 
import group
import message
import user
from datetime import datetime
import time
import threading



def publisher(chat_obj, group_name, sender_name):
    while True:
        text = input('Write your message: ')

        if text == 'q':
            chat_obj.main_menu()

        t = datetime.now()
        #create message key
        sent_at = f'{t.year}-{t.month}-{t.day}-{t.hour}:{t.minute}:{t.second}'
        message_key = f'{group_name}-{sender_name}-{sent_at}'
        print(message_key)

        #time.sleep(1)
     
        #may need multi-threading      
        
        group.save_message(group_name, message_key)
        message.create_message(group_name, sender_name, text, sent_at, message_key)
        group.groups_db.publish(group_name, message_key)

        time.sleep(1)



def run_pubsub(chat_obj, group_name, sender_name, pubsub):

    threading.Thread(target=publisher, args=(chat_obj, group_name, sender_name, )).start()
    
    for item in pubsub.listen():
        if type(item['data']) != int:
            message_key = item['data'].decode('utf-8')
            
            # retrieve the message from messages_db
            received_message = message.load_message_from_db(message_key)
            if received_message != None:
                sender, sent_at, text = received_message
                print(f'[{sent_at}] {sender} ({group_name}): {text}')

            


def load_channels(user_name, pubsub):
    groups = user.list_user_groups(user_name)
    if len(groups) != 0:
        for group_name in groups:
            pubsub.subscribe([group_name])