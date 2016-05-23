import subprocess
import os

class Formatter(object):
    def __init__(self, input_text, style=None): # style=None is a pretty good description of me tbh
        self.text = input_text
        if style == None:
            self.style = "{BasedOnStyle: Google, ColumnLimit: 0}"
        else:
            self.style = style

    def get_formatted_text(self, clang_path=None):
        if clang_path == None:
            clang_path = self.get_clang_path()
        if clang_path == None:
            return self.text #TODO(Wesley) warn user
        try:
            clang_process = subprocess.Popen([clang_path, "-style=" + self.style], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            return clang_process.communicate(input=bytes(self.text.encode("utf-8")))[0].decode("utf-8")
        except subprocess.CalledProcessError:
            return self.text #TODO(Wesley) warn user


    def get_clang_path(self):
        possible_paths = [
            "/usr/bin/clang-format",
            "/usr/bin/clang-format-3.7",
            "/usr/bin/clang-format-3.6",
            "/usr/bin/clang-format-3.5"
        ]

        for path in possible_paths:
            if os.path.isfile(path):
                return path

        return None
