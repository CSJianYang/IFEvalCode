import argparse
from utils import utils, code_execute_multiple, code_parser
import os
import re
import collections
import tqdm
import jsonlines
import json
import numpy as np
import collections
def python_post_process_func(response, check_correctness, tree_sitter_path):
    code_group = re.search(r"```.*?\n(.*?)```", response, flags = re.DOTALL)
    if code_group is not None:
        code = code_group.group(1)
    else:
        code = response
    check_correctness = check_correctness.encode('utf-8').decode('unicode_escape')
    code_string = code + "\n" + check_correctness + "\n" + "check_correctness()"
    return code_string
    

def cpp_post_process_func(response, check_correctness, tree_sitter_path):
    code_group = re.search(r"```.*?\n(.*?)```", response, flags = re.DOTALL)
    if code_group is not None:
        code = code_group.group(1)
    else:
        code = response

    code = code_parser.remove_cpp_main_function(code, tree_sitter_path = tree_sitter_path)

    # code = re.sub(r"int main\(\) \{\s*([\s\S]*?)\s*return\s+0;\s*\}\n", "", code, flags = re.DOTALL)
    check_correctness_suffix = """
int main() {
    check_correctness();
    return 0;
}
"""
    check_correctness = check_correctness.encode('utf-8').decode('unicode_escape')
    code_string = code + "\n" + "\n#include <iostream>\nusing namespace std;\n" + check_correctness + "\n" + check_correctness_suffix
    return code_string

def csharp_post_process_func(response, check_correctness, tree_sitter_path):
    code_group = re.search(r"```.*?\n(.*?)```", response, flags = re.DOTALL)
    if code_group is not None:
        code = code_group.group(1)
    else:
        code = response
    check_correctness = check_correctness.replace("public class CheckCorrectness\n{\n", """public class CheckCorrectness
{
    public static bool return_value;
    public static void Main(string[] args) {
        return_value = check_correctness();
        if (!return_value) {
            throw new Exception("check_correctness()");
        }
    }

""")
    check_correctness = check_correctness.encode('utf-8').decode('unicode_escape')
    code_string = code + "\n" + check_correctness + "\n"
    return code_string


def java_post_process_func(response, check_correctness, tree_sitter_path):
    code_group = re.search(r"```.*?\n(.*?)```", response, flags = re.DOTALL)
    if code_group is not None:
        code = code_group.group(1)
    else:
        code = response
    # static method signature
    if "Solution." in check_correctness:
        code = code.replace("public class Solution {", """public class Problem {
    public static void main(String[] args) {
        TestCases.checkCorrectness();
    }
""")
        check_correctness = check_correctness.replace("Solution.", "Problem.")
        check_correctness = check_correctness.encode('utf-8').decode('unicode_escape')
        code_string = code + "\n\n\n" + check_correctness
    # class signature
    else:
        code = code.replace("public class", "class")
        check_correctness_suffix = """public class Problem {
    public static void main(String[] args) {
        TestCases.checkCorrectness();
    }
}
"""
        check_correctness = check_correctness.encode('utf-8').decode('unicode_escape')
        code_string = code + "\n\n\n" + check_correctness + "\n" + check_correctness_suffix
    return code_string

def javascript_post_process_func(response, check_correctness, tree_sitter_path):
    code_group = re.search(r"```.*?\n(.*?)```", response, flags = re.DOTALL)
    if code_group is not None:
        code = code_group.group(1)
    else:
        code = response
    code_string = code + "\n" + check_correctness + "\n" + "check_correctness()"
    return code_string

def typescript_post_process_func(response, check_correctness, tree_sitter_path):
    code_group = re.search(r"```.*?\n(.*?)```", response, flags = re.DOTALL)
    if code_group is not None:
        code = code_group.group(1)
    else:
        code = response
    code_string = code + "\n" + check_correctness + "\n" + "check_correctness()"
    return code_string
    
