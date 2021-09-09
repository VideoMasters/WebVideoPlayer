from urllib.parse import unquote
from . import BCOV_POLICY, ACCOUNT_ID
import requests
from youtube_dl import YoutubeDL
from flask import render_template

BC_URL = "https://edge.api.brightcove.com/playback/v1/accounts/{}/videos/{}"
JW_URL = "https://cdn.jwplayer.com/v2/media/{}"


def play_dash(url, title, track_url, widevine_url, microsoft_url):
    return render_template(
        "dash.html",
        title=title,
        url=url,
        track_url=track_url,
        widevine_url=widevine_url,
        microsoft_url=microsoft_url,
    )


def play_hls(url, title, track_url):
    return render_template(
        "hls.html",
        title=title,
        url=url,
        track_url=track_url,
    )


def play_brightcove(video_id, account_id=ACCOUNT_ID, bcov_policy=BCOV_POLICY):
    bc_url = BC_URL.format(account_id, video_id)
    bc_hdr = {"BCOV-POLICY": bcov_policy}
    video_response = requests.get(bc_url, headers=bc_hdr)

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
    return play_dash(video_url, video_name, track_url, widevine_url, microsoft_url)


def play_jw(video_id):
    jw_url = JW_URL.format(video_id)
    video_response = requests.get(jw_url)

    if video_response.status_code != 200:
        return "<font color=red size=20>Wrong Video ID</font>"

    video = video_response.json()

    video_name = video["title"]

    video_url = video["playlist"][0]["sources"][0]["file"]
    track_url = video["playlist"][0]["tracks"][0]["file"]
    return play_hls(video_url, video_name, track_url)


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


def play_audio(url, title):
    ext = url.split('.')[-1]
    url_type = f"audio/{ext}"

    return render_template(
        "audio_video.html",
        title=title,
        url=url,
        type=url_type,
    )


def play_video(url, title, track_url):
    ext = url.split('.')[-1]
    url_type = f"video/mp4"

    return render_template(
        "audio_video.html",
        title=title,
        url=url,
        type=url_type,
        track_url=track_url,
    )

