import group
import message
import user
import pub_sub


class Main_Chat:

    def __init__(self, user_name):
        self.user_name = user_name 
        self.pubsub = group.groups_db.pubsub()#


    def main_menu(self):
        """Display the main menu"""
        print('1. Create a Group ')
        print('2. View All Groups ')
        print('3. View Your Groups ')
        

        option = int(input("Choose an option: "))
        if option == 1:
            self.create_a_group()
        elif option == 2:
            self.view_all_groups()
        elif option == 3:
            self.view_your_groups()
        else: 
            print("Invalid option!")
            self.main_menu()



    def create_a_group(self):
        """Create a group by entering group name"""
        group_name = input('Enter a name for your group: ')

        if group_name in group.list_all_groups():
            print('The group name already exists!')
        else:
            description = input('Group Description: ')

            group.create_group(group_name, self.user_name, description)
            #join/subscribe
            user.join_group(group_name, self.user_name, self.pubsub)
            print('SUCCESSFUL!')

        self.main_menu()



    def view_all_groups(self):
        """Display a list oghf all of the groups and allow the user to join a group"""
        for g in group.list_all_groups():
            group.group_details(g)

        print("+++++++++++++++++++++++++++++++++++++++++++++")    
        group_name = input("Enter a group name to join OR press q to go back: ")
        if group_name == "q":
            self.main_menu()
        else:
            #join/subscribe
            user.join_group(group_name, self.user_name, self.pubsub)
            # main menu
            self.main_menu()



    def view_your_groups(self):
        """Display the groups that the user has joined."""
    
        for g in user.list_user_groups(self.user_name):
            group.group_details(g)

        print("------------------------+ ----- +------------------------")   

    
        group_name = input("Enter a group name OR press q to go back: ")

        if group_name == "q":
            self.main_menu()
        else:
            print("1- View group messages")
            print("2- Leave the group")
            option = int(input('Choose a option: '))

            if option == 1: 
                # group details
                group.group_details(group_name)  
                # group messages        
                self.display_messages(group_name)
                # send a message
            elif option == 2:
                user.leave_group(group_name, self.user_name, self.pubsub)
                print(f'You left {group_name}!')
            else: 
                print("Invalid input. Try again!")
                self.view_your_groups()



    def display_messages(self, group_name):   
        """Display and print the last n-hour messages to the new user"""
    
        print("------------------------+ Messages +------------------------")
        
        # a list of meessage tuples
        all_messages = group.load_group_messages(group_name) # a list of all messages

        #if all_messages != None:
        for m in all_messages:
            if m != None:                      
                sender, sent_at, text = m
                print(f'[{sent_at}] {sender} ({group_name}): {text}')
        # send and get messages
        pub_sub.run_pubsub(self,group_name, self.user_name, self.pubsub) 




def start_app():
    """Start the program"""
    user_name = input("Enter your name: ")
    
    if user_name not in user.list_all_users():
       user.create_user(user_name)

    chat = Main_Chat(user_name)
    pub_sub.load_channels(user_name, chat.pubsub)    
    chat.main_menu()


start_app()