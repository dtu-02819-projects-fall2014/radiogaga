# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 16:21:07 2014

@author: Søren bærbar
"""


from gettempo import getbpm
import MySQLdb
import time

db = MySQLdb.connect(host="ip",user="user", passwd="pass",db="dbname")
cursor = db.cursor()


cursor.execute("SELECT * FROM p3 WHERE bpm = -1")

for row in cursor:
  track = str(row[0])
  artist = str(row[1])
  print(row)
  bpm = getbpm(artist,track)
  print('BPM lykkedes')
  sql_command = """UPDATE p3 SET bpm = '%s' WHERE track='%s'
                     AND artist = '%s'""" % (bpm,track,artist)
  try:
      cursor.execute(sql_command)
      db.commit()
  except:
      print 'ERROR: in update BPM'
      db.rollback()
  time.sleep(10) # to avoid error 429: too many requests. Hack
  
db.close()
