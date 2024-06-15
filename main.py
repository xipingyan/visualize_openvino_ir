import argparse
# import OV_IR from read_ir
from read_ir import OV_IR
from visualize import visualize

def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument("-m", "--model", help="OpenVINO IR, xml file.", required=True)
    parser.add_argument("-id", "--layer_id", help="Visualize snippet of Graph based on this layer id.")
    parser.add_argument("-name", "--layer_name", help="Visualize snippet of Graph based on this layer name.")
    parser.add_argument("-t", "--top", type=int, default=3, help="Visualize layer number on the top of specific layer.")
    parser.add_argument("-b", "--bottom", type=int, default=1, help="Visualize layer number on the bottom of specific layer.")
    parser.add_argument("-ic", "--ignore_const", action="store_true")
    parser.add_argument("-highlight", "--highlight_nodes", help="Highlight display node with color, input types, split with ',', for example: MatMul,Multiply,FullyConnected")
    parser.add_argument("-o", "--output", default="result_graph", help="Output graph diagram, pdf file, for example: -o graph")

    args = parser.parse_args()

    print(f"== Input parameters:")
    prefix="    "
    print(f"{prefix}model={args.model}")
    if args.layer_name != None:
        print(f"{prefix}layer_name={args.layer_name}")
    if args.layer_id != None:
        print(f"{prefix}layer_id={args.layer_id}")

    print(f"{prefix}top={args.top}")
    print(f"{prefix}bottom={args.bottom}")
    highlight_nodes=[]
    if args.highlight_nodes != None:
        highlight_nodes = str(args.highlight_nodes).split(',')

    ir = OV_IR(xml_fn=args.model)

    visualize(ir, layer_name=args.layer_name, layer_id=args.layer_id,
              top=args.top, bottom=args.bottom, ignore_const=args.ignore_const, 
              highlight_nodes=highlight_nodes, output=args.output)

if __name__ == "__main__":
    main()
