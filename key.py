# -*- coding: utf-8 -*-
import random as ran
import mysqlinterface as my


def unique_key(size):
    """Return a unique key

    Args:
        size: the size of the string returned
    Returns:
        key: the random unique string. Note that there is a possibility of
        creating two identical string. However there is a total of 62^size
        number of possible keys. We recommend size > 9
    """
    # Charset to create keys from
    charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    l = len(charset)-1
    bad_key = 1

    # Get a new seed
    ran.seed()

    while(bad_key > 0):
        # Create key
        key = list()
        for i in range(size):
            r = ran.randint(0, l)
            key.append(charset[r])
        key = "".join(key)

        # Check key
        bad_key = check_key(key)

    return(key)


def check_key(key):
    """
    Check that a key is unique. Returns 1 if so, 0 otherwise
    """
    # Open a new connection
    conn = my.MySQLConnection('ip', 'usr', 'psd', 'db')
    set_of_tables = ['P3', 'P6B', 'P7M', 'RAM']

    # Go through each table
    for table in set_of_tables:
        c = my.radiogaga_db_get(conn, table, {'ukey': key})
        if len(c) > 0:
            return(1)

    # End connection and return answer
    conn.end_connection()
    return(0)