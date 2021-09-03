from urllib.parse import unquote
from . import BCOV_POLICY, ACCOUNT_ID
import requests
from youtube_dl import YoutubeDL
from flask import render_template
from flask import request

bc_url = f"https://edge.api.brightcove.com/playback/v1/accounts/{ACCOUNT_ID}/videos"
jw_url = "https://cdn.jwplayer.com/v2/media"

bc_hdr = {"BCOV-POLICY": BCOV_POLICY}


def play_brightcove(video_id):
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


def play_jw(video_id):
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


def play_youtube(video_id):
    url = f"https://youtu.be/{video_id}"
    with YoutubeDL() as ydl:
      info_dict = ydl.extract_info(url, download=False)

    video_name = info_dict['title']

    videos = [ {"format": format["height"], "url": format["url"]} for format in info_dict["formats"] if format["format_id"] in ["18", "22"] ]
    captions = info_dict["automatic_captions"] if "automatic_captions" in info_dict else []
    video_captions = { caption: captions[caption][-1]["url"] for caption in captions if caption in ['en', 'hi'] }
    caption = len(video_captions) != 0

    return render_template(
        "youtube.html",
        video_name=video_name,
        videos=videos,
        caption=caption,
        video_captions=video_captions
    )


def play_audio():
    url = request.query_string.decode("utf-8").removeprefix("url=")
    ext = url.split('.')[-1]
    title = "Audio"
    url_type = f"audio/{ext}"

    return render_template(
        "direct_template.html",
        title=title,
        url=url,
        type=url_type,
    )


def play_video():
    url = request.query_string.decode("utf-8").removeprefix("url=")
    ext = url.split('.')[-1]
    title = "Video"
    url_type = f"video/mp4"

    return render_template(
        "direct_template.html",
        title=title,
        url=url,
        type=url_type,
    )

