#!/usr/bin/python
import os
import glob
import argparse

from objects.function import Function
from objects.file import File

def enumerate_auto_files(path):
    if not path[-1] == "/":
        path += "/"
    auto_function_files = []

    for function_file in glob.glob(os.path.join(path, "*.func")):
        auto_function_files.append(Function(open(function_file).read()))
    return auto_function_files

def generate_auto_functions_h(auto_function_objects):
    replacements = [
        ["replace_file", "warning", get_script_dir() + "text_includes/warning.inc"],
        ["replace_file", "ls_convert", get_script_dir() + "text_includes/ls_convert.inc"],
    ]
    includes = []

    for auto_function in auto_function_objects:
        for constructor in auto_function.get_constructors():
            replacement = ["insert_text", "functions", constructor + ";"]
            replacements.append(replacement)
        includes += auto_function.get_includes()

    includes = list(set(includes)) # remove duplicates
    includes = ["#include " + name for name in includes]
    replacements.append(["insert_text", "includes", "\n".join(includes)])

    return File(open(get_script_dir() + "text_includes/auto_functions.h.skel").read(), replacements).text

def generate_auto_functions_cpp(auto_function_objects):
    replacements = [["replace_file", "warning", get_script_dir() + "text_includes/warning.inc"]]

    for auto_function in auto_function_objects:
        cpp_init_code = auto_function.get_constructors()[0] + " {\n" + \
                        auto_function.get_section_code("init") + "\n" + \
                        "}\n"
        init_code_replacement = ["insert_text", "functions", cpp_init_code]

        cpp_periodic_code = auto_function.get_constructors()[1] + " {\n" + \
                            auto_function.get_section_code("periodic") + "\n" + \
                            "}\n"
        periodic_code_replacement = ["insert_text", "functions", cpp_periodic_code]

        replacements.append(init_code_replacement)
        replacements.append(periodic_code_replacement)

    return File(open(get_script_dir() + "text_includes/auto_functions.cpp.skel").read(), replacements).text

def get_script_dir():
    return os.path.dirname(os.path.realpath(__file__)) + "/"

def parse_args():
    parser = argparse.ArgumentParser(description="Convert Lemonscript .func files to C++ code")
    parser.add_argument("--output-dir", help="Set the directory to output the .cpp and .h files in")
    parser.add_argument("--input-dir", default="auto_functions", help="Set the directory to read the .func files from")
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

    cpp_file.write(generate_auto_functions_cpp(auto_functions))
    h_file.write(generate_auto_functions_h(auto_functions))
    cpp_file.close()
    h_file.close()

if __name__ == "__main__":
    main()
