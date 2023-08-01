from flask import Flask, request, url_for, session, redirect, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import time


custom_dotenv_path = "D:/Users/Biki/OneDrive/My Documents/var.env"

load_dotenv(custom_dotenv_path)


app = Flask(__name__, static_folder='static')

app.secret_key = 'SOMETHING-RANDOM'
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'
TOKEN_INFO = "token_info"




@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    return redirect(auth_url)


@app.route('/authorize')
def authorize():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect("/getTracks")

@app.route('/getTracks')
def getTracks():
    token_info = get_token()
    sp = spotipy.Spotify(auth=token_info['access_token'])
    tracks1 = sp.current_user_top_tracks(limit=50)['items']
    tracks2 = sp.current_user_top_tracks(limit=50, offset=50)['items']
    tracks=tracks1+tracks2
    return render_template('tracks.html', tracks=tracks)

def get_token():
    token_valid = False
    token_info = session.get("token_info", {})


    # Checking if the session already has a token stored
    if not (session.get('token_info', False)):
        token_valid = False
        return {}

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if (is_token_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET'),
        redirect_uri=url_for('authorize', _external=True),
        scope="user-library-read user-top-read"

    )

