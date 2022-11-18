
# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import os
import logging
import random
from flask import Flask, request

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)
moves = ['F', 'T', 'L', 'R']

@app.route("/", methods=['GET'])
def index():
    return "Let the battle begin!"

@app.route("/", methods=['POST'])
def move():
    request.get_data()
    #logger.info(request.json)
    dimension = request.json['arena']['dims']
    
    mystate = request.json['arena']['state']['https://cloud-run-hackathon-python-nkqzxqazya-uc.a.run.app']
    allstate = request.json['arena']['state']


    if mystate['x'] == (dimension[0] - 1) and mystate['y'] == 0 :
        for key, value in allstate.items():
            if key != 'https://cloud-run-hackathon-python-nkqzxqazya-uc.a.run.app':
                if mystate['x'] == value['x'] and mystate['y'] >= (value['y'] - 3):
                    if mystate['direction'] == 'S':
                        return 'T'
                    elif mystate['direction'] == 'E' or mystate['direction'] == 'N':
                        return 'R'
                    else:
                        return 'L'
                elif mystate['x'] <= (value['x'] + 3) and mystate['y'] == value['y']:
                    if mystate['direction'] == 'W':
                        return 'T'
                    elif mystate['direction'] == 'N' or mystate['direction'] == 'E':
                        return 'L'
                    else:
                        return 'R'
    
    if mystate['y'] > 0:
        if mystate['direction'] == 'N' :
            for key, value in allstate.items():
                if key != 'https://cloud-run-hackathon-python-nkqzxqazya-uc.a.run.app':
                    if mystate['x'] == value['x'] and mystate['y'] <= (value['y'] + 3):
                        return 'T'
            return 'F'
        elif mystate['direction'] == 'E' or mystate['direction'] == 'S':
            return 'L'
        elif mystate['direction'] == 'W' :
            return 'R'

    if  mystate['x'] < (dimension[0] - 1) :
        if mystate['direction'] == 'E' :
            for key, value in allstate.items():
                if key != 'https://cloud-run-hackathon-python-nkqzxqazya-uc.a.run.app':
                    if mystate['x'] >= (value['x'] - 3) and mystate['y'] == value['y']:
                        return 'T'
            return 'F'
        elif mystate['direction'] == 'W' or mystate['direction'] == 'N':
            return 'R'
        elif mystate['direction'] == 'S' :
            return 'L'

    return 'T'
if __name__ == "__main__":
  app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
  
