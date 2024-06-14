# visualize_openvino_ir
Netron can't visualize large model, just customize a script to display snippet of a model quickly.

# dependencies

    pip install graphviz

# Usage

    <!-- Show subgraph based on id -->
    python main.py -m $model -id $layer_id  --top 10 --bottom 1 --ignore_const -hn 'MatMul'

    <!-- Show graph -->
    python main.py -m $model