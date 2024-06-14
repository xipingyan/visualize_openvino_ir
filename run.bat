
@echo off
echo "==========================="
call .\python-env\Scripts\activate.bat
echo "==========================="
set model=..\\phi3\\openvino_model.xml
set layer_name='__module.model.layers.0.self_attn/aten::scaled_dot_product_attention/ScaledDotProductAttention'
set layer_id=289
echo "==========================="
python main.py -m %model% -id %layer_id% --top 2 --bottom 1