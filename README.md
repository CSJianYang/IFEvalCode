# IFEvalCode
Official repository for paper "IFEvalCode: Controlled Code Generation"

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

## Citation

If you find our work helpful, feel free to give us a cite.

```
@misc{yang2025ifevalcodecontrolledcodegeneration,
      title={IFEvalCode: Controlled Code Generation}, 
      author={Jian Yang and Wei Zhang and Shukai Liu and Linzheng Chai and Yingshui Tan and Jiaheng Liu and Ge Zhang and Wangchunshu Zhou and Guanglin Niu and Zhoujun Li and Binyuan Hui and Junyang Lin},
      year={2025},
      eprint={2507.22462},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2507.22462}, 
}
```

