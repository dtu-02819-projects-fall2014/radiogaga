r"""
config - Radiogaga.

This file belongs to Joachim Blom Hansen, Rasmus Jessen Aaskov and Soren
Trads Steen.
"""
import csv


def getfromconfig():
    """Return fields from a single line csv file."""
    with open('configuration.csv') as f:
        r = csv.reader(f)
        line = r.next()
    return(line)
