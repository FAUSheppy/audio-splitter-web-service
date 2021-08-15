#!/usr/bin/python3
import os
import flask
import argparse
import sys
import PIL.Image
import werkzeug.utils

app = flask.Flask("Picture factory app", static_folder=None)
cache = "cache/"

@app.route("/upload", methods = ['GET', 'POST'])
def upload():
    if flask.request.method == 'POST':
        os.system("rm -r cache/")
        os.system("mkdir cache/")

        f = flask.request.files['file']
        fname = werkzeug.utils.secure_filename(f.filename)
        sfName = os.path.join(cache, fname)
        if not sfName.endswith(".ogg"):
            f.save(sfName + "_tmp")
            os.system("ffmpeg -i '{}' '{}.ogg'".format(sfName + "_tmp", sfName))
            sfName += ".ogg"
        else:
            f.save(sfName)

        os.system("./audio_splitter.py --silence-padding 500 --silence-vol -50 --target-dir chunks {}".format(sfName))
        os.system("rm static/segments.zip")
        os.system("zip -r static/segments.zip cache")
        return flask.redirect("/segments.zip")

    
    return flask.render_template("upload.html")

@app.route("/segments.zip")
def segments():
    return flask.send_from_directory("static", "segments.zip")

@app.before_first_request
def init():
    app.config['MAX_CONTENT_PATH'] = 32+1000*1000
    app.config['UPLOAD_FOLDER']    = cache
    app.config['UPLOAD_ENABLED']   = os.path.isfile("./upload.enable")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Audio-Splitter',
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # general parameters #
    parser.add_argument("-i", "--interface", default="127.0.0.1", help="Interface to listen on")
    parser.add_argument("-p", "--port",      default="5000",      help="Port to listen on")

    # startup #
    args = parser.parse_args()
    app.run(host=args.interface, port=args.port)
