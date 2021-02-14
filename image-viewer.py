#!/usr/bin/env python
import json
import spotipy
import spotipy.util as util
from keys import spotify_secret
from PIL import Image, ImageFont, ImageDraw
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
import requests
import time

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.brightness = 55
# options.chain_length = 1
# options.pwm_lsb_nanoseconds = 270
# options.hardware_mapping = "regular"

matrix = RGBMatrix(options=options)

token = util.prompt_for_user_token("mattnovelli", "user-read-currently-playing", client_id='b5285806382b4bad8895640467fbf693', client_secret=spotify_secret, redirect_uri="https://mnovelli.com/projects/CUM_MATRIX.html")
sp = spotipy.Spotify(auth=token)

def refreshUrl():
    current_track = sp.currently_playing()
    print('making a request..')
    if current_track is None:
        print('nothing playing lmao')
    else:
        updateBoard(current_track['item']['album']['images'][1]['url'])
        time.sleep(5)
        refreshUrl()

def updateBoard(url):
    art = Image.open(requests.get(url, stream=True).raw)
    art = art.resize((32,32))
    canvas = Image.new("RGB", (64, 32), color=(0, 0, 0))
    canvas.paste(art)
    canvas.paste(art, (32,0))
    # draw = ImageDraw.Draw(canvas)
    matrix.SetImage(canvas.convert("RGB"))

refreshUrl()
    
