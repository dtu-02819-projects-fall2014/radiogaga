r"""
Lyricanalysis - Radiogaga.

This file belongs to Joachim Blom Hansen, Rasmus Jessen Aaskov and Soren
Trads Steen.
"""
import sys
import datamining as dm
import mysqlinterface as my
from key import unique_key
from gettempo import getbpm
from lyricanalysis import get_score
import time as tt

# This might be a very bad idea but we still have some encoding issues
reload(sys)
sys.setdefaultencoding('iso8859-1')

# Handle cammand arguments
station_list = ['P3', 'P6B', 'P7M', 'RAM']
station = 'P3'

# Handle cammand arguments
call = list(sys.argv)
try:
    if call[1] in station_list:
        station = call[1]
    else:
        sys.exit('Error in command. No such station was found')
except:
    station = 'P3'
    print('Error in command. You have to specify the name of the station')


# Get track info from DR
url = "http://www.dr.dk/playlister/feeds/nowNext/nowPrev.drxml?items=1&cid={0}"
url = url.format(station)

while True:
    # Read the recieved data
    try:
        # If fails, then wait until json becomes available again
        no_json = 0
        track_i = dm.JsonResponse(url, ['now', 'track_title'])
        artist_i = dm.JsonResponse(url, ['now', 'display_artist'])
        lastplay_i = dm.JsonResponse(url, ['now', 'start_time'])
    except:
        no_json = 1

    # If any one of the info is missing, wait
    # Note there is a PEP E129 I can't get rid off
    if (track_i.answer != "" or
        artist_i.answer != "" or
        lastplay_i.answer != "" or
        no_json == 1):
        # Check if already exist in db
        # Start a new connection
        conn = my.MySQLConnection('ip', 'bobafett', 'bobafett', 'gaga')

        # Remove any char that might return an encoding error
        bad_char = ["§", "½", "!", "@", '"', "#", "£", "$", "¤", "%", "&",
                    "/", "{", "(", "[", "]", ")", "}", "=", "?", "+", "´",
                    "|", "`", "^", "'", "*", ",", ";", ".", ":", "-", "_"]
        e_track = ""
        for ch in track_i.answer:
            if ch not in bad_char:
                e_track = e_track + ch

        e_artist = ""
        for ch in artist_i.answer:
            if ch not in bad_char:
                e_artist = e_artist + ch

        e_track = e_track.replace('  ', ' ')
        e_artist = e_artist.replace('  ', ' ')

        # Display
        print(e_track, e_artist)

        # Set up an element
        element = {'track': e_track,
                   'artist': e_artist,
                   'lastplay': lastplay_i.answer}

        # Search for the same track/artist
        container = my.radiogaga_db_get(conn,
                                        station,
                                        {'track': "%" + track_i.answer + "%",
                                         'artist': "%" + artist_i.answer + "%",
                                         'lastplay': lastplay_i.answer})

        # If container is empty, it is a new track
        s = len(container)
        if s == 0:
            # Get a new unique key
            new_key = unique_key(10)

            # Get the bpm
            bpm = getbpm(element['artist'], element['track'])

            # Get the sentiment analysis
            moodlib = 'mood_lib.csv'
            try:
                sentiment = get_score(element['artist'],
                                      element['track'], moodlib)
            except:
                sentiment = [0, 0, 0, 0]

            # Get the album cover (not implemented yet)
            # get_album_cover()

            # Combine and insert into the db
            element['track'] = track_i.answer
            element['artist'] = artist_i.answer
            element['history'] = element['lastplay']
            element['ukey'] = new_key
            element['bpm'] = bpm
            element['sad'] = sentiment[3]
            element['happy'] = sentiment[1]
            element['relaxed'] = sentiment[2]
            element['angry'] = sentiment[0]
            my.radiogaga_db_insert(conn, station, element)

            # Create a new track page (not fully implemented yet)
            # create_page()
        else:
            # The track has been played before
            last_save = container[0][3]

            if last_save != element['lastplay']:
                # Create a new history element
                history = container[0][4]
                new_element = {'history': history + ',' + element['lastplay'],
                               'lastplay': element['lastplay']}

                # Update the server with new_element
                where_element = {'track': element['track'],
                                 'artist': element['artist']}
                my.radiogaga_db_update(conn, station,
                                       new_element, where_element)

        # Close the connection to the db
        conn.end_connection()

    tt.sleep(15)
