# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 13:55:46 2014

@author: Søren bærbar
"""

import numpy as np
import MySQLdb
from sklearn.decomposition import PCA
from config import getfromconfig

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
line = getfromconfig()
conn = MySQLConnection(line[0], line[1], line[2], line[3])

def do_pca(radiokanal,time,connection):
    """Compute PCA and return data projected onto 2 principal directions.
    
    Arguments:
        radiokanal: the radio channel to be examined.\n
        time: ex '%2014-11-11%'. \n
        connection: connection to database, see class MySQLConnection. 
        
    Output:
        a NumPy array with track and artist in two first columns and the projec-
        tion onto the principal directions in the last two. 
        .csv files with radio station followed by:
            X.csv includes only bpm and moods.
            X_pca.csv includes only first two PCA coordinates.
            Y_pca.csv includes track, artist and PCA coordinates.
    
    """
    sqlstring = """SELECT track, artist, bpm, angry, happy, relaxed, sad 
                FROM %s WHERE time LIKE "%s" AND bpm NOT IN ( -1, 0 ) AND angry
                NOT IN (-1,0)""" % (radiokanal,time)
    connection.cursor.execute(sqlstring)
    data = connection.cursor.fetchall()
    Y = np.array(data)
    X = Y[:,2:]
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    Y_pca = np.concatenate((Y[:,:2],X_pca),axis = 1)
    np.savetxt(str(radiokanal)+'_Y_pca.csv', Y_pca, delimiter = ',',fmt="%s")
    np.savetxt(str(radiokanal)+'_X.csv', X, delimiter = ',', fmt='%s')    
    np.savetxt(str(radiokanal)+'_X_pca.csv', X_pca, delimiter = ',', fmt='%s')        
    return(Y_pca)
    
do_pca('p3','%2014-11-14T11%',conn)