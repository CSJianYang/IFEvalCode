#gpt-4o-mini
MODEL_NAME="Qwen3-Coder-480B-A35B-Instruct"
INPUT_PATH="./data/benchmark/IFEvalCode.jsonl"
OUTPUT_PATH="./data/eval_results/${MODEL_NAME}/IFEvalCode.jsonl"
WORKERS=32
python infer_models.py --input_path ${INPUT_PATH} --output_path ${OUTPUT_PATH} -model ${MODEL_NAME} -workers ${WORKERS} -use_api -base_url https://xxxx -api_key sk-xxxxx

#use_local_model
MODEL_NAME="Qwen2.5-Coder-7B-Instruct"
MODEL_DIR="/pretrained_models/Qwen/${MODEL_NAME}/"
INPUT_PATH="./data/benchmark/IFEvalCode.jsonl"
OUTPUT_PATH="./data/eval_results/${MODEL_NAME}/IFEvalCode.jsonl"
TP="4"
python infer_models.py --input_path ${INPUT_PATH} --output_path ${OUTPUT_PATH} -model ${MODEL_DIR} -tensor_parallel_size ${TP}