def php_post_process_func(response, check_correctness, tree_sitter_path):
    code_group = re.search(r"```.*?\n(.*?)```", response, flags=re.DOTALL)
    if code_group is not None:
        code = code_group.group(1)
    else:
        code = response
    if "<?php" in code:
        code = code.replace("<?php", "")
    if "?>" in code:
        code = code.replace("?>", "")
    code_string = "<?php\n" + code + "\n" + check_correctness + "\n" + "check_correctness();\n\n\n?>"
    return code_string

def shell_post_process_func(response, check_correctness, tree_sitter_path):
    code_group = re.search(r"```.*?\n(.*?)```", response, flags=re.DOTALL)
    if code_group is not None:
        code = code_group.group(1)
    else:
        code = response
    code_string = "#!/bin/bash\n" + code + "\n" + check_correctness + "\n" + "check_correctness\n\n\n"
    return code_string

    
def eval_correctness_and_instrction(response, check_correctness_func, check_instruction_func, programming_language, post_process_func, tmp_dir, tree_sitter_path):
    if_correct_code_string = post_process_func(response, check_correctness_func, tree_sitter_path)
    #try:
    if_correct, if_correct_logs = code_execute_multiple.check_correctness_multiple(if_correct_code_string, programming_language, tmp_dir = tmp_dir)
    #except:
    #    if_correct, if_correct_logs = 0, None
    if_instruction_code_string = f"response = {repr(response)}" + "\n" + f"{check_instruction_func}" + "\n" + "check_instruction(response)"
    #try:
    if_instruction, if_instruction_logs = code_execute_multiple.check_correctness_multiple(if_instruction_code_string, programming_language = "python", tmp_dir = tmp_dir)
    #except:
    #    if_instruction, if_instruction_logs = 0, None
    return if_correct, if_instruction,if_correct_logs, if_instruction_logs


def check_correctness_worker(args):
    objs, worker_id, workers, args = args
    tmp_dir = args["tmp_dir"]
    tree_sitter_path = args["tree_sitter_path"]
    post_process_funcs = {
        "python": python_post_process_func,
        "cpp": cpp_post_process_func,
        "java": java_post_process_func,
        "csharp": csharp_post_process_func,
        "typescript": typescript_post_process_func,
        "javascript": javascript_post_process_func,
        "php": php_post_process_func,
        "shell": shell_post_process_func,
    }
    for obj in tqdm.tqdm(objs, desc=f"job id: {worker_id}| {workers} workers"): 
        en_response = obj["english_response"] if "english_response" in obj else ""
        programming_language = obj["programming_language"]
        check_correctness_func = obj["check_correctness"]
        check_instruction_func = obj["check_instruction"]
        en_if_correct, en_if_instruction, en_if_correct_logs, en_if_instruction_logs = eval_correctness_and_instrction(
            en_response, 
            check_correctness_func = check_correctness_func, 
            check_instruction_func = check_instruction_func, 
            programming_language = programming_language, 
            post_process_func = post_process_funcs[programming_language],
            tmp_dir = tmp_dir,
            tree_sitter_path = tree_sitter_path
        )
        #
        zh_response = obj["chinese_response"] if "chinese_response" in obj else "" # if "chinese_response" in obj else obj["claude-3-7-sonnet-20250219_chinese_response"]
        zh_if_correct, zh_if_instruction, zh_if_correct_logs, zh_if_instruction_logs = eval_correctness_and_instrction(
            zh_response,
            check_correctness_func = check_correctness_func, 
            check_instruction_func = check_instruction_func, 
            programming_language = programming_language, 
            post_process_func = post_process_funcs[programming_language],
            tmp_dir = tmp_dir,
            tree_sitter_path = tree_sitter_path
        )
        obj["eval_results"] = {
            "en": {
                "if_correct": en_if_correct, 
                "if_instruction": en_if_instruction,
                "if_correct_logs": en_if_correct_logs, 
                "if_instruction_logs": en_if_instruction_logs
            },
            "zh": {
                "if_correct": zh_if_correct, 
                "if_instruction": zh_if_instruction,
                "if_correct_logs": zh_if_correct_logs, 
                "if_instruction_logs": zh_if_instruction_logs
            }
        }
    return objs


