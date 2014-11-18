# -*- coding: utf-8 -*-
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


def radiogaga_db_get(MySQLConnection, table, element):
    """Get element from Radio gaga server interface
    Args:
        MySQLConnection: element of type MySQLConnection
        table: name of the table in database
        element: dictionary of information to search for
    """
    # DB connection
    conn = MySQLConnection

    # Write the mysql command to send to the server.
    s = "SELECT * FROM {0} WHERE ".format(table)
    n = len(element)
    count = 1
    for option in element:
        s = s + "{0} LIKE '{1}'".format(option, element[option])
        count = count + 1
        if count <= n:
            s = s + " AND "

    # Commit the command
    conn.cursor.execute(s)
    answer = conn.cursor.fetchall()
    return(answer)


def radiogaga_db_insert(MySQLconnection, table, element):
    """Insert an element to the radiogaga database

    Args:
        MySQLconnection: element of type MySQLConnection
        talbe: name of the table
        element: dictionary of information to insert
    """
    # DB connection
    conn = MySQLconnection

    # Write the mysql command to send to the server
    # Note that this follows the new PEP 3101 and PEP 249 (DB-API)
    s = "INSERT INTO {0} ("
    s = s.format(table)
    count = 1
    n = len(element)
    for option in element:
        if count == n:
            d = "{0}"
        else:
            d = "{0},"
        d = d.format(option)
        s = s + d
        count = count + 1
    s = s + ") VALUES ("
    count = 1
    for option in element:
        if count == n:
            d = "'{0}'"
        else:
            d = "'{0}',"
        d = d.format(element[option])
        s = s + d
        count = count + 1
    s = s + ")"

    # Commit the command
    conn.cursor.execute(s)
    conn.db.commit()
