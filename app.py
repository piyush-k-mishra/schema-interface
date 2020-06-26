from flask import Flask, render_template, request
import json

app = Flask(__name__, static_folder='./static', template_folder='./static')
json_string = ''

nodes = {}
edges = []

schema_key_dict = {
    'schema': ['@id', 'super', 'name'],
    'step': ['@id', '@type', 'aka'],
    'slot': ['@id', 'name', 'aka', 'role', 'entityTypes'],
    'value': ['valueId', 'value', 'entityTypes']
}

def createNode(_id, _label, _type, _shape=''):
    return {
        'data': {
            'id': _id,
            '_label': _label if _label else _id,
            '_type': _type,
            '_shape': _shape
        },
        'classes': ''
    }

def createEdge(_id, _source, _target, _label='', _edge_type=''):
    return {
        'data': {
            'id': _id,
            '_label': _label,
            'source': _source,
            'target': _target,
            '_edge_type': _edge_type
        },
        'classes': ''
    }

def get_nodes_and_edges(schema):
    nodes = {}
    edges = []
    steps_to_connect = []
    
    nodes['root'] = createNode('root', 'Start', 'root', 'round-rectangle')

    for step in schema['steps']:
        _label = step['@id'].split('/')[-1].replace('_', ' ')
        nodes[step['@id']] = createNode(step['@id'], _label, 'step', 'ellipse')

        steps_to_connect.append(step['@id'])

        if 'slots' in step:
            for slot in step['slots']:
                nodes[slot['@id']] = createNode(slot['@id'], slot['name'], 'slot', 'round-pentagon')
                
                e_id = f"{step['@id']}_{slot['@id']}"
                edges.append(createEdge(e_id, step['@id'], slot['@id'], _edge_type='step_slot'))

                if 'values' in slot:
                    for value in slot['values']:
                        nodes[value['valueId']] = createNode(value['valueId'], value['value'], 'value', 'round-diamond')

                        e_id = f"{slot['@id']}_{value['valueId']}"
                        edges.append(createEdge(e_id, slot['@id'], value['valueId'], _edge_type='slot_value'))
    
    for order in schema['order']:
        if 'flags' in order:
            if order['flags'] == 'precondition':
                if isinstance(order['before'], list):
                    for before in order['before']:
                        e_id = f"{before}_{order['after']}"
                        edges.append(createEdge(e_id, before, order['after'], 'Precondition', 'step_step'))
                        if order['after'] in steps_to_connect:
                            steps_to_connect.remove(order['after'])
                else:
                    e_id = f"{order['before']}_{order['after']}"
                    edges.append(createEdge(e_id, order['before'], order['after'], 'Precondition', 'step_step'))
                    
                    if order['after'] in steps_to_connect:
                        steps_to_connect.remove(order['after'])


        elif 'overlaps' in order:
            pass
            # for node_id in order['overlaps']:
            #     node = get_node_by_id(node_id)
            #     node['classes'] = ' overlapped'
        elif 'contained' in order and 'container' in order:
            if nodes[order['contained']]:
                nodes[order['contained']]['data']['parent'] = order['container']
        else:
            if 'before' in order:
                if isinstance(order['before'], list):
                    for before in order['before']:
                        e_id = f"{before}_{order['after']}"
                        e = createEdge(e_id, before, order['after'], 'Before', 'step_step')
                        e['classes'] = 'optional-before'
                        edges.append(e)

                        if order['after'] in steps_to_connect:
                            steps_to_connect.remove(order['after'])
                else:
                    e_id = f"{order['before']}_{order['after']}"
                    e = createEdge(e_id, order['before'], order['after'], 'Before', 'step_step')
                    e['classes'] = 'optional-before'
                    edges.append(e)
                    
                    if order['after'] in steps_to_connect:
                        steps_to_connect.remove(order['after'])

    for step in steps_to_connect:
        e = createEdge(f"root_{step}", 'root', step, _edge_type='root_step')
        e['classes'] = 'root-edge'
        edges.append(e)
        
    return nodes, edges

def get_connencted_nodes(selected_node):
    n = []
    e = []
    id_set = set()

    if selected_node == 'root':
        n.append(nodes[selected_node])
        for key, node in nodes.items():
            if node['data']['_type'] == 'step':
                n.append(node)
        for edge in edges:
            if edge['data']['_edge_type'] == 'step_step' or edge['data']['_edge_type'] == 'root_step':
                e.append(edge)
    else:
        for edge in edges:
            if edge['data']['source'] == selected_node and edge not in e:
                e.append(edge)
                node = nodes[edge['data']['target']]
                if node['data']['_type'] == 'slot':
                    n.append(node)
                    id_set.add(node['data']['id'])
        for edge in edges:
            if edge['data']['source'] in id_set or edge['data']['target'] in id_set:
                if edge not in e:
                    e.append(edge)
                    source_node = nodes[edge['data']['source']]
                    target_node = nodes[edge['data']['target']]
                    if source_node not in n:
                        n.append(source_node)
                    if target_node not in n:
                        n.append(target_node)
            
    return {
        'nodes': n,
        'edges': e
    }

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    schema_string = file.read().decode("utf-8")
    schema = json.loads(schema_string)['schemas'][0]
    global nodes
    global edges
    nodes, edges = get_nodes_and_edges(schema)
    schema_name = schema['name']
    parsed_schema = get_connencted_nodes('root')
    return json.dumps({
        'parsedSchema': parsed_schema,
        'name': schema['name']
    })

@app.route('/node', methods=['GET'])
def get_subtree():
    if not (bool(nodes) and bool(edges)):
        return 'Parsing error! Upload the file again.', 400
    node_id = request.args.get('ID')
    subtree = get_connencted_nodes(node_id)
    return json.dumps(subtree)
