import sys
import os
import unittest

parent_dir = os.path.dirname(os.path.realpath(__file__)) + "/../"
sys.path.append(parent_dir) # a bit of a hack, but it makes the import the same
from objects.function import Function

def get_file_path(path):
    return os.path.dirname(os.path.realpath(__file__)) + "/" + path


class TestFunctionMethods:

    def test_get_section(self):
        test_file = open(get_file_path("files/get_section.func"))
        test_text = test_file.read()
        test_file.close()
        test_results = {
            "test1": "  test1",
            "test2": "  test2",
            "test3": "  test3\n  test3",
            "test4": "  test4"
        }
        function = Function(test_text)

        for test in test_results:
            assert function._get_section(test) == test_results[test]

    def test_get_includes(self):
        test_file = open(get_file_path("files/get_includes.func"))
        test_text = test_file.read()
        test_file.close()
        test_results = [
            "test1",
            "test2",
            "test3",
            "test4",
            "test5"
        ]
        function = Function(test_text)

        assert function._get_includes() == test_results

    def test_get_name(self):
        test_file = open(get_file_path("files/get_name.func"))
        test_text = test_file.read()
        test_file.close()
        test_results = "Name"

        for line in test_text.split("\n"):
            if line != "":
                function = Function(line)
                assert function._get_name() == test_results
