import sys
import io
from PIL import Image
import cv2
import base64
import torch
from flask import Flask, Response,  jsonify, render_template, request, make_response
from werkzeug.exceptions import BadRequest
import os
import json
from flask_socketio import SocketIO
import numpy as np
import time
from flask_cors import CORS
# creating flask app

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, async_mode='threading', cors_allowed_origins='*', cors_credentials=True)

# create a python dictionary for your models d = {<key>: <value>, <key>: <value>, ..., <key>: <value>}
dictOfModels = {}
# create a list of keys to use them in the select part of the html code
listOfKeys = []

modelname = []

global cap

cors = CORS(app, resources={r"/*": {"origins": "*"}})

# inference fonction
def get_prediction(img_bytes,model):
    img = Image.open(io.BytesIO(img_bytes))
    results = model(img, size=480)  
    return results


# get method
@app.route('/', methods=['GET'])
def get():
    return render_template("index.html")

@app.route('/model', methods=['GET'])
def getModel():
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    return (listOfKeys, 200, headers)

# def gen_frames():
#     global cap
#     cap = cv2.VideoCapture(0)
#     while cap.isOpened():
#         success, frame = cap.read()
#         if not success:
#             break
#         results = dictOfModels[listOfKeys[0]](frame, size = 640)
#         results.render()
#         for img in results.ims:
#             # RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#             im_arr = cv2.imencode('.jpg', img)[1]
#         frame = im_arr.tobytes()
#         yield (b'--frame\r\n'
#                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/video_feed')
# def video_feed():
#     respon = Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
#     respon.headers.add('Access-Control-Allow-Origin', '*')
#     return respon

# @app.route('/stop_video')
# def stop_video():
#     global cap
#     if(cap != None):
#         cap.release()
#         cap = cv2.VideoCapture(0)
#         cv2.destroyAllWindows()
#         cap = cv2.VideoCapture(0)
#     return 'Video stopped'

@app.route('/predict', methods=['POST'])
def predictnohtml():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    file = request.files['file']
    img_bytes = file.read()
    model_get = dictOfModels[listOfKeys[0]]
    results = get_prediction(img_bytes,model_get)
    labels = results.xyxy[0][:, -1].tolist()
    boxes = results.xyxy[0][:, :-1].tolist()
    conf_scores = results.pred[0][:, -2].tolist()
   
    output_str = ''
    results_json = []
    for i in range(len(labels)):
        out_name = results.names[int(labels[i])].capitalize()
        out_conf = conf_scores[i]
        output_str += f'{out_name}: conf: {round(out_conf,3)}, at {round(boxes[i][0])}, {round(boxes[i][1])}, {round(boxes[i][2])}, {round(boxes[i][3])}\n'
        results_json.append({
            "class": out_name,
            "confidence": float(out_conf),
            "topleft_x": boxes[i][0],
            "topleft_y": boxes[i][1],
            "bottomright_x": boxes[i][2],
            "bottomright_y": boxes[i][3]
        })
    output_str_break = output_str.replace("\n", "<br>")
    json_out  = json.dumps(results_json, indent=2)

    results.render()
   
    for img in results.ims:
        RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im_arr = cv2.imencode('.jpg', RGB_img)[1]

        encoded_image_base64 = base64.b64encode(im_arr.tobytes()).decode('utf-8')
    
    response = jsonify({
        'results': json_out,
        'result_img': encoded_image_base64,
        'result_str': output_str_break
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
 
# post method
@app.route('/', methods=['POST'])
def predict():
    file = extract_img(request)
    img_bytes = file.read()
    
    # choice of the model
    model_get = dictOfModels[request.form.get("model_choice")]
    results = get_prediction(img_bytes,model_get)
    print(f'User selected model : {request.form.get("model_choice")}')

    labels = results.xyxy[0][:, -1].tolist()
    boxes = results.xyxy[0][:, :-1].tolist()
    conf_scores = results.pred[0][:, -2].tolist()
    # create string with class and coordinates
    output_str = ''
    results_json = []
    for i in range(len(labels)):
        out_name = results.names[int(labels[i])].capitalize()
        out_conf = conf_scores[i]
        output_str += f'{out_name}: conf: {round(out_conf,3)}, at {round(boxes[i][0])}, {round(boxes[i][1])}, {round(boxes[i][2])}, {round(boxes[i][3])}\n'
        results_json.append({
            "class": out_name,
            "confidence": float(out_conf),
            "topleft": boxes[i][0],
            "bottomright": boxes[i][3]
        })

    output_str_break = output_str.replace("\n", "<br>")
    json_out  = json.dumps(results_json, indent=4)

    # updates results.imgs with boxes and labels
    results.render()
    
    # encoding the resulting image and return it
    for img in results.ims:
        RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im_arr = cv2.imencode('.jpg', RGB_img)[1]
        # response = make_response(im_arr.tobytes())
        encoded_image_base64 = base64.b64encode(im_arr.tobytes()).decode('utf-8')
        # response.headers['Content-Type'] = 'image/jpeg'
    return render_template("index.html", len = len(listOfKeys), listOfKeys = listOfKeys, responsed = encoded_image_base64, output_str=output_str_break, json_out=json_out)
    # return response

@socketio.on('frame')
def process_frame(frame):
    # Convert base64 string to numpy array
    imgdata = base64.b64decode(frame.split(',')[1])
    img_real = Image.open(io.BytesIO(imgdata))
    results = dictOfModels[listOfKeys[0]](img_real, size = 640)
    results.render()
    for img in results.ims:
        RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im_arr = cv2.imencode('.jpg', RGB_img)[1]
    data = base64.b64encode(im_arr).decode('utf-8')
    # Send processed frame back to frontend
    socketio.emit('processed_frame', f"data:image/jpeg;base64,{data}")

def extract_img(request):
    # checking if image uploaded is valid
    if 'file' not in request.files:
        raise BadRequest("Missing file parameter!")
        
    file = request.files['file']
    
    if file.filename == '':
        raise BadRequest("Given file is invalid")
        
    return file
    

if __name__ == '__main__':
    print('Starting yolov5 webservice...')
    # Getting directory containing models from command args (or default 'models_train')
    models_directory = 'models_train'
    if len(sys.argv) > 1:
        models_directory = sys.argv[1]
    print(f'Watching for yolov5 models under {models_directory}...')
    for r, d, f in os.walk(models_directory):
        for file in f:
            if ".pt" in file:
                # example: file = "model1.pt"
                # the path of each model: os.path.join(r, file)
                model_name = os.path.splitext(file)[0]
                model_path = os.path.join(r, file)
                print(f'Loading model {model_path} with path {model_path}...')
                dictOfModels[model_name] = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)
                # you would obtain: dictOfModels = {"model1" : model1 , etc}
        for key in dictOfModels :
            listOfKeys.append(key) # put all the keys in the listOfKeys

    #print(f'Server now running on {os.environ["JOB_URL_SCHEME"]}{os.environ["JOB_ID"]}.{os.environ["JOB_HOST"]}')
    print('Server is now running')
    
    # starting app
    socketio.run(app, debug=True, host='0.0.0.0', allow_unsafe_werkzeug=True)
    #app.run(debug=True,host='0.0.0.0')