from flask import Flask, g, request, Response, make_response, session, render_template
from flask import Markup, redirect, url_for
from werkzeug.utils import secure_filename
import os

app=Flask(__name__)
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template("main.html")

@app.route('/pcs_yolo', methods=['GET', 'POST'])
def pcs_yolo():
    if request.method=='POST':
        cmd1 = ("mkdir video")
        os.system(cmd1)
        f=request.files['file']
        name = f.filename.split('.')
        inputname = 'input_video.' + name[len(name)-1]

        f.save('./video/' + secure_filename(inputname))

        return render_template('pcs_yolo.html') 

@app.route('/finish_yolo', methods=['GET', 'POST'])
def finish_yolo():

    cmd_list = ["python extract.py", \
                "rm -r video", \
                "python detect.py --source video_frame --weights crack1.pt --conf-thres 0.75 --save-txt  --name result", \
                "mv ./video_frame ../_data/OpenSfM/data/result/images", \
                "mv ./runs/detect/result/labels ../_data/OpenSfM/data/result/labels", \
                "mv ./runs/detect/result ../_data/OpenSfM/data/images"]
    
    for cmd in cmd_list:
        os.system(cmd)
    
    return render_template("finish_yolo.html")
        
if __name__ == '__main__':
    app.run(host='0.0.0.0')
