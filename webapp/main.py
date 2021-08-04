import os
import tempfile
from urllib.parse import unquote
import requests
from flask import Flask
from flask import request
from flask import render_template
from dotenv import load_dotenv
from werkzeug.utils import redirect
from youtube_dl import YoutubeDL


load_dotenv()

ACCOUNT_ID = os.environ.get("ACCOUNT_ID")
BCOV_POLICY = os.environ.get("BCOV_POLICY")

bc_url = f"https://edge.api.brightcove.com/playback/v1/accounts/{ACCOUNT_ID}/videos"

bc_hdr = {"BCOV-POLICY": BCOV_POLICY}

jw_url = "https://cdn.jwplayer.com/v2/media"

app = Flask(__name__)


@app.route("/<int(fixed_digits=13):video_id>")
def brightcove(video_id):
    video_response = requests.get(f"{bc_url}/{video_id}", headers=bc_hdr)

    if video_response.status_code != 200:
        return "<font color=red size=20>Wrong Video ID</font>"

    video = video_response.json()

    video_name = video["name"]

    video_source = video["sources"][3]
    video_url = video_source["src"]
    widevine_url = ""
    microsoft_url = ""
    if "key_systems" in video_source:
        widevine_url = video_source["key_systems"]["com.widevine.alpha"]["license_url"]
        microsoft_url = video_source["key_systems"]["com.microsoft.playready"][
            "license_url"
        ]
    track_url = video["text_tracks"][1]["src"]
    return render_template(
        "template.html",
        type="dash",
        video_name=video_name,
        video_url=video_url,
        track_url=track_url,
        widevine_url=widevine_url,
        microsoft_url=microsoft_url,
    )


@app.route("/<string(length=8):video_id>")
def jw(video_id):
    video_response = requests.get(f"{jw_url}/{video_id}")

    if video_response.status_code != 200:
        return "<font color=red size=20>Wrong Video ID</font>"

    video = video_response.json()

    video_name = video["title"]

    video_url = video["playlist"][0]["sources"][0]["file"]
    track_url = video["playlist"][0]["tracks"][0]["file"]
    return render_template(
        "template.html",
        type="hls",
        video_name=video_name,
        video_url=video_url,
        track_url=track_url,
    )


@app.route("/<string(length=11):video_id>")
def youtube(video_id):
    url = f"https://youtu.be/{video_id}"
    with YoutubeDL() as ydl:
      info_dict = ydl.extract_info(url, download=False)

    video_name = info_dict['title']

    videos = [ {"format": format["height"], "url": format["url"]} for format in info_dict["formats"] if format["format_id"] in ["18", "22"] ]
    captions = info_dict["automatic_captions"] if "automatic_captions" in info_dict else []
    video_captions = { caption: captions[caption][-1]["url"] for caption in captions if caption in ['en', 'hi'] }
    caption = len(video_captions) != 0

    return render_template(
        "yt_template.html",
        video_name=video_name,
        videos=videos,
        caption=caption,
        video_captions=video_captions
    )


@app.route("/play")
def play():
    url = request.query_string.decode("utf-8").removeprefix("url=")
    content_type = requests.head(url).headers["content-type"]
    print(content_type)
    con_type = content_type.split("/")[0]
    if con_type == "audio":
        title = "Audio"
        url_type = content_type
    elif con_type == "Video":
        title = "Video"
        url_type = content_type
    elif url.endswith(".mp3") or url.endswith(".m4a"):
        ext = url.split('.')[-1]
        title = "Audio"
        url_type = f"audio/{ext}"
    elif url.endswith(".mp4") or url.endswith(".mkv"):
        ext = url.split('.')[-1]
        title = "Video"
        url_type = f"video/{ext}"
    else:
        return "Unsupported format"

    return render_template(
        "direct_template.html",
        title=title,
        url=url,
        type=url_type,
    )


@app.route("/arc-sw.js")
def arc():
    return redirect("https://arc.io/arc-sw.js")
