# visualize_openvino_ir
Netron can't visualize large model(OpenVINO IR), just customize a script to display model fragments quickly.

# dependencies

#### Linux
    pip install graphviz

#### Windows
    pip install graphviz
    Download:windows_10_cmake_Release_graphviz-install-11.0.0-win64.exe from https://www.graphviz.org/download/, and then default install.

# Usage

    <!-- Show subgraph based on id -->
    python main.py -m $model -id $layer_id  --top 10 --bottom 1 --ignore_const -highlight MatMul,Slice,FullyConnected,Split

    <!-- Show graph -->
    python main.py -m $model

    Linux refer: run.sh
    Windows refer: run.bat