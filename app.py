from flask import Flask, render_template, request
import json

app = Flask(__name__, static_folder='./static', template_folder='./static')
json_string = ''

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    json_string = file.read().decode("utf-8")
    elements = [
        { 'data': { 'id': 'one', 'label': 'Node 1' }, 'position': { 'x': 0, 'y': 0 } },
        { 'data': { 'id': 'two', 'label': 'Node 2' }, 'position': { 'x': 100, 'y': 0 } },
        { 'data': { 'source': 'one', 'target': 'two', 'label': 'Edge from Node1 to Node2' } }
    ];
    return json.dumps(elements)