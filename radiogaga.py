# -*- coding: utf-8 -*-
import urllib2 as ul
import json
import MySQLdb
import sys
import time as t
import sys
from GetScore import GetScore
from radioplay import radioplay
from gettempo import getbpm

live = ''
stations = ['p3','p7m','thevoice','novafm','popfm']
stationcodes = {'p3':'P3','p7m':'P7M','thevoice':17,'novafm':18,'popfm':19}

#Handle cammand arguments
call = list(sys.argv)
try:
    if call[1] in stations:
        live = call[1]
    else:
        sys.exit('Error in command. No such station was found')
except:
    live = 'p3'
    print('Error in command. You have to specify the name of the station')
        

def mining_station(station):
    #Only DR radio stations
    if station == 'p3' or station == 'p7m':
        address = {"http":"http://www.dr.dk/playlister/feeds/nowNext/nowPrev.drxml?items=1&cid=%s" % stationcodes[station]}  
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
            print 'No json was found' 
    #Other radio stations
    elif station == 'thevoice' or station == 'novafm' or station == 'popfm':
        [artist, title] = radioplay(station)


def insert_element_to_db(station, track, artist, time, lastplay, bpm, angry, relaxed, sad, happy):
    sql_command = """INSERT INTO %s(track,artist,time,lastplay,bpm,angry,relaxed,sad,happy)
                    VALUES ('%s','%s','%s','%s',%d,%d,%d,%d,%d)
                    """ % (track,artist,time,lastplay,bpm,angry,relaxed,sad,happy)
    try:
        cursor.execute(sql_command)
        db.commit()
    except:
        print 'ERROR: in insertElementDB'
        db.rollback()
    
def get_element_from_db(station,track, artist):
    sql_command = """SELECT DISTINCT * FROM %s WHERE track='%s' AND artist='%s'""" % (station,track,artist)
    cursor.execute(sql_command)
    element = cursor.fetchall()
    return element

def update_element_from_db(station,track,artist,time,lastplay,bpm,angry,relaxed,sad,happy):    
    sql_command = """UPDATE %s SET time='%s', lastplay='%s' ,bpm=%d,angry=%d,
                    relaxed=%d,sad=%d,happy=%d WHERE track='%s' AND artist='%s' LIMIT 1
                    """ % (station,time,lastplay,bpm,angry,relaxed,sad,happy,track,artist)  
    try:
        cursor.execute(sql_command)
        db.commit()
    except: 
        print 'ERROR: in updateElementDB'
        db.rollback()



if True:
    #Establish MySQL connection
    try:
        db = MySQLdb.connect(host="83.92.40.216",user="bobafett", passwd="bobafett",db="radiogaga")
        cursor = db.cursor()
    except:
        sys.exit("No connection to MySQL")
        
    
    #Get data from station
    try:
        play_data = mining_station(live)
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

    #Get BPM for song            
    if play_status is 'music':
        try:
            bpm = getbpm(artist, track)
        except:
            print 'bpm failed'
            bpm = -1
            
    #Peform sentiment analysis
    if play_status is 'music':
        try:
            [angry, happy, relaxed, sad] = GetScore(artist,track)
        except:
            print 'get score failed'
            angry = -1
            relaxed = -1
            sad = -1
            happy = -1    
    
    
    #Get the element from the db; it may or may not jet exist
    if play_status is 'music':
        element = get_element_from_db(live,track,artist)
    
    if play_status is 'music':
        try:
            time_stamp = element[0][2]
            time_array = time_stamp.split(',')
            l = len(time_array)
            last_time = unicode(time_array[l-1])
            
            if not last_time == play_time:
                updated_time = time_stamp + ',' + play_time
                update_element_from_db(live,track,artist,updated_time,play_time,bpm,angry,relaxed,sad,happy)
        except:
            insert_element_to_db(live,track,artist,play_time,play_time,bpm,angry,relaxed,sad,happy)
    
    #Always close connection to the db
    db.close()
    if play_status is 'music':
        print(bpm, angry, happy, relaxed, sad, play_data)
    
    #t.sleep(30)