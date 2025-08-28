MODEL_NAME="Qwen3-Coder-480B-A35B-Instruct"
INPUT_PATH="./data/eval_results/${MODEL_NAME}/IFEvalCode.jsonl"
OUTPUT_PATH="./data/eval_results/${MODEL_NAME}"
python eval_models.py --input_path ${INPUT_PATH} --output_path ${OUTPUT_PATH} --tmp_dir "tmp/code_execution/" --workers 16