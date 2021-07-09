from flask import Flask

app = Flask(__name__)


@app.route("/<int(fixed_digits=13):video_id>")
def index(video_id):
    return str(video_id)
