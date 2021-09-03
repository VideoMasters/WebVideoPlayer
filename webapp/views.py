from functools import wraps
from . import app
from . import KEY, DIRECT
from . import vigenere
from .players import (
        play_brightcove,
        play_jw,
        play_youtube,
        play_audio,
        play_video
)
from flask import Flask
from werkzeug.utils import redirect


def check_direct(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if DIRECT:
            return func(*args, **kwargs)
        else:
            return "<font color=red size=20>Only Encrypted Video Ids Allowed</font>"

    return wrapper


@app.route("/arc-sw.js")
def arc():
    return app.send_static_file('arc-sw.js')


@app.route("/brightcove/<int(fixed_digits=13):video_id>")
@check_direct
def _brightcove(video_id):
    return play_brightcove(video_id)


@app.route("/jw/<string(length=8):video_id>")
@check_direct
def _jw(video_id):
    return play_jw(video_id)


@app.route("/youtube/<string(length=11):video_id>")
@check_direct
def _youtube(video_id):
    return play_youtube(video_id)


@app.route("/brightcove/<video_id>")
def brightcove(video_id):
    video_id = vigenere.decode(KEY, video_id)
    return play_brightcove(video_id)


@app.route("/jw/<video_id>")
def jw(video_id):
    video_id = vigenere.decode(KEY, video_id)
    return play_jw(video_id)


@app.route("/youtube/<video_id>")
def youtube(video_id):
    video_id = vigenere.decode(KEY, video_id)
    return play_youtube(video_id)


@app.route("/audio")
def audio():
    return play_audio()


@app.route("/video")
def video():
    return play_video()


