source ../python-env/bin/activate
model=../vit_int8_optimization/WW24_llm_2024.3.0-15670-98180edcbcc/phi-3-medium-4k-instruct/pytorch/dldt/FP16/openvino_model.xml
python main.py -m $model -layer "" --top 10 --bottom 1