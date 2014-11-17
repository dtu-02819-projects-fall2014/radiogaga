# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 00:04:54 2014

@author: Rasmus
"""
import MySQLdb


class MySQLConnection:
    """Set up a connection to a MySQL sever
    Args:
        address: the address to the mysql server.\n
        usr: the usename.\n
        psw: the password.\n
        dbname: the name of the database.
    """
    def __init__(self, host, usr, psw, dbname):
        self.host = host
        self.usr = usr
        self.psw = psw
        self.dbname = dbname
        self.setup_connection()

    def setup_connection(self):
        self.db = MySQLdb.connect(self.host, self.usr, self.psw, self.dbname)
        self.cursor = self.db.cursor()

    def end_connection(self):
        self.db.close()

# The following provide a example for setting up a connection
conn = MySQLConnection('83.92.40.216', 'myusername', 'mypassword', 'db')


def radiogaga_db_get(MySQLConnection, table, element):
    """Get element from Radio gaga server interface
    Args:
        MySQLConnection: element of type MySQLConnection
        table: name of the table in database
        element: dictionary of information to insert holding e.g.
                 element = {'track':'Enter Sandman',\n
                            'artist':'Metallica',\n
                            'time':'2014-9-11T20:02:55',\n
                            'lastplay':'2014-9-11T20:02:55',\n
                            'bpm':120,\n
                            'angry':110,\n
                            'relaxed':23,\n
                            'sad':34,\n
                            'happy':2}
    """
    # DB connection
    conn = MySQLConnection

    # Write the mysql command to send to the server
    sql_command = """SELECT * FROM %s WHERE""" % (table)
    n_element = len(element)
    count = 0
    for option in element:
        sql_command = sql_command + """ %s LIKE "%s"
                                    """ % (option, element[option])
        count = count + 1
        if count < n_element:
            sql_command = sql_command + "AND"

    # Commit the command
    conn.cursor.execute(sql_command)
    answear = conn.cursor.fetchall()
    return answear

# Providing an example for calling the function
element = {'lastplay': '%2014-11-09T%'}
answear = radiogaga_db_get(conn, 'p3', element)
print(answear)
