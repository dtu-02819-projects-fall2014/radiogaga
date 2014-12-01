r"""
MySQLinterface - Radiogaga.

This file belongs to Joachim Blom Hansen, Rasmus Jessen Aaskov and Soren
Trads Steen.
"""
import MySQLdb


class MySQLConnection:
    
    r"""Set up a connection to a MySQL sever.
    
    Args:
        address: the address to the mysql server.
        usr: the usename.
        psw: the password.
        dbname: the name of the database.
    """
    
    def __init__(self, host, usr, psw, dbname):
        """Initialize the MySQLConnection class."""
        self.host = host
        self.usr = usr
        self.psw = psw
        self.dbname = dbname
        self.setup_connection()

    def setup_connection(self):
        """Setting up a connection to a MySQL db."""
        self.db = MySQLdb.connect(self.host, self.usr, self.psw, self.dbname)
        self.cursor = self.db.cursor()

    def end_connection(self):
        """Closing the MySQL connection."""
        self.db.close()


def radiogaga_db_get(MySQLConnection, table, element):
    r"""Get element from Radio gaga server interface.
    
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
        s = s + """{0} LIKE "{1}" """.format(option, element[option])
        count = count + 1
        if count <= n:
            s = s + " AND "

    # Commit the command
    conn.cursor.execute(s)
    answer = conn.cursor.fetchall()
    return(answer)


def radiogaga_db_insert(MySQLconnection, table, element):
    r"""Insert an element to the radiogaga database.

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
            d = """ "{0}" """
        else:
            d = """ "{0}","""
        d = d.format(element[option])
        s = s + d
        count = count + 1
    s = s + ")"

    # Commit the command
    conn.cursor.execute(s)
    conn.db.commit()


def radiogaga_db_update(MySQLconnection, table, set_element, where_element):
    r"""Update existing track/artist info.
    
    Args:
        MySQLconnection: element of type MySQLConnection
        table: namem of table
        set_element: element with info to update
        where_element: element with info about which element to update
    """
    conn = MySQLconnection
    
    # Write the mysql command to send to the server
    # Note this follows the new PEP 3101 and PEP 249 (DB-API)
    s = "UPDATE {0} SET "
    s = s.format(table)
    set_n = len(set_element)
    set_count = 1
    for option in set_element:
        if set_count == set_n:
            d = "{0}='{1}'"
        else:
            d = "{0}='{1}', "
        d = d.format(option, set_element[option])
        s = s + d
        set_count = set_count + 1
    s = s + " WHERE "
    where_n = len(where_element)
    where_count = 1
    for option in where_element:
        if where_count == where_n:
            d = """{0}="{1}" """
        else:
            d = """{0}="{1}" AND """
        d = d.format(option, where_element[option])
        s = s + d
        where_count = where_count + 1
    
    # Commit the command
    conn.cursor.execute(s)
    conn.db.commit()
        