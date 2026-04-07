try:
    from .read_ir import OV_IR, Layer, Edge
except ImportError:
    from read_ir import OV_IR, Layer, Edge
import graphviz
import os, platform

if platform.system() == 'Windows':
    os.environ["PATH"] += os.pathsep + "C:\\Program Files\\Graphviz\\bin"

def print_splitter():
    print("=======================================================")

def draw_graph(all_nodes:list[Layer], all_edges:list, highligt_nodes:list, cur_node:Layer=None, cur_nodes:list[Layer]=None, output="result_graph", draw_tid=False):
    dot = graphviz.Digraph(name="Graph", filename=output)
    focus_ids = set()
    if cur_node is not None:
        focus_ids.add(cur_node.id)
    if cur_nodes is not None:
        for node in cur_nodes:
            focus_ids.add(node.id)

    for layer in all_nodes:
        show_name=layer.type+":"+layer.id+"\n"
        for output_att in layer.output:
            show_name=show_name+str(output_att['shape'])+":"+output_att["element_type"]+"\n"+layer.name+"\n"

        color=None
        style=None
        if layer.type == "Parameter":
            color = 'lightgrey'
            style = 'filled'
        elif layer.id in focus_ids:
            color = 'lightgreen'
            style = 'filled'
        elif layer.type in highligt_nodes:
            color = 'lightblue'
            style = 'filled'
        elif layer.type in ["Reorder"]:
            color = 'lightyellow'
            style = 'filled'

        if draw_tid:
            color_list = ['red', 'blue', 'yellow', 'green']
            color = color_list[layer.thread_id % len(color_list)]

        dot.node(layer.id, show_name, style=style, color=color)
    for parent_id, cur_id, name in all_edges:
        dot.edge(parent_id, cur_id, name)
    # dot.view()
    print(f"== start dot.render()")
    dot.render()
    print(f"== Done!\n== Save graph to ./{output}.pdf")

def collect_subgraph(ir:OV_IR, root_ids:list[str], top=3, bottom=1, ignore_const=False):
    all_nodes=set()
    all_edges=set()
    valid_roots=[]

    for layer_id in root_ids:
        cur_layer = ir.get_layer_via_id(layer_id)
        if cur_layer is None:
            print(f"Warning: Can't find layer_id[{layer_id}] in IR. Skip.")
            continue

        valid_roots.append(cur_layer)
        print(f"== Start visualize layer_id[{layer_id}], layer_name[{cur_layer.name}], layer_type[{cur_layer.type}]")

        # Grab current node.
        if (ignore_const and cur_layer.type == 'Const') is False:
            all_nodes.add(cur_layer)

        # Grab parent
        pair_edges=[]
        print(f"== Grab parent nodes of layer_id[{layer_id}]")
        for parent_id in ir.get_parent_ids(layer_id=layer_id):
            parent_layer = ir.get_layer_via_id(parent_id)
            if parent_layer is None:
                continue
            if (ignore_const and parent_layer.type == 'Const') is False:
                pair_edges.append((parent_id, cur_layer.id))
                print(f"    parent_id[{parent_id}] -> layer_id[{layer_id}]")

        print(f"== Grab parent nodes of layer_id[{layer_id}] with top={top}")
        for t in range(top):
            next_ids=[]
            for parent_id, current_id in pair_edges:
                parent_layer = ir.get_layer_via_id(parent_id)
                if parent_layer is None:
                    continue
                if (ignore_const and parent_layer.type == 'Const') is False:
                    all_nodes.add(parent_layer)
                    all_edges.add((parent_layer.id, current_id, ""))

                for new_parent_id in ir.get_parent_ids(parent_id):
                    next_ids.append((new_parent_id, parent_id))
            pair_edges=next_ids.copy()  # Avoid reference issue, make a copy of list.
            next_ids=[]

        # Grab son
        print(f"== Grab son nodes of layer_id[{layer_id}]")
        pair_edges=[]
        next_ids=[]
        for son_id in ir.get_son_ids(layer_id=cur_layer.id):
            pair_edges.append((cur_layer.id, son_id))

        print(f"== Grab son nodes of layer_id[{layer_id}] with bottom={bottom}")
        for t in range(bottom):
            for current_id, son_id in pair_edges:
                son_layer = ir.get_layer_via_id(son_id)
                if son_layer is None:
                    continue
                if (ignore_const and son_layer.type == 'Const') is False:
                    all_nodes.add(son_layer)
                    all_edges.add((current_id, son_id, ""))

                for new_son_id in ir.get_son_ids(son_id):
                    next_ids.append((son_id, new_son_id))
            pair_edges=next_ids.copy()
            next_ids=[]

    return all_nodes, all_edges, valid_roots

def visualize_via_name(ir:OV_IR, layer_name=None, top=3, bottom=1, ignore_const=False, highlight_nodes=[], output="result_graph", draw_tid=False):
    layer = ir.get_layer_via_name(layer_name)
    if layer is None:
        print("Error: can't find layer via layer name:", layer_name)
        return None
    else:
        visualize_via_id(ir, layer.id, top, bottom, ignore_const, highlight_nodes, output=output, draw_tid=draw_tid)

def visualize_via_names(ir:OV_IR, layer_names=None, top=3, bottom=1, ignore_const=False, highlight_nodes=[], output="result_graph", draw_tid=False):
    if layer_names is None:
        return
    layer_ids=[]
    for layer_name in layer_names:
        layer = ir.get_layer_via_name(layer_name)
        if layer is None:
            print("Warning: can't find layer via layer name:", layer_name)
            continue
        layer_ids.append(layer.id)
    visualize_via_ids(ir, layer_ids, top, bottom, ignore_const, highlight_nodes, output=output, draw_tid=draw_tid)

def visualize_via_id(ir:OV_IR, layer_id=None, top=3, bottom=1, ignore_const=False, highlight_nodes=[], output="result_graph",draw_tid=False):
    visualize_via_ids(ir, [layer_id], top, bottom, ignore_const, highlight_nodes, output=output, draw_tid=draw_tid)

def visualize_via_ids(ir:OV_IR, layer_ids=None, top=3, bottom=1, ignore_const=False, highlight_nodes=[], output="result_graph",draw_tid=False):
    if layer_ids is None or len(layer_ids) == 0:
        print("Error: Empty layer_ids.")
        return

    all_nodes, all_edges, cur_layers = collect_subgraph(
        ir, layer_ids, top=top, bottom=bottom, ignore_const=ignore_const
    )
    if len(cur_layers) == 0:
        print("Error: all input layer_ids are invalid. Exit.")
        return

    # Draw.
    print(f"== Start drawing graph with node number={len(all_nodes)}, edge number={len(all_edges)}")
    draw_graph(all_nodes, all_edges, highlight_nodes, cur_nodes=cur_layers, output=output, draw_tid=draw_tid)

def visualize_all(ir:OV_IR, ignore_const=False, highlight_nodes=[], output="result_graph", draw_tid=False):
    all_nodes=set()
    all_edges=set()
    for layer in ir.get_layers():
        all_nodes.add(layer)
    for edge in ir.get_edges():
        all_edges.add((edge.from_layer, edge.to_layer, ""))

    # Draw.
    draw_graph(all_nodes, all_edges, highlight_nodes, None, output=output, draw_tid=draw_tid)

def visualize(ir:OV_IR, layer_name=None, layer_id=None, layer_names=None, layer_ids=None, top=3, bottom=1, ignore_const=False, highlight_nodes=[], output="result_graph", draw_tid=False):
    print('== Call:', __name__)
    if layer_names is not None and len(layer_names) > 0:
        visualize_via_names(ir, layer_names=layer_names, top=top, bottom=bottom, ignore_const=ignore_const, highlight_nodes=highlight_nodes, output=output)
    elif layer_ids is not None and len(layer_ids) > 0:
        visualize_via_ids(ir, layer_ids=layer_ids, top=top, bottom=bottom, ignore_const=ignore_const, highlight_nodes=highlight_nodes, output=output)
    elif layer_name is not None:
        visualize_via_name(ir, layer_name=layer_name, top=top, bottom=bottom, ignore_const=ignore_const, highlight_nodes=highlight_nodes, output=output)
    elif layer_id is not None:
        visualize_via_id(ir, layer_id=layer_id, top=top, bottom=bottom, ignore_const=ignore_const, highlight_nodes=highlight_nodes, output=output)
    else:
        visualize_all(ir, ignore_const=ignore_const, highlight_nodes=highlight_nodes, output=output, draw_tid=draw_tid)