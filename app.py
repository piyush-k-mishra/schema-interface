from flask import Flask, render_template, request
import json

app = Flask(__name__, static_folder='./static', template_folder='./static')
json_string = ''

nodes = []
edges = []

def get_nodes_and_edges(schema):
    node = []
    edges = []

    nodes.append({
        'data': {
            'id': 'root',
            'label': schema['name'],
            'shape': 'round-rectangle'
        }
    })

    for step in schema['steps']:
        nodes.append({
            'data': {
                'id': step['@id'], 
                'label': step['@id'].split('/')[-1].replace('_', ' '),
                'type': 'step',
                '@type': step['@type'],
                'shape': 'ellipse'
            }
        })

        edges.append({
            'data': {
                'id': f"root_{step['@id']}",
                'label': '',
                'source': 'root',
                'target': step['@id'],
                'edge_type': 'root_step'
            },
            'classes': 'root-edge'
        })

        if 'slots' in step:
            for slot in step['slots']:
                nodes.append({
                    'data': {
                        'id': slot['@id'], 
                        'label': slot['name'],
                        'type': 'slot',
                        '@role': slot['role'],
                        'shape': 'round-pentagon'
                    }
                })
                edges.append({
                    'data': {
                        'id': f"{step['@id']}_{slot['@id']}",
                        'label': '',
                        'source': step['@id'],
                        'target': slot['@id'],
                        'edge_type': 'step_slot'
                    }
                })

                if 'values' in slot:
                    for value in slot['values']:
                        nodes.append({
                            'data': {
                                'id': value['valueId'], 
                                'label': value['value'],
                                'type': 'value',
                                'shape': 'round-hexagon'
                            }
                        })
                        edges.append({
                            'data': {
                                'id': f"{slot['@id']}_{value['valueId']}",
                                'label': '',
                                'source': slot['@id'],
                                'target': value['valueId'],
                                'edge_type': 'slot_value'
                            }
                        })
                if 'entityTypes' in slot:
                    if isinstance(slot['entityTypes'], str):
                        nodes.append({
                            'data': {
                                'id': slot['entityTypes'], 
                                'label': slot['entityTypes'].split(':')[-1],
                                'type': 'entityType',
                                'shape': 'round-octagon'
                            }
                        })
                        edges.append({
                            'data': {
                                'id': f"{slot['@id']}_{slot['entityTypes']}",
                                'label': '',
                                'source': slot['@id'],
                                'target': slot['entityTypes'],
                                'edge_type': 'slot_etype'
                            }
                        })
                            
                    else:
                        for entityType in slot['entityTypes']:
                            nodes.append({
                                'data': {
                                    'id': entityType, 
                                    'label': entityType.split(':')[-1],
                                    'type': 'entityType',
                                    'shape': 'round-octagon'
                                }
                            })
                            edges.append({
                                'data': {
                                    'id': f"{slot['@id']}_{entityType}",
                                    'label': '',
                                    'source': slot['@id'],
                                    'target': entityType,
                                    'edge_type': 'slot_etype'
                                }
                            })
    
    for order in schema['order']:
        if 'flags' in order:
            if order['flags'] == 'precondition':
                if isinstance(order['before'], list):
                    for before in order['before']:
                        edges.append({
                            'data': {
                                'id': f"{before}_{order['after']}",
                                'label': 'Before',
                                'source': before,
                                'target': order['after'],
                                'edge_type': 'step_step'
                            }
                        })
                else:
                    edges.append({
                        'data': {
                            'id': f"{order['before']}_{order['after']}",
                            'label': 'Before',
                            'source': order['before'],
                            'target': order['after'],
                            'edge_type': 'step_step'
                        }
                    })

        elif 'overlaps' in order:
            parent_id = "_".join([node_id.split("/")[-1] for node_id in order['overlaps']])
            for node_id in order['overlaps']:
                node = get_node_by_id(node_id)
                node['data']['parent'] = parent_id
            nodes.append({
                "data": {"id": parent_id}
            })
        elif 'contained' in order and 'container' in order:
            for node in nodes:
                if node['data']['id'] == order['contained']:
                    node['data']['parent'] = order['container']
        else:
            if 'before' in order:
                if isinstance(order['before'], list):
                    for before in order['before']:
                        edges.append({
                            'data': {
                                'id': f"{before}_{order['after']}",
                                'label': 'Before',
                                'source': before,
                                'target': order['after'],
                                'edge_type': 'step_step'
                            },
                            'classes': 'optional-before'
                        })
                else:
                    edges.append({
                        'data': {
                            'id': f"{order['before']}_{order['after']}",
                            'label': 'Before',
                            'source': order['before'],
                            'target': order['after'],
                            'edge_type': 'step_step'
                        },
                        'classes': 'optional-before'
                    })
    
    return nodes, edges

def get_node_by_id(node_id):
    for node in nodes:
        if node['data']['id'] == node_id:
            return node

def get_connencted_nodes(selected_node):
    n = []
    e = []
    id_set = set()

    if selected_node == 'root':
        id_set.add(selected_node)
        for edge in edges:
            if edge['data']['source'] == selected_node:
                e.append(edge)
                id_set.add(edge['data']['target'])
        for node in nodes:
            if node['data']['id'] in id_set:
                n.append(node)
                if 'parent' in node['data']:
                    parent_node = get_node_by_id(node['data']['parent'])
                    if parent_node not in n:
                        n.append(parent_node)
        for edge in edges:
            if edge['data']['source'] in id_set and edge['data']['target'] in id_set:
                if edge not in e:
                    e.append(edge)
    else:
        for edge in edges:
            if edge['data']['source'] == selected_node and edge not in e:
                e.append(edge)
                node = get_node_by_id(edge['data']['target'])
                if node['data']['type'] == 'slot':
                    n.append(node)
                    id_set.add(node['data']['id'])
        for edge in edges:
            if edge['data']['source'] in id_set or edge['data']['target'] in id_set:
                if edge not in e:
                    e.append(edge)
                    source_node = get_node_by_id(edge['data']['source'])
                    target_node = get_node_by_id(edge['data']['target'])
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
    parsed_schema = get_connencted_nodes('root')
    return json.dumps(parsed_schema)

@app.route('/node', methods=['GET'])
def get_subtree():
    node_id = request.args.get('ID')
    subtree = get_connencted_nodes(node_id)
    return json.dumps(subtree)
