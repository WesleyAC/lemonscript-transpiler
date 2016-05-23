import os
import unittest

import transpiler

class TestTranspiler:

    def test_transpiler_creates_files_without_format(self):
        try:
            os.remove("/tmp/auto_functions.cpp")
            os.remove("/tmp/auto_functions.h")
        except FileNotFoundError:
            pass

        transpiler.main(["--output-dir", "/tmp"])

        assert os.path.isfile("/tmp/auto_functions.cpp")
        assert os.path.isfile("/tmp/auto_functions.h")

    def test_transpiler_creates_files_with_format(self):
        try:
            os.remove("/tmp/auto_functions.cpp")
            os.remove("/tmp/auto_functions.h")
        except FileNotFoundError:
            pass

        transpiler.main(["--format", "--output-dir", "/tmp"])

        assert os.path.isfile("/tmp/auto_functions.cpp")
        assert os.path.isfile("/tmp/auto_functions.h")
