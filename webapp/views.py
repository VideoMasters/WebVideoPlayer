from functools import wraps
from . import app
from . import KEY, DIRECT
from . import vigenere
from .players import (
        play_brightcove,
        play_jw,
        play_youtube,
        play_audio,
        play_video,
        play_dash,
        play_hls
)
from flask import Flask
from flask import request
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
    url = request.args.get("url")
    title = request.args.get("title", "Audio")
    return play_audio(url, title)


@app.route("/video")
def video():
    url = request.args.get("url")
    track_url = request.args.get("track", "")
    title = request.args.get("title", "Video")
    return play_video(url, title, track_url)


@app.route("/mpd")
def mpd():
    url = request.args.get("url")
    title = request.args.get("title", "DASH")
    track_url = request.args.get("track", "")
    widevine_url = request.args.get("wv_url", "")
    microsoft_url = request.args.get("ms_url", "")
    return play_dash(url, title, track_url, widevine_url, microsoft_url)


@app.route("/m3u8")
def m3u8():
    url = request.args.get("url")
    title = request.args.get("title", "HLS")
    track_url = request.args.get("track", "")
    return play_hls(url, title, track_url)


