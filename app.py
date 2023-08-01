from flask import Flask, request, url_for, sessions, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

custom_dotenv_path = r'Spotify-Analytics\evs.gitignore\var.env'

load_dotenv(custom_dotenv_path)

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

print(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)

app = Flask(__name__)

app.secret_key = "safkhsdhfkbjdhfsjfsdf"
app.config['SESSION_COOKIE_NAME'] = 'Cookie'




@app.route('/')
def index():
    return "Home Page"

@app.route('/redirect')
def redirectPage():
    return 'redirect'

@app.route('/getTracks')
def getTracks():
    return "Songs lol"

