# -*- coding: utf-8 -*-
"""
Created on Fri Oct 03 17:59:41 2014

@author: Rasmus
"""
import urllib2 as ul
import json
import MySQLdb
import sys
from gettempo import getbpm


def insertElementDB(track, artist, time, bpm, temper):
    sql_command = """INSERT INTO music(track,artist,time,bpm,temper) 
                     VALUES ('%s','%s','%s',%d,%d)""" % (track,artist,time,bpm,temper)   
    try:
        cursor.execute(sql_command)
        db.commit()
    except:
        print 'ERROR: in insertElementDB'
        db.rollback()
    
def getElementFromDB(track, artist):
    sql_command = """SELECT DISTINCT * FROM music WHERE track='%s' 
                     AND artist='%s'""" % (track,artist)
    cursor.execute(sql_command)
    element = cursor.fetchall()
    return element

def updateElementDB(track,artist,time):
    sql_command = """UPDATE music SET time = '%s' WHERE track='%s'
                     AND artist = '%s'""" % (time,track,artist)
    try:
        cursor.execute(sql_command)
        db.commit()
    except:
        print 'ERROR: in updateElementDB'
        db.rollback()


def mining_station(station):
    url_str = 'http://www.dr.dk/playlister/feeds/nowNext/nowPrev.drxml?items=1&cid=' + station
    ul_req = ul.Request(url_str,headers={'User-agent':'Mozilla/5.0'})
    json_str = ul.urlopen(ul_req).read()
    
    try:
        json_data = json.loads(json_str)
        
        if not 'no_music' in json_data['now']['status']:
            track_title = json_data['now']['track_title']
            track_artist = json_data['now']['display_artist']
            play_time = json_data['now']['start_time']
            return (track_title, track_artist, play_time)
    except:
        #nothing to do
        print('')
    
    
 





#Set up a MySQL connection
try:
    db = MySQLdb.connect(host="localhost", user="root", passwd="",db="radiogaga")
    cursor = db.cursor()
except:
    sys.exit("No connection to MySQL")
        

play_status = 'music'

#Retrieve the json data from broadcaster
play_data = mining_station('P3')
try:
    track = play_data[0].decode('iso-8859-1')
    artist = play_data[1].decode('iso-8859-1')
    play_time = play_data[2]
    
    #Encoding for MySQL
    try:
        track_list = list(track)
        for ch in range(1,len(track_list)):
            if track_list[ch] == u"'":
                track_list[ch] = u"''"
        track = ''.join(track_list)
        
        artist_list = list(artist)
        for ch in range(1,len(artist_list)):
            if artist_list[ch] == u"'":
                artist_list[ch] = u"''"
        artist = ''.join(artist_list)
    except IOError:
        print('IOEroror')
except:
    play_status = 'no music'
    

try:
    bpm = getbpm(artist,track)
    temper = 0 #temp
except:
    bpm = -1
    temper = -1        
   
   
#Get the element from the db; it may or may not jet exist
if play_status is 'music':
    element = getElementFromDB(track,artist)

if play_status is 'music':
    try:
        time_stamp = element[0][2]
        time_array = time_stamp.split('\n')
        l = len(time_array)
        last_time = unicode(time_array[l-1])
        
        if not last_time == play_time:
            updated_time = time_stamp + '\n' + play_time
            updateElementDB(track,artist,updated_time)
    except:
        insertElementDB(track,artist,play_time,bpm,temper)

#Always close connection to the db
db.close()


print(play_data)






