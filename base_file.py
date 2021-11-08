import json
import requests
import api_keys_tokens
import sys


class LastFmSpotify:
    def __init__(self):
        self.token = api_keys_tokens.spotify_token()
        self.api_key = api_keys_tokens.last_fm_api_key()
        self.user_id = api_keys_tokens.spotify_user_id()

        self.spotify_headers = {"Content-Type": "application/json",
                                "Authorization": f"Bearer {self.token}"}
        self.playlist_id = ''
        self.song_info = {}
        self.uris = []

    def strip_punctuation(self, input_str):
        punctuation = '''{};:'"\,<>/@#$%^&*_~'''
        for element in input_str:
            if element in punctuation:
                input_str = input_str.replace(element, "")
        return input_str

    def fetch_songs_from_lastfm(self):
        params = {'limit': 20, 'api_key': self.api_key}
        url = f'http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&format=json'
        response = requests.get(url, params=params)
        if response.status_code != 200:
            self.exceptions(response.status_code, response.text)
        res = response.json()
        song_info = dict()
        for item in res['tracks']['track']:
            song = item['name']
            song = self.strip_punctuation(song)
            artist = item['artist']['name'].title()
            song_info[song] = artist
        return song_info

    def get_uri_from_spotify(self, song_info):
        uri_list = []
        for song_name, artist in song_info.items():
            url = f"https://api.spotify.com/v1/search?query=track%3A{song_name}+artist%3A{artist}&type=track&offset=0&limit=10"
            response = requests.get(url, headers=self.spotify_headers)
            res = response.json()
            output_uri = res['tracks']['items']
            if not output_uri:
                # end of list, break so we don't get error trying to index out of range
                break
            uri = output_uri[0]['uri']  # 0th element to make sure to get first song (avoid remixes etc)
            uri_list.append(uri)
        return uri_list

    def create_spotify_playlist(self, name, description):
        data = {
            "name": name,
            "description": description,
            "public": True
        }
        data = json.dumps(data)
        url = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        response = requests.post(url, data=data, headers=self.spotify_headers)

        if response.status_code == 201:
            res = response.json()
            return res['id']
        else:
            self.exceptions(response.status_code, response.text)

    def add_songs_to_playlist(self, playlist_id, uris):
        uri_list = json.dumps(uris)
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        response = requests.post(url, data=uri_list, headers=self.spotify_headers)
        if response.status_code == 201:
            return "Songs added successfully yuh"
        else:
            self.exceptions(response.status_code, response.text)

    def list_songs_in_playlist(self, playlist_id):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        response = requests.get(url, headers=self.spotify_headers)
        if response.status_code != 200:
            self.exceptions(response.status_code, response.text)
        else:
            res = response.json()
            songs = []
            for item in res['items']:
                songs.append(item['track']['name'])
            return songs

    def exceptions(self, status_code, err):
        print("Exception has occurred with status_code", status_code)
        print("Error: ", err)
        sys.exit(0)

