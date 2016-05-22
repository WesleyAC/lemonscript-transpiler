import sys
import os
import unittest

parent_dir = os.path.dirname(os.path.realpath(__file__)) + "/../"
sys.path.append(parent_dir) # a bit of a hack, but it makes the import the same
from objects.file import File

def get_file_path(path):
    return os.path.dirname(os.path.realpath(__file__)) + "/" + path


class TestFileMethods:

    def test_init(self):
        test_file = open(get_file_path("files/file/init.skel"))
        test_text = test_file.read()

        file_object = File(test_text)

        assert file_object.text == test_text
        assert file_object.init_text == test_text

    def test_init_replacements(self):
        test_file = open(get_file_path("files/file/init.skel"))
        test_text = test_file.read()

        replacements = [
            ["replace_text", "key", "value"],
            ["replace_file", "key2", get_file_path("files/file/init.inc")]
        ]
        file_object = File(test_text, replacements)

        result = test_text.replace("<<<key>>>", "value").replace("<<<key2>>>", open(get_file_path("files/file/init.inc")).read())

        assert file_object.text == result
