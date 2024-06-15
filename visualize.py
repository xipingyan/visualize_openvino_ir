from read_ir import OV_IR, Layer, Edge
import graphviz
import os, platform

if platform.system() == 'Windows':
    os.environ["PATH"] += os.pathsep + "C:\\Program Files\\Graphviz\\bin"

def print_splitter():
    print("=======================================================")

def draw_graph(all_nodes:list[Layer], all_edges:list, highligt_nodes:list, cur_node:Layer=None):
    dot = graphviz.Digraph()
    for layer in all_nodes:
        show_name=layer.type+":"+layer.id+"\n"
        for output in layer.output:
            show_name=show_name+str(output['shape'])+":"+output["element_type"]+"\n"

        color=None
        style=None
        if layer.type == "Parameter":
            color = 'lightgrey'
            style = 'filled'
        elif cur_node != None and layer.name == cur_node.name:
            color = 'lightgreen'
            style = 'filled'
        elif layer.type in highligt_nodes:
            color = 'lightblue'
            style = 'filled'
        elif layer.type in ["Reorder"]:
            color = 'red'

        dot.node(layer.id, show_name, style=style, color=color)
    for parent_id, cur_id, name in all_edges:
        dot.edge(parent_id, cur_id, name)
    dot.view()

def visualize_via_name(ir:OV_IR, layer_name=None, top=3, bottom=1, ignore_const=False, highlight_nodes=[]):
    layer = ir.get_layer_via_name(layer_name)
    if layer is None:
        print("Error: can't find layer via layer name:", layer_name)
        return None
    else:
        visualize_via_id(ir, layer.id, top, bottom, ignore_const, highlight_nodes)

def visualize_via_id(ir:OV_IR, layer_id=None, top=3, bottom=1, ignore_const=False, highlight_nodes=[]):
    all_nodes=set()
    all_edges=set()

    cur_layer = ir.get_layer_via_id(layer_id)
    if cur_layer is None:
        print(f"Can't find layer_id[{layer_id}] in IR. Exit.")
        return

    # Grab current node.
    if (ignore_const and cur_layer.type == 'Const') is False:
        all_nodes.add(cur_layer)
    pair_edges=[]
    for parent_id in ir.get_parent_ids(layer_id=layer_id):
        # node pair (parent id -> current id)
        if (ignore_const and ir.get_layer_via_id(parent_id).type == 'Const') is False:
            pair_edges.append((parent_id, cur_layer.id))

    # Grab parent
    for t in range(top):
        next_ids=[]
        for parent_id, current_id in pair_edges:
            parent_layer = ir.get_layer_via_id(parent_id)
            if (ignore_const and parent_layer.type == 'Const') is False:
                all_nodes.add(parent_layer)
                all_edges.add((parent_layer.id, current_id, ""))

            for new_parent_id in ir.get_parent_ids(parent_id):
                next_ids.append((new_parent_id, parent_id))
        pair_edges=next_ids
    
    # Grap son
    next_ids=[]
    for son_id in ir.get_son_ids(layer_id=cur_layer.id):
        # node pair (parent id -> current id)
        pair_edges.append((cur_layer.id, son_id))

    for t in range(bottom):
        for current_id, son_id in pair_edges:
            son_layer = ir.get_layer_via_id(son_id)
            all_nodes.add(son_layer)
            all_edges.add((current_id, son_id, ""))

            for new_son_id in ir.get_son_ids(son_id):
                next_ids.append((son_id, new_son_id))
        pair_edges=next_ids


    # Draw.
    draw_graph(all_nodes, all_edges, highlight_nodes, cur_layer)

def visualize_all(ir:OV_IR, ignore_const=False, highlight_nodes=[]):
    all_nodes=set()
    all_edges=set()
    for layer in ir.get_layers():
        all_nodes.add(layer)
    for edge in ir.get_edges():
        all_edges.add((edge.from_layer, edge.to_layer, ""))

    # Draw.
    draw_graph(all_nodes, all_edges, highlight_nodes, None)

def visualize(ir:OV_IR, layer_name=None, layer_id=None, top=3, bottom=1, ignore_const=False, highlight_nodes=[]):
    print('Call:', __name__)
    print(layer_name)
    if layer_name is not None:
        visualize_via_name(ir, layer_name=layer_name, top=top, bottom=bottom, ignore_const=ignore_const, highlight_nodes=highlight_nodes)
    elif layer_id is not None:
        visualize_via_id(ir, layer_id=layer_id, top=top, bottom=bottom, ignore_const=ignore_const, highlight_nodes=highlight_nodes)
    else:
        visualize_all(ir, ignore_const=ignore_const, highlight_nodes=highlight_nodes)