# spotify-playlist-maker

REST web app made with python and flask that allows user to create a Spotify playlist of the top 20 trending songs on Last.fm via the Spotify and Last.fm APIs. 

Issues to fix: 
- although 20 songs are retreived from last.fm charts, only first 18/19 songs actually get added to spotify playlist??

Todo: 
- add functionality to also be able to make playlist from top songs on billboard/rolling stone/NZtop40 etc
- allow for login via spotify so dont have to keep regenerating Spotify API token every hour when it expires. 

To run:
- generate playlist-modify-public spotify token from https://developer.spotify.com/console/post-playlists/
- return generated token in spotify_token() in api_keys_tokens.py
- run on command line:

    > set FLASK_APP=app
    
    > flask run
