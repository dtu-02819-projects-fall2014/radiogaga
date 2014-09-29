# -*- coding: utf-8 -*-
import urllib2 as ul
import os
import csv
import json
import time


def mining_station(station):
    url_str = 'http://www.dr.dk/playlister/feeds/nowNext/nowPrev.drxml?items=1&cid=' + station
    ul_req = ul.Request(url_str,headers={'User-agent':'Mozilla/5.0'})
    json_str = ul.urlopen(ul_req).read()
    json_data = json.loads(json_str)
    
    json_output = json.dumps(json_data,indent=True)
    
    with open('out_' + station + '.json','w') as jf:
        jf.write(json_output)
    
    
    #Json file fetched; now use it to analyse/mine
    file_mining = station + '.csv'
    working_dir = os.getcwd()
    file_path = os.path.join(working_dir,file_mining)
    
    
    #Get the last start time
    def print_csv_file(object):
        for title,artist,time_play in object:
            print title,artist,time_play
    
    with open(file_path,'rb') as f:
        t_reader = csv.reader(f)
        lastline = t_reader.next()
        for line in t_reader:
            lastline = line
    
    last_time = lastline[2]
    
    
    #Write new artist data if change in time
    with open(file_path,'ab') as wf:
        wr = csv.writer(wf)
        if not 'no_music' in json_data['now']['status']:
            track_title = json_data['now']['track_title'].encode('ascii','ignore')
            track_artist = json_data['now']['display_artist'].encode('ascii','ignore')
            start_time = json_data['now']['start_time'].encode('ascii','ignore')
            if start_time != last_time:
                wr.writerow((track_title, track_artist,start_time))
                print station, start_time


while True:
    station_list = ['P3','P5D','P6B','P7M','P8J','RAM','DRM']
    for station in station_list:
        mining_station(station)
    time.sleep(30)

