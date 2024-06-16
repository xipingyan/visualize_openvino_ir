
@echo off
call .\python-env\Scripts\activate.bat

set model=..\\phi3\\openvino_model.xml
set layer_name='__module.model.layers.0.self_attn/aten::scaled_dot_product_attention/ScaledDotProductAttention'
set layer_id=289

@REM python main.py -m %model% -id %layer_id% --top 10 --bottom 1 --ignore_const -highlight MatMul,Slice

set model=..\\phi3\\xxx_0.xml
set layer_id=208
python main.py -m %model% -id %layer_id% --top 10 --bottom 1 --ignore_const -highlight MatMul,Slice,FullyConnected,Split