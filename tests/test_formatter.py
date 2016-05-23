import os
import sys
import shutil
import unittest

parent_dir = os.path.dirname(os.path.realpath(__file__)) + "/../"
sys.path.append(parent_dir) # a bit of a hack, but it makes the import the same
from objects.formatter import Formatter

class TestFormatterMethods():

    def test_get_clang_path_exists(self):
        formatter = Formatter("test")

        clang_path_suffixes = ["", "-3.7", "-3.6", "-3.5"]

        for path_suffix in clang_path_suffixes:
            try:
                shutil.rmtree("/tmp/test_root/")
            except OSError:
                pass

            os.mkdir("/tmp/test_root/")
            os.mkdir("/tmp/test_root/usr/")
            os.mkdir("/tmp/test_root/usr/bin/")
            open("/tmp/test_root/usr/bin/clang-format" + path_suffix, "w").close()

            assert formatter.get_clang_path("/tmp/test_root") == "/usr/bin/clang-format" + path_suffix

    def test_clang_path_doesnt_exist(self):
        formatter = Formatter("test")

        try:
            shutil.rmtree("/tmp/test_root/")
        except OSError:
            pass

        os.mkdir("/tmp/test_root/")
        os.mkdir("/tmp/test_root/usr/")
        os.mkdir("/tmp/test_root/usr/bin/")

        assert formatter.get_clang_path("/tmp/test_root") == None
