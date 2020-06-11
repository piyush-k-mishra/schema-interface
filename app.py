from flask import Flask, render_template, request
import json

app = Flask(__name__, static_folder='./static', template_folder='./static')
json_string = ''

def parse(schema):
    nodes = []
    edges = []

    nodes.append({
        'data': {
            'id': 'root',
            'label': schema['name'],
            'type': 'round-rectangle'
        }
    })

    for step in schema['steps']:
        nodes.append({
            'data': {
                'id': step['@id'], 
                'label': step['@id'].split('/')[-1].replace('_', ' '),
                'type': 'step',
                '@type': step['@type'],
                'type': 'ellipse'
            }
        })

        edges.append({
            'data': {
                'source': 'root',
                'target': step['@id']
            },
            'classes': 'root-edge'
        })
    
    for order in schema['order']:
        if 'flags' in order:
            if order['flags'] == 'precondition':
                if type(order['before']) == list:
                    for before in order['before']:
                        edges.append({
                            'data': {
                                'source': before,
                                'target': order['after']
                            }
                        })
                else:
                    edges.append({
                        'data': {
                            'source': order['before'],
                            'target': order['after']
                        }
                    })

        elif 'overlaps' in order:
            pass
        elif 'contained' in order and 'container' in order:
            for node in nodes:
                if node['data']['id'] == order['contained']:
                    node['data']['parent'] = order['container']
        else:
            pass
    
    return {
        'nodes': nodes,
        'edges': edges
    }

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    schema_string = file.read().decode("utf-8")
    schema = json.loads(schema_string)['schemas'][0]
    parsed_schema = parse(schema)
    return json.dumps(parsed_schema)