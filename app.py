from flask import Flask, render_template, request
import json

app = Flask(__name__, static_folder='./static', template_folder='./static')
json_string = ''

nodes = {}
edges = []

schema_key_dict = {
    'root': ['@id', 'super', 'name', 'description', 'comment'],
    'step': ['@id', '@type', 'aka', 'reference', 'provenance'],
    'slot': ['@id', 'name', 'aka', 'role', 'entityTypes', 'comment', 'reference'],
    'value': ['valueId', 'value', 'entityTypes', 'mediaType', 'confidence', 'provenance']
}

def create_node(_id, _label, _type, _shape=''):
    return {
        'data': {
            'id': _id,
            '_label': _label if _label else _id,
            '_type': _type,
            '_shape': _shape
        },
        'classes': ''
    }

def create_edge(_id, _source, _target, _label='', _edge_type=''):
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

def extend_node(node, obj):
    for key in obj.keys():
        if key in schema_key_dict[node['data']['_type']]:
            node['data'][key] = obj[key]
    return node

def handle_precondition(order, label='Precondition'):
    e = []
    if isinstance(order['before'], list):
        for before_id in order['before']:
            if isinstance(order['after'], list):
                for after_id in order['after']:
                    e_id = f"{before_id}_{after_id}"
                    e.append(create_edge(e_id, before_id, after_id, label, 'step_step'))
            else:
                e_id = f"{before_id}_{order['after']}"
                e.append(create_edge(e_id, before_id, order['after'], label, 'step_step'))
    else:
        if isinstance(order['after'], list):
            for after_id in order['after']:
                e_id = f"{order['before']}_{after_id}"
                e.append(create_edge(e_id, order['before'], after_id, label, 'step_step'))
        else:
            e_id = f"{order['before']}_{order['after']}"
            e.append(create_edge(e_id, order['before'], order['after'], label, 'step_step'))
    return e

def handle_optional(_order):
    print(_order)

def handle_flags(_flag, _order):
    switcher={
        'precondition': handle_precondition,
        'optional': handle_optional
    }
    func = switcher.get(_flag, lambda *args: None)
    return func(_order)

def get_nodes_and_edges(schema):
    nodes = {}
    edges = []
    steps_to_connect = []
    
    nodes['root'] = extend_node(create_node('root', 'Start', 'root', 'round-rectangle'), schema)

    for step in schema['steps']:
        _label = step['@id'].split('/')[-1].replace('_', ' ')
        nodes[step['@id']] = extend_node(create_node(step['@id'], _label, 'step', 'ellipse'), step)

        steps_to_connect.append(step['@id'])

        if 'slots' in step:
            for slot in step['slots']:
                nodes[slot['@id']] = extend_node(create_node(slot['@id'], slot['name'], 'slot', 'round-pentagon'), slot)
                
                e_id = f"{step['@id']}_{slot['@id']}"
                edges.append(create_edge(e_id, step['@id'], slot['@id'], _edge_type='step_slot'))

                if 'values' in slot:
                    for value in slot['values']:
                        nodes[value['valueId']] = create_node(value['valueId'], value['value'], 'value', 'round-diamond')

                        e_id = f"{slot['@id']}_{value['valueId']}"
                        edges.append(create_edge(e_id, slot['@id'], value['valueId'], _edge_type='slot_value'))
    
    for order in schema['order']:
        if 'overlaps' in order:
            pass
            # for node_id in order['overlaps']:
            #     node = get_node_by_id(node_id)
            #     node['classes'] = ' overlapped'
        elif 'contained' in order and 'container' in order:
            if nodes[order['contained']]:
                nodes[order['contained']]['data']['parent'] = order['container']
        elif 'before' in order and 'after' in order:
            e = []
            
            if 'flags' in order:
                e = handle_flags(order['flags'], order)
            else:
                e = handle_precondition(order, 'Before')
                for entry in e:
                    entry['classes'] = 'optional-before'
            
            edges.extend(e)
            
            if isinstance(order['after'], list):
                for step_id in order['after']:
                    if step_id in steps_to_connect:
                        steps_to_connect.remove(step_id)
            else:
                if order['after'] in steps_to_connect:
                        steps_to_connect.remove(order['after'])

    for step in steps_to_connect:
        e = create_edge(f"root_{step}", 'root', step, _edge_type='root_step')
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
    schemaJson = json.loads(schema_string)['schemas']
    schema = schemaJson[0]
    global nodes
    global edges
    nodes, edges = get_nodes_and_edges(schema)
    schema_name = schema['name']
    parsed_schema = get_connencted_nodes('root')
    return json.dumps({
        'parsedSchema': parsed_schema,
        'name': schema['name'],
        'schemaJson': schemaJson
    })

@app.route('/node', methods=['GET'])
def get_subtree():
    if not (bool(nodes) and bool(edges)):
        return 'Parsing error! Upload the file again.', 400
    node_id = request.args.get('ID')
    subtree = get_connencted_nodes(node_id)
    return json.dumps(subtree)
