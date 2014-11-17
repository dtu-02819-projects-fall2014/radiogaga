# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 13:55:46 2014

@author: Søren bærbar
"""

import numpy as np
from sklearn.decomposition import PCA

from mqsqlinterface import MySQLConnection
    
conn = MySQLConnection('83.92.40.216', 'bobafett', 'bobafett', 'radiogaga')

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
    
do_pca('p3','%2014%',conn)