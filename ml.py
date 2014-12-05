r"""
Machine learning - Radiogaga.

This file belongs to Joachim Blom Hansen, Rasmus Jessen Aaskov and Soren
Trads Steen.
"""

import numpy as np
from sklearn.decomposition import PCA


def do_pca(radiokanal, time, connection):
    """Compute PCA and return data projected onto 2 principal directions.

    Arguments:
        radiokanal: the radio channel to be examined.
        time: ex '%2014-11-11%'.
        connection: connection to database, see class MySQLConnection.

    Output:
        a NumPy array with track and artist in two first columns and the
         projection onto the principal directions in the last two.
        .csv files with radio station followed by:
            X.csv includes only bpm and moods.
            X_pca.csv includes only first two PCA coordinates.
            Y_pca.csv includes track, artist and PCA coordinates.

    """
    sqlstring = """SELECT track, artist, bpm, angry, happy, relaxed, sad
                 FROM {0} WHERE history LIKE {1} AND bpm NOT IN (0) AND
                 angry NOT IN (0) """.format(radiokanal, time)
    connection.cursor.execute(sqlstring)
    data = connection.cursor.fetchall()
    Y = np.array(data)
    X = Y[:, 2:]
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    Y_pca = np.concatenate((Y[:, :2], X_pca), axis=1)
    np.savetxt(str(radiokanal)+'_Y_pca.csv', Y_pca, delimiter=',', fmt="%s")
    np.savetxt(str(radiokanal)+'_X.csv', X, delimiter=',', fmt='%s')
    np.savetxt(str(radiokanal)+'_X_pca.csv', X_pca, delimiter=',', fmt='%s')
    return(Y_pca)


def EJ(a, b):
    """Calculate the Extended Jaccard similarity meassure.

    Arguments:
        a,b: two list of same length

    Output:
        the value of EJ
    """
    numerator = np.dot(a, b)
    denominator = np.sum(np.power(a, 2)) + np.sum(np.power(b, 2)) - numerator
    if np.sum(numerator+denominator) == 0:
        value = 1
    else:
        value = np.divide(numerator, denominator)
    return(value)
