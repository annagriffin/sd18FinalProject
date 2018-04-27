from getpass import getpass

import importlib

import sqlite3
from flask import g

DATABASE = '/path/to/database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

#@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
#moduleName = input('datacollect')
#importlib.import_module(moduleName)


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

def event_name(events, event):
    temp1 = event
    temp2 = list(temp1[0])
    return temp2[0]

def event_progress(events,event):
    progress_bar_length = 50
    event_slice = event
    hours_complete = event_slice[1]
    hours_wanted = list(event_slice[0])[1]
    ratio = hours_complete / hours_wanted
    how_far = int(progress_bar_length * ratio)
    if how_far > progress_bar_length:
        how_far = progress_bar_length
    the_bar = "["+ how_far*"|" + (progress_bar_length-how_far)*" "+"]"
    return the_bar


def display_progress(events):

    for i in events:
        print(event_name(events,i))
        print(event_progress(events,i))

def add_progress(events):
    pos = 1
    print("To which event would you like to add time to?")
    for i in events:
        print(str(pos)+". "+event_name(events,i))
        pos += 1
    event_position = getpass("Event Position:")
    try:
        int(event_position)
        pos = int(event_position)
    except ValueError:
        print("Not a valid position")
        return add_progress(events)

    try:
        0 <= pos <= len(events)
        pos = int(event_position)
    except False:
        print("Not a valid position")
        return add_progress(events)
    event = events[pos-1]
    add_hours = input("How many hours would you like to add?\n")

    try:
        int(add_hours)
        add_hours = int(add_hours)
    except ValueError:
        print("Not a valid time.")
        return add_progress(events)
    event[1] = event[1]+ add_hours


def user_input_loop():

    events = []
    flag = True

    while flag:
        create_pair(events)
        flag = get_continue_message()

    print(events)
    add_progress(events)
    display_progress(events)

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

    #user_input_loop()
    get_db()
    #loop = Activity()


    #get_activity()
    #get_time()
