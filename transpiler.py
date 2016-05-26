#!/usr/bin/python
import os
import glob
import argparse

from objects.function import Function
from objects.file import File
from objects.formatter import Formatter
from objects.logger import Logger

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
        auto_classes_cpp_file.insert_text("addgenerators", File(open(get_script_dir() + "text_includes/add_to_return_vector.skel").read(), [["replace_text", "name", auto_function.get_name()], ["replace_text", "args", "-".join([argl[0] for argl in auto_function.get_args()])]]).text)

    includes = ["#include " + name for name in includes]
    auto_classes_h_file.insert_text("include", "\n".join(includes))
    auto_classes_cpp_file.replace_file("convert", get_script_dir() + "text_includes/ls_convert.inc")

    return [auto_classes_h_file.text, auto_classes_cpp_file.text]

def get_script_dir():
    return os.path.dirname(os.path.realpath(__file__)) + "/"

def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Convert Lemonscript .func files to C++ code")
    parser.add_argument("--output-dir", default="./", help="Set the directory to output the .cpp and .h files in")
    parser.add_argument("--input-dir", default="auto_functions", help="Set the directory to read the .func files from")
    parser.add_argument("--format", action="store_true", help="Run clang-format on outputted code")
    parser.add_argument("--verbose", "-v", action="count", default=0, help="Show more debug info")
    parser.add_argument("--quiet", "-q", action="count", default=0, help="Show less debug info")
    return parser.parse_args(args)

def main(arg_list=None):
    args = vars(parse_args(arg_list))
    Logger.show_log_levels += args["verbose"] - args["quiet"]
    Logger.debug("Log level: {}".format(Logger.show_log_levels))
    Logger.debug("Arguments: {}".format(args))
    auto_functions = enumerate_auto_files(args["input_dir"])
    Logger.info("Found auto functions: {}".format([func.get_name() for func in auto_functions]))
    output_path = args["output_dir"]
    if output_path[-1] != "/":
        output_path += "/"

    cpp_file = open(output_path + "auto_functions.cpp", "w")
    h_file = open(output_path + "auto_functions.h", "w")

    compiled_auto_functions = generate_auto_functions(auto_functions)

    if args["format"]:
        Logger.info("Formatting output files")
        compiled_auto_functions = [Formatter(func).get_formatted_text() for func in compiled_auto_functions]

    Logger.debug("Writing output files")
    h_file.write(compiled_auto_functions[0])
    cpp_file.write(compiled_auto_functions[1])
    cpp_file.close()
    h_file.close()
    Logger.info("Done :)")

if __name__ == "__main__":
    main()