def statistic_results(output_objs):
    zh_if_correct = np.average([obj["eval_results"]["zh"]["if_correct"] for obj in output_objs])
    zh_if_instruction = np.average([obj["eval_results"]["zh"]["if_instruction"] for obj in output_objs])
    en_if_correct = np.average([obj["eval_results"]["en"]["if_correct"] for obj in output_objs])
    en_if_instruction = np.average([obj["eval_results"]["en"]["if_instruction"] for obj in output_objs])
    #print(f"zh_if_correct: {zh_if_correct} ({len([obj for obj in output_objs if obj['eval_results']['zh']['if_correct'] == 1])}/{len(output_objs)}), zh_if_instruction: {zh_if_instruction} ({len([obj for obj in output_objs if obj['eval_results']['zh']['if_instruction'] == 1])}/{len(output_objs)}), en_if_correct: {en_if_correct} ({len([obj for obj in output_objs if obj['eval_results']['en']['if_correct'] == 1])}/{len(output_objs)}), en_if_instruction: {en_if_instruction} ({len([obj for obj in output_objs if obj['eval_results']['en']['if_instruction'] == 1])}/{len(output_objs)})")
    result = {
        "zh_if_correct": round(zh_if_correct * 100, 1), 
        "zh_if_instruction": round(zh_if_instruction * 100, 1), 
        "en_if_correct": round(en_if_correct * 100, 1), 
        "en_if_instruction": round(en_if_instruction * 100 , 1)
    }
    return result


def statistic_results_by_programming_languages(output_objs):
    lgs = collections.defaultdict(list)
    avg_results = statistic_results(output_objs)
    for obj in output_objs:
        lgs[obj["programming_language"]].append(obj)
    results = {}
    results["all"] = avg_results
    for lg in lgs:
        results[lg] = statistic_results(lgs[lg])
    return results


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", "-input_path", type=str, default="data/dataset/eval_results/debug/IFEvalCode.jsonl")
    parser.add_argument("--output_path", "-output_path", type=str, default="data/tmp/")
    parser.add_argument("--tmp_dir", "-tmp_dir", type=str, default="tmp/ifeval_code/tmp")
    parser.add_argument("--tree_sitter_path", "-tree_sitter_path", type=str, default="build/")
    parser.add_argument("--workers", "-workers", type=int, default=1)
    args = parser.parse_args()
    return args


def remove_thinking_content(objs):
    print("Removing <think>\\n...\\n</think> in response!")
    data = []
    for obj in objs:
        if "response" in obj and obj["response"] is not None:
            obj["response"] = re.sub(r"<think>.*?</think>", "", obj["response"], flags = re.DOTALL)
    print(f"{len(objs)} -> {len(data)}")
    return objs


def main():
    args = parse_args()
    print(args)
    objs = utils.read_jsonl_file(args.input_path)
    objs = remove_thinking_content(objs)
    os.makedirs(args.tmp_dir, exist_ok = True)
    input_args = {
        "tmp_dir": args.tmp_dir,
        "tree_sitter_path": args.tree_sitter_path
    }
    output_objs = utils.multi_tasks_from_objs(objs, workers = args.workers, task = check_correctness_worker, args = input_args)
    utils.write_jsonl_file(output_objs, f"{args.output_path}/eval_results.log.jsonl")
    results = statistic_results_by_programming_languages(output_objs)
    results["model"] = output_objs[0]["model_name"] if "model_name" in output_objs[0] else None
    zh_results = []
    en_results = []
    lgs = [
        "python", 
        "java", 
        "cpp", 
        "csharp", 
        "typescript", 
        "javascript", 
        "php", 
        "shell", 
        "all"
        ]
    for lg in lgs:
        zh_results.append(str(results[lg]["zh_if_correct"]))
        zh_results.append(str(results[lg]["zh_if_instruction"]))
        en_results.append(str(results[lg]["en_if_correct"]))
        en_results.append(str(results[lg]["en_if_instruction"]))
    zh_latex_str = " & ".join(zh_results)
    en_latex_str = " & ".join(en_results)
    results["zh_latex_str"] = zh_latex_str
    results["en_latex_str"] = en_latex_str
    utils.save_json(results, f"{args.output_path}/eval_results.json")


if __name__ == "__main__":
    main()