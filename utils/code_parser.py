from tree_sitter import Language, Parser
import tree_sitter_cpp as ts_cpp
import os

def remove_cpp_main_function(cpp_code, tree_sitter_path):
    #CPP_LANGUAGE = Language(f'{tree_sitter_path}/tree-sitter-cpp.so')
    CPP_LANGUAGE = Language(ts_cpp.language())
    parser = Parser(CPP_LANGUAGE)
    #parser.set_language(CPP_LANGUAGE)
    tree = parser.parse(bytes(cpp_code, "utf8"))
    
    # 获取根节点
    root_node = tree.root_node
    
     # 查找所有函数定义
    main_function_ranges = []
    for node in root_node.children:
        if node.type == "function_definition":
            function_name_node = node.child_by_field_name("declarator").child_by_field_name("declarator")
            if function_name_node and function_name_node.text.decode("utf-8") == "main":
                main_function_ranges.append((node.start_byte, node.end_byte))

    # 如果没有 main 函数，直接返回原代码
    if not main_function_ranges:
        return cpp_code

    # 删除 main 函数（从后往前删除，避免影响字节偏移）
    code_bytes = bytearray(cpp_code, "utf-8")
    for start, end in sorted(main_function_ranges, reverse=True):
        del code_bytes[start:end]

    return code_bytes.decode("utf-8")

if __name__ == "__main__":
    # 示例使用
    cpp_code = """
#include <iostream>

int add(int a, int b) {
    return a + b;
}

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}

void foo() {
    // do something
}
    """

    cleaned_code = remove_cpp_main_function(cpp_code, "./build/")
    print("Original code:")
    print(cpp_code)
    print("\nCode after removing main function:")
    print(cleaned_code)