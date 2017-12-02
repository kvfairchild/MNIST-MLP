from .node import Node
from .gate_factory import gate_factory
from .slot_factory import slot_factory

NODE_TYPES = {
    "register": [
        [ "gen" ],
        [ "gen" ]
    ],
    "sensor": [
        [ "gen" ]
    ],
    "actuator": [
        [ "gen" ]
    ],    
    "concept": [
        [ "gen" ],
        [ "gen", "por", "ret", "sub", "sur", "cat", "exp", "sym", "ref" ]
    ]
}

def node_factory(node_data):
    # return a list of nodes, generated from node types based on a list of names
    if len(node_data) > 0:
        layers = []
        for layer_index, layer in enumerate(node_data):
            if layer_index < len(node_data)-1:
                node = [Node(node[0], *_get_slots_and_gates(*NODE_TYPES.get(node[1]))) for node in layer]
                layers.append(node)
            else:
                node = [Node(node[0], *_get_output_slots_and_gates(*NODE_TYPES.get(node[1]))) for node in layer]
                layers.append(node)
        return layers
    else:
        raise ValueError("please pass in node data or number of nodes to create")

def _get_slots_and_gates(slot_names, gate_names):
    return [
        slot_factory(slot_names),
        gate_factory(gate_names, is_output_node=False)
    ]

def _get_output_slots_and_gates(slot_names, gate_names):
    return [
        slot_factory(slot_names),
        gate_factory(gate_names, is_output_node=True)
    ]
