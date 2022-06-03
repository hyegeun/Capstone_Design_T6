import argparse
import os
from typing import List
from flask import render_template

from flask import (
    Flask,
    abort,
    jsonify,
    Response,
    send_file,
)


app = Flask(__name__, static_folder="./", static_url_path="")


DATA = "data"
IMAGES = "images"

datapath = None

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/index")
def index() -> Response:
    return send_file(os.path.join(app.static_folder, "index.html"))

@app.route("/upload")
def upload():
    #기존 result file들은 다 지워줌 
    if os.path.isdir('data/result'):
        cmd1 = ("rm -r data/result")
        os.system(cmd1)
    if os.path.isfile('data/result.zip'):
        cmd2 = ("rm -r data/result.zip")
        os.system(cmd2)
        
    os.makedirs('data/result')
    
    return render_template("upload.html")
    
@app.route("/pcs_sfm", methods=['GET', 'POST'])
def pcs_sfm():
    return render_template("pcs_sfm.html")
    
@app.route("/finish_sfm", methods=['GET', 'POST'])
def finish_sfm():

    cmd = ["cp data/config.yaml data/result", "bin/opensfm extract_metadata data/result", \
    "bin/opensfm detect_features data/result", \
    "bin/opensfm match_features data/result", \
    "bin/opensfm create_tracks data/result", \
    "python3 color_point.py data/result 1.0", \
    "bin/opensfm reconstruct data/result", \
    "bin/opensfm mesh data/result", \
    "mv data/result/images data/result/original_images", \
    "mv data/images data/result/images", \
    "zip data/result.zip -r data/result"]
           
    for command in cmd:
        os.system(command)
    
    return render_template("finish_sfm.html")    

@app.route("/items")
def get_recs() -> Response:
    if datapath is None:
        return jsonify({"items": []})

    reconstructions = [
        {
            "children": [],
            "name": rec,
            "type": "RECONSTRUCTION",
            "url": [os.path.join(DATA, rec)],
        }
        for rec in reconstruction_files(datapath)
    ]

    return jsonify({"items": reconstructions})


@app.route("/data/<path:subpath>")
def get_data(subpath) -> Response:
    path = os.path.join(datapath, subpath)
    return verified_send(path)


@app.route("/image/<shot_id>")
def get_image(shot_id) -> Response:
    path = os.path.join(datapath, IMAGES, shot_id)
    return verified_send(path)


def json_files(path) -> List[str]:
    """List all json files under a dir recursively."""
    paths = []
    for root, _, files in os.walk(datapath):
        for file in files:
            if ".json" in file:
                absolute = os.path.join(root, file)
                relative = os.path.relpath(absolute, path)
                paths.append(relative)
    return paths


def probably_reconstruction(file) -> bool:
    """Decide if a path may be a reconstruction file."""
    return file.endswith("json") and "reconstruction" in file


def reconstruction_files(path) -> List[str]:
    """List all files that look like a reconstruction."""
    files = json_files(path)
    return sorted(filter(probably_reconstruction, files))


def verified_send(file) -> Response:
    if os.path.isfile(file):
        return send_file(file)
    else:
        # pyre-fixme[7]: Expected `Response` but got implicit return value of `None`.
        abort(404)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-d", "--dataset", help="dataset to visualize")
    parser.add_argument(
        "-p", "--port", type=int, default=8080, help="port to bind server to"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    global datapath
    if args.dataset is not None:
        datapath = os.path.abspath(args.dataset)
    return app.run(host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    exit(main())
