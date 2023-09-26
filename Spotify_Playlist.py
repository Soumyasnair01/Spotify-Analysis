import pandas as pd
import spotipy
import spotipy.util as util
import json
from hdbcli import dbapi
from datetime import datetime
from spotipy.oauth2 import SpotifyClientCredentials

client_id = "******************"  #Your Spotify Client ID -Refer Blog2  of this series
client_secret = "******************" #Your Spotify Secret Key -Refer Blog2 of this series
redirect_uri = "http://localhost:8888/callback"
username = "Abi"  #Your Spotify Username
scope = "user-library-modify"

# Get the access token
token = spotipy.util.prompt_for_user_token(
        username="*******", 
        scope=scope,
        client_id="******************",
        client_secret="******************",
        redirect_uri=redirect_uri,
    )

client_manager = SpotifyClientCredentials('******************','******************')
sp = spotipy.Spotify(auth=token, client_credentials_manager=client_manager)

#Process all tracks and items of a specific playlist
def get_top2022_playllst(playlistid, country):
    playlist2022 = playlistid
    collname   = country
    toptracks1 = sp.user_playlist(username, playlist2022)
    tracks1 = toptracks1["tracks"]
    toptracks = tracks1["items"]
    t2  = json.dumps(toptracks)    #here we store the json information as a text file in t2
    finaljson = insert_json_hcdb(t2,collname) #call the insert function
    print(collname + " tracks has been succesfully inserted")   


#Collect all the playlist data and insert it into HANA Cloud tenant of Datasphere as NCLOB
def insert_json_hcdb(t3, country1):
    conn = dbapi.connect (address= '******************',
                      port= '***',
                      user= '******************',  # Provide your OpenSQL container Username here
                      password= "******************",  # Provide your OpenSQL contianer password here
                      encrypt=True           
                     ) #establish open SQL schema access 
    get = datetime.now()
    cntdaily = country1 + str(get.day)+ str(get.month)+str(get.year)   #add datetime to filename country
    sql = 'INSERT INTO SA4 (COUNTRY, TOPTRACKS) VALUES (?,?)'
    cursor = conn.cursor()
    cursor.execute(sql,(cntdaily,t3))
    cursor.close()
    conn.close()       
    return country1



# Get all top playlist from different countries
playlist2022 = get_top2022_playllst('37i9dQZEVXbLp5XoPON0wI','USA')
playlist2022 = get_top2022_playllst('37i9dQZEVXbK4fwx2r07XW','AUS')
playlist2022 = get_top2022_playllst('37i9dQZEVXbLJ0paT1JkgZ','CHILI')
playlist2022 = get_top2022_playllst('37i9dQZEVXbKPTKrnFPD0G','ARG')
playlist2022 = get_top2022_playllst('37i9dQZEVXbM1EaZ0igDlz','AUSTR')
playlist2022 = get_top2022_playllst('37i9dQZEVXbMw2iUtFR5Eq','DEN')
playlist2022 = get_top2022_playllst('37i9dQZEVXbK8BKKMArIyl','GER')
playlist2022 = get_top2022_playllst('37i9dQZEVXbMWDif5SCBJq','IND')
playlist2022 = get_top2022_playllst('37i9dQZEVXbIWlLQoMVEFp','NZ')
playlist2022 = get_top2022_playllst('37i9dQZEVXbJZGli0rRP3r','KOR')

