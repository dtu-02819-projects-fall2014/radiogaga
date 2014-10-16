# -*- coding: utf-8 -*-
"""
Created on Sun Oct 12 20:05:42 2014

@author: Rasmus
"""
import urllib2 as ul
import json
import MySQLdb
import sys
import time as t

station = 'P3'

def mining_station(station):
    address = {"http":"http://www.dr.dk/playlister/feeds/nowNext/nowPrev.drxml?items=1&cid=%s" % station}
    headers = {'User-agent':'Mozilla/5.0'}
    prox = ul.ProxyHandler(address)
    opener = ul.build_opener(prox, ul.HTTPHandler(debuglevel=0))
    ul.install_opener(opener)
    
    req = ul.Request(address["http"],None,headers)
    data = ul.urlopen(req).read()
    
    try:
        json_data = json.loads(data)
        
        if not 'no_music' in json_data['now']['status']:
            track_title = json_data['now']['track_title']
            track_artist = json_data['now']['display_artist']
            play_time = json_data['now']['start_time']
            return (track_title, track_artist, play_time)
    except:
        print 'No json'


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
        


    

if True:
    #Set up a MySQL connection
    try:
        db = MySQLdb.connect(host="localhost", user="root", passwd="",db="radiogaga")
        cursor = db.cursor()
    except:
        sys.exit("No connection to MySQL")    
    
    #Get data from station
    try:
        play_data = mining_station(station)
    except:
        print 'No data to retrieve'
    
    play_status = 'music'
    
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
        
    
    bpm = -1
    temper = -1
    
    #Get the element from the db; it may or may not jet exist
    if play_status is 'music':
        element = getElementFromDB(track,artist)
    
    if play_status is 'music':
        try:
            time_stamp = element[0][2]
            time_array = time_stamp.split(',')
            l = len(time_array)
            last_time = unicode(time_array[l-1])
            
            if not last_time == play_time:
                updated_time = time_stamp + ',' + play_time
                updateElementDB(track,artist,updated_time)
        except:
            insertElementDB(track,artist,play_time,bpm,temper)
    
    #Always close connection to the db
    db.close()
    print(play_data)
    
    #t.sleep(30)
    
    