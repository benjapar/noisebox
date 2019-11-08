from playsound import playsound
from flask import Flask
from flask import request
import os
import threading

sem = threading.Semaphore()

app = Flask(__name__)

SOUND_FOLDER= os.getcwd() + '/sounds/'
app.config['UPLOAD_FOLDER'] = SOUND_FOLDER
#sudo kill -9 $(sudo lsof -t -i:5000)

@app.route('/')
def list():
    links = '<h3>Here is the sound list: </h3><ul>'
    for r, d, file_list in os.walk(SOUND_FOLDER):
        for _file in file_list:
            links += '<li><a href="'+request.base_url+'play?sound=' + _file + '">'+ _file.replace('.mp3','') +'</a> </li>'
    links += '</li>'
    return links

@app.route('/play', methods=['GET'])
def play():
    sem.acquire()
    sound = request.args.get('sound', type = str)
    if sound:
        playsound(SOUND_FOLDER+ sound)
    sem.release()
    return 'Sound played !'

if __name__ == '__main__':
    app.run(port=5000)
