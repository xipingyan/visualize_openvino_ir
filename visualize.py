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
    
    dot.node(cur_layer.id, cur_layer.name)

    # Draw top
    cur_ids=ir.get_parent_edgs(layer_id=layer_id)
    cur_ids = [[cur_ids[0], layer_id]]
    for t in range(top):
        next_ids=[]
        for id in cur_ids:
            cur_layer = ir.get_layer(id[0])
            dot.node(cur_layer.id, cur_layer.name)
            dot.edge(cur_layer.id, id[1], "")
            for x in ir.get_parent_edgs(cur_layer.id):
                next_ids.append([x, cur_layer.id])
        cur_ids=next_ids

    dot.render('graph', view=True)

def visualize(ir:OV_IR, layer_name=None, layer_id=None, top=3, bottom=1):
    print('Call:', __name__)
    print(layer_name)
    if layer_name is not None:
        visualize_via_name(ir, layer_name=layer_name, top=top, bottom=bottom)
    elif layer_id is not None:
        visualize_via_id(ir, layer_id=layer_id, top=top, bottom=bottom)
    pass