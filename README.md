# visualize_openvino_ir
Netron can't visualize large model(OpenVINO IR), just customize a script to display model fragments quickly.

# dependencies

#### Linux
    pip install graphviz

#### Windows
    pip install graphviz
    Download:windows_10_cmake_Release_graphviz-install-11.0.0-win64.exe from https://www.graphviz.org/download/, and then default install.

# Usage

    <!-- source ov -->
    source openvino/install/setupvars.sh

    <!-- Show subgraph based on id -->
    python main.py -m $model -id $layer_id  --top 10 --bottom 1 --ignore_const -highlight MatMul,Slice,FullyConnected,Split

    <!-- Show subgraph based on multiple ids -->
    python main.py -m $model -ids 123,456,789 --top 5 --bottom 2 --ignore_const

    <!-- Show subgraph based on multiple names -->
    python main.py -m $model -names layer_a,layer_b --top 5 --bottom 2 --ignore_const

    <!-- Show graph -->
    python main.py -m $model

    Linux refer: run.sh
    Windows refer: run.bat