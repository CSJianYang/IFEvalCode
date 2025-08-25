npm install -g /home/data/yj411294/CodeQwen1.5/evaluation/multipl_e/chat/multiple_metrics/typescript-5.5.4.tgz
npm i --save-dev @types/node

INPUT_PATH="./data/eval_results/${MODEL_NAME}/IFEvalCode.jsonl"
OUTPUT_PATH="./data/eval_results/${MODEL_NAME}"
python eval_models.py --input_path ${INPUT_PATH} --output_path ${OUTPUT_PATH} --tmp_dir "tmp/code_execution/" --workers 32