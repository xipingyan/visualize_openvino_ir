source ../python-env/bin/activate
model=../vit_int8_optimization/WW24_llm_2024.3.0-15670-98180edcbcc/phi-3-medium-4k-instruct/pytorch/dldt/FP16/openvino_model.xml
layer_name='__module.model.layers.0.self_attn/aten::scaled_dot_product_attention/ScaledDotProductAttention'
layer_id='289'

# python main.py -m $model -id $layer_id --top 8 --bottom 1
python main.py -m $model -name $layer_name --top 10 --bottom 1 --ignore_const
# python main.py -m $model