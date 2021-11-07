from flask import Flask, render_template, request, session, redirect
import json, base_file

app = Flask(__name__)

app.secret_key = 'This is a very secure app'    # make something that is difficult to crack


obj = base_file.LastFmSpotify()  # object variable, change later
topsongs = obj.fetch_songs_from_lastfm()


@app.route('/')
def hello_world():
    return redirect('/create')

@app.route('/top', methods=['GET', 'POST'])
def top_songs():
    if request.method == 'GET':
        return render_template("index.html", topsongs=topsongs, template='top')
    else:
        if 'playlist_id' in session.keys():
            uri = obj.get_uri_from_spotify(topsongs)
            playlist_id = session['playlist_id']
            ans = obj.add_songs_to_playlist(playlist_id, uri)
            return redirect('/view')
        else:
            return redirect('/create')

@app.route('/create', methods=['GET', 'POST'])
def create_playlist():
    if request.method == 'GET':
        return render_template("index.html", template='create')
    else: # request.method == 'POST':
        name = request.form['playlist_name'].strip()
        description = request.form['playlist_description'].strip()
        session['playlist_id'] = obj.create_spotify_playlist(name, description)
        return redirect('/top')

@app.route('/view')
def view_songs():
    if 'playlist_id' in session.keys():
        songs = obj.list_songs_in_playlist(session['playlist_id'])
        return render_template("index.html", songs=songs, template='view')
    return redirect('/create')


if __name__ == '__main__':
    app.run(debug=True)
