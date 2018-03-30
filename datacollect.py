from getpass import getpass


def get_activity():

    activity = input("What event would you like to add? \n")

    return activity

def get_time():

    time = input("How much time would you like to spend on this activity? (hours) \n")
    try:
        int(time)
        return int(time)
    except ValueError:
        print("Not a valid time")
        return get_time()

def pair(activity, time):

    event = (activity,time)

    return event

def add_pair(events, event):

    group = []
    group.append(event)
    group.append(0)
    events.append(group)

    return events

def create_pair(events):

    activity = get_activity()
    time = get_time()
    event = pair(activity, time)
    add_pair(events, event)

def user_input_loop():

    events = []
    flag = True

    while flag:
        create_pair(events)
        flag = get_continue_message()

    return print(events)

def get_continue_message():

    flag = getpass("Would you like to add another? [y,n]")

    if flag == 'y':
        return True
    else:
        return False

if __name__ == "__main__":

    # events = []
    # create_pair(events)
    # create_pair(events)
    # print(events)

    user_input_loop()

    #get_activity()
    #get_time()
