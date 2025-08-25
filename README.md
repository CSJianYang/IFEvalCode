## Evaluation
1. **Infer**
```bash
MODEL_DIR="/pretrained_models/Qwen/Qwen2.5-Coder-32B-Instruct/"
INPUT_PATH="./data/benchmark/IFEvalCode.jsonl"
OUTPUT_PATH="./data/eval_results/Qwen2.5-Coder-32B-Instruct/IFEvalCode.jsonl"
TP="8"
python infer_models.py --input_path ${INPUT_PATH} --output_path ${OUTPUT_PATH} -model ${MODEL_DIR} -tensor_parallel_size ${TP}
```
2. **Evaluation**
   
```bash
INPUT_PATH="./data/eval_results/Qwen2.5-Coder-32B-Instruct/IFEvalCode.jsonl"
OUTPUT_PATH="./data/eval_results/${MODEL_NAME}"
python eval_models.py --input_path ${INPUT_PATH} --output_path   ${OUTPUT_PATH} --tmp_dir "./tmp/"
```


