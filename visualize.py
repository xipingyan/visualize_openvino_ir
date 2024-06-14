from read_ir import OV_IR, Layer, Edge
import graphviz
import os, platform

if platform.system() == 'Windows':
    # print("os.pathsep=", os.path.dirname(os.path.abspath(__file__)) + "\python-env\Lib\site-packages\graphviz")
    os.environ["PATH"] += os.pathsep + os.path.dirname(os.path.abspath(__file__)) + "\python-env\Lib\site-packages\graphviz"

def print_splitter():
    print("=======================================================")

def visualize_via_name(ir:OV_IR, layer_name=None, top=3, bottom=1):
    pass

def visualize_via_id(ir:OV_IR, layer_id=None, top=3, bottom=1):
    dot = graphviz.Digraph()

    cur_layer = ir.get_layer(layer_id)
    if cur_layer is None:
        print(f"Can't find layer_id[{layer_id}] in IR. Exit.")
        return

    # Draw current node.
    dot.node(cur_layer.id, cur_layer.type)
    pair_edges=[]
    for parent_id in ir.get_parent_ids(layer_id=layer_id):
        # node pair (parent id -> current id)
        pair_edges.append((parent_id, cur_layer.id))

    # Draw parent
    for t in range(top):
        next_ids=[]
        for parent_id, current_id in pair_edges:
            parent_layer = ir.get_layer(parent_id)
            dot.node(parent_layer.id, parent_layer.type)
            dot.edge(parent_layer.id, current_id, "")

            for new_parent_id in ir.get_parent_ids(parent_id):
                next_ids.append((new_parent_id, parent_id))
        pair_edges=next_ids

    # dot.render('graph', view=True)
    dot.view()


def visualize(ir:OV_IR, layer_name=None, layer_id=None, top=3, bottom=1):
    print('Call:', __name__)
    print(layer_name)
    if layer_name is not None:
        visualize_via_name(ir, layer_name=layer_name, top=top, bottom=bottom)
    elif layer_id is not None:
        visualize_via_id(ir, layer_id=layer_id, top=top, bottom=bottom)
    pass