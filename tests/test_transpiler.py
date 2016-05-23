import os
import subprocess
import unittest

import transpiler

class TestTranspiler:

    def clean_auto_funcs(self):
        try:
            os.remove("/tmp/auto_functions.cpp")
            os.remove("/tmp/auto_functions.h")
            os.remove("auto_functions.cpp")
            os.remove("auto_functions.h")
        except OSError:
            pass


    def test_transpiler_creates_files_without_format(self):
        self.clean_auto_funcs()

        transpiler.main(["--output-dir", "/tmp"])

        assert os.path.isfile("/tmp/auto_functions.cpp")
        assert os.path.isfile("/tmp/auto_functions.h")

    def test_transpiler_creates_files_with_format(self):
        self.clean_auto_funcs()

        transpiler.main(["--format", "--output-dir", "/tmp"])

        assert os.path.isfile("/tmp/auto_functions.cpp")
        assert os.path.isfile("/tmp/auto_functions.h")

    def test_transpiler_uses_input_files(self):
        self.clean_auto_funcs()

        transpiler.main(["--format", "--output-dir", "/tmp", "--input-dir", "tests/files/transpiler/auto_functions"])

        assert os.path.isfile("/tmp/auto_functions.cpp")
        assert os.path.isfile("/tmp/auto_functions.h")
        assert "Wait" in open("/tmp/auto_functions.h").read()
        assert "Wait" in open("/tmp/auto_functions.cpp").read()

    def test_transpiler_works_from_other_dir(self):
        self.clean_auto_funcs()

        old_dir = os.getcwd()
        os.chdir("/tmp")

        transpiler.main(["--format", "--input-dir", old_dir + "/tests/files/transpiler/auto_functions"])

        assert os.path.isfile("/tmp/auto_functions.cpp")
        assert os.path.isfile("/tmp/auto_functions.h")
        assert "Wait" in open("/tmp/auto_functions.h").read()
        assert "Wait" in open("/tmp/auto_functions.cpp").read()

        os.chdir(old_dir)

    def test_transpiler_code_compiles(self):
        self.clean_auto_funcs()

        transpiler.main(["--format", "--input-dir", "tests/files/transpiler/auto_functions_compile"])

        subprocess.check_call(["g++", "-o", "/dev/null", "--std=c++11", "auto_functions.cpp"])

    def test_run_transpiler_as_process(self):
        self.clean_auto_funcs()

        subprocess.check_call(["./transpiler.py", "--format", "--input-dir", "tests/files/transpiler/auto_functions", "--output-dir", "/tmp"])

        assert os.path.isfile("/tmp/auto_functions.cpp")
        assert os.path.isfile("/tmp/auto_functions.h")
        assert "Wait" in open("/tmp/auto_functions.h").read()
        assert "Wait" in open("/tmp/auto_functions.cpp").read()
