import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """create a database connection to an SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_user(conn,user):
    """
    Create a new activity into the Activities TABLE
    :param conn:
    :param activity:
    :return: user id
    """
    sql = ''' INSERT INTO Users(name, username, password)
                VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    return cur.lastrowid


def create_activity(conn, activity):
    """
    Create a new activity
    :param conn:
    :param activity:
    :return: project id
    """
    sql = ''' INSERT INTO Activities (activity, time_goal, time_done, user_id)
                VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, activity)
    return cur.lastrowid

def update_activity(conn, task):
    """
    update activity, time_goal, and time_done
    :param conn:
    :param activity:
    :return: project id
    """
    sql = ''' UPDATE Activities
                SET activity = ? ,
                    time_goal = ? ,
                    time_done = ?
                WHERE activity = ?
                AND user_id = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)

def delete_activity(conn, id):
    """
    Delete a task by task id
    :param conn: Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    sql = 'DELETE FROM Activities WHERE activity = ? AND user_id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    pass

def delete_all_activities(conn):
    """
    Delete all rows in the activities table
    :param conn: Connection to the SQLite database
    :return:
    """
    sql = 'DELETE FROM Activities'
    cur = conn.cursor()
    cur.execute(sql)

def main():
    database = "activities.db"

    #Creates the table if id didn't already exist
    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS Users (
                                        name text NOT NULL,
                                        username text NOT NULL,
                                        password text
                                        ); """
    sql_create_activities_table = """ CREATE TABLE IF NOT EXISTS Activities (
                                        activity text NOT NULL,
                                        time_goal integer NOT NULL,
                                        time_done integer NOT NULL,
                                        user_id integer NOT NULL,
                                        FOREIGN KEY (user_id) REFERENCES Users (username)
                                    ); """
    #creates the connection
    conn = create_connection(database)

    # Validating the connection
    if conn is not None:
        # create the activities table
        create_table(conn, sql_create_users_table)
        print('Users Table Created')
        create_table(conn, sql_create_activities_table)
        print('Activities Table Created')
    else:
        print("Error! cannot create the database connection.")


    # Adding an event
    with conn:
        # create a new user
        # Name, Username, Password
        user = ('Test_Dummy', 'username','password')
        user_id = create_user(conn, user)

        # tasks
        # activity, time_goal, time_done, user_id
        activity_1 = ('Gardening', 10, 0, user_id)
        activity_2 = ('Sleeping', 28, 10, user_id)

        create_activity(conn, activity_1)
        create_activity(conn, activity_2)

        #Update an activity
        update_activity(conn, ('Sleeping',24,20, "Sleeping", 3))

        #Delete the second activity_1
        #delete_activity(conn, ('Gardening', 2))
    # Query the db. Shows all the activities in table Activities
    cur = conn.cursor()
    cur.execute("SELECT * FROM Activities")
    rows = cur.fetchall()
    for row in rows:
        print(row) #use [0] for just the name

if __name__ == '__main__':
    main()

#conn = sqlite3.connect('database.db')
#print("Opened database successfully");

#conn.execute('CREATE TABLE Activities (activity TEXT, time_goal TEXT, time_done TEXT)')
#print("Table created successfully");



# Print all rows
#cur = conn.cursor()
#cur.execute("SELECT * FROM Activities")
#rows = cur.fetchall()
#for row in rows:
#    print(row)

#conn.close()
