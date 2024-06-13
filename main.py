import argparse
# import OV_IR from read_ir
from read_ir import OV_IR

def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument("-m", "--model", help="OpenVINO IR, xml file.", required=True)
    parser.add_argument("-layer", "--layer_name", help="Visualize snippet of Graph if set.")
    parser.add_argument("-t", "--top", default=3, help="Visualize layer number on the top of specific layer.")
    parser.add_argument("-b", "--bottom", default=1, help="Visualize layer number on the bottom of specific layer.")

    args = parser.parse_args()

    print(f"model={args.model}")
    print(f"layer_name={args.layer_name}")
    print(f"top={args.top}")
    print(f"bottom={args.bottom}")

    ir = OV_IR(args.model)

if __name__ == "__main__":
    main()
