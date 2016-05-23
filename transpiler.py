#!/usr/bin/python
import os
import glob
import argparse

from objects.function import Function
from objects.file import File
from objects.formatter import Formatter

def enumerate_auto_files(path):
    if not path[-1] == "/":
        path += "/"
    auto_function_files = []

    for function_file in glob.glob(os.path.join(path, "*.func")):
        auto_function_files.append(Function(open(function_file).read(), get_script_dir()))
    return auto_function_files

def generate_auto_functions(auto_function_objects):
    replacements = [
        ["replace_file", "warning", get_script_dir() + "text_includes/warning.inc"]
    ]
    includes = []

    auto_classes_h_file = File(open(get_script_dir() + "text_includes/auto_classes.h.skel").read(), replacements)
    auto_classes_cpp_file = File(open(get_script_dir() + "text_includes/auto_classes.cpp.skel").read(), replacements)

    for auto_function in auto_function_objects:
        includes += auto_function.get_includes()
        auto_classes_h_file.insert_text("classes", auto_function.get_class()[0])
        auto_classes_cpp_file.insert_text("classes", auto_function.get_class()[1])
        auto_classes_h_file.insert_text("generators", auto_function.get_generator()[0])
        auto_classes_cpp_file.insert_text("generators", auto_function.get_generator()[1])

    includes = list(set(includes)) # remove duplicates
    includes = ["#include " + name for name in includes]
    auto_classes_h_file.insert_text("include", "\n".join(includes))

    return [auto_classes_h_file.text, auto_classes_cpp_file.text]

def get_script_dir():
    return os.path.dirname(os.path.realpath(__file__)) + "/"

def parse_args():
    parser = argparse.ArgumentParser(description="Convert Lemonscript .func files to C++ code")
    parser.add_argument("--output-dir", help="Set the directory to output the .cpp and .h files in")
    parser.add_argument("--input-dir", default="auto_functions", help="Set the directory to read the .func files from")
    parser.add_argument('--format', action='store_true', help="Run clang-format on outputted code")
    return parser.parse_args()

def main():
    args = vars(parse_args())
    auto_functions = enumerate_auto_files(args["input_dir"])
    if args["output_dir"] is None:
        output_path = "./"
    else:
        output_path = args["output_dir"]
    if output_path[-1] != "/":
        output_path += "/"

    cpp_file = open(output_path + "auto_functions.cpp", "w")
    h_file = open(output_path + "auto_functions.h", "w")

    compiled_auto_functions = generate_auto_functions(auto_functions)

    if args["format"]:
        compiled_auto_functions = [Formatter(func).get_formatted_text() for func in compiled_auto_functions]

    h_file.write(compiled_auto_functions[0])
    cpp_file.write(compiled_auto_functions[1])
    cpp_file.close()
    h_file.close()

if __name__ == "__main__":
    main()
