from sqlite3 import Error
import datetime 
import sqlite3


DATABASE_PATH = r"./sqlite.db"


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return conn

 
def create_table(conn):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """

    sql_create_table = """ 
    CREATE TABLE IF NOT EXISTS gionjistar1 (
        id integer     PRIMARY KEY AUTOINCREMENT,
        panel_voltage         real,
        panel_current         real,
        battery_voltage       real,
        battery_current       real,
                                    
        load_voltage          real,
        load_current          real,
        power_input           real,
        power_output          real,
        output_current_plug_1 real,
                                       
        output_current_plug_2 real,
        inverter_current      real,
        irradiation           real,
        time                  timestamp NOT NULL
    ); 
    """

    try:
        c = conn.cursor()
        c.execute( sql_create_table ) as e:
        print(e)


def perform_insert(conn, data):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    data = data + (datetime.datetime.now(),)

    sql = """ 
    INSERT INTO gionjistar1(
        panel_voltage,
        panel_current,
        battery_voltage,
        battery_current,
        load_voltage,

        load_current,
        power_input,
        power_output,
        output_current_plug_1,
        output_current_plug_2,

        inverter_current,
        irradiation,
        time
    )
    VALUES( ?,?,?,?,?, ?,?,?,?,?, ?,?,? ) 
    """

    try:

        cur = conn.cursor()
        cur.execute(sql, data)

        conn.commit()
        conn.close()
    
    except Exception as e:

        print(e)



def select_data_last():
    conn = create_connection( DATABASE_PATH )

    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM gionjistar1 ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()

    conn.close()

    return result



def getLastData():

    data = dict()

    result = select_data_last()

    if result != None:
        data['panel_voltage'] = result[1]
        data['panel_current'] = result[2]
        data['battery_voltage'] = result[3]
        data['battery_current'] = result[4]
        data['load_voltage'] = result[5]
        data['load_current'] = result[6]
        data['power_input'] = result[7]
        data['power_output'] = result[8]
        data['output_current_plug_1'] = result[9]
        data['output_current_plug_2'] = result[10]
        data['inverter_current'] = result[11]
        data['irradiation'] = result[12]
        data['time'] = result[13]
    else:
        data = None

    return data



def select_data(conn, start, end):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    conn = create_connection( DATABASE_PATH )
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM gionjistar1 WHERE time >= ? AND time <= ?", (start, end))
 
    rows = cur.fetchall()
 
    conn.close()    

    return rows


def select_data_all():
    conn = create_connection( DATABASE_PATH )
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM gionjistar1 ")

    rows = cur.fetchall()

#    print( len(rows) )

#    for row in rows:
#        print(row)
    
    conn.close()

    return rows


def init():

    conn = create_connection( DATABASE_PATH )

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn)
    else:
        print("Error! cannot create the database connection.")

    conn.close()



def insert_data(data):

    conn = create_connection(DATABASE_PATH)

    if conn is not None:
        perform_insert(conn, data)
    else:
        print("Error! cannot create db connection")

    conn.close()


def main():

    DATABASE_PATH = r"./sqlite.db"
 
    sql_create_gionji_table = """ 
    CREATE TABLE IF NOT EXISTS gionjistar1 (
        id integer PRIMARY KEY,
        panel_voltage         real,
        panel_current         real,
        battery_voltage       real,
        battery_current       real,
        load_voltage          real,
        load_current          real,
        power_input           real,
        power_output          real,
        output_current_plug_1 real,
        output_current_plug_2 real,
        inverter_current      real,
        irradiation           real,
        time                  timestamp NOT NULL
    ); 
    """
 
    # create a database connection
    conn = create_connection(DATABASE_PATH)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_gionji_table)
    else:
        print("Error! cannot create the database connection.")

    data = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, datetime.datetime.now())

    create_task(conn, data)