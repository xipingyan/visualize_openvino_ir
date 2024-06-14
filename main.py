import argparse
# import OV_IR from read_ir
from read_ir import OV_IR
from visualize import visualize

def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument("-m", "--model", help="OpenVINO IR, xml file.", required=True)
    parser.add_argument("-name", "--layer_name", help="Visualize snippet of Graph based on this layer name.")
    parser.add_argument("-id", "--layer_id", help="Visualize snippet of Graph based on this layer id.")
    parser.add_argument("-t", "--top", type=int, default=3, help="Visualize layer number on the top of specific layer.")
    parser.add_argument("-b", "--bottom", type=int, default=1, help="Visualize layer number on the bottom of specific layer.")
    parser.add_argument("-ic", "--ignore_const", action="store_true")

    args = parser.parse_args()

    print(f"model={args.model}")
    if args.layer_name != None:
        print(f"layer_name={args.layer_name}")
    if args.layer_id != None:
        print(f"layer_id={args.layer_id}")

    print(f"top={args.top}")
    print(f"bottom={args.bottom}")

    ir = OV_IR(xml_fn=args.model)

    visualize(ir, layer_name=args.layer_name, layer_id=args.layer_id, top=args.top, bottom=args.bottom, ignore_const=args.ignore_const)

if __name__ == "__main__":
    main()
