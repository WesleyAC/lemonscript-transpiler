class File(object):
    """
    This class represents a file that can have parts of it replaced with text
    or another file.

    "Tags" in the file are represented by strings enclosed in pairs of 3 angle
    brackets. For example:

    file.txt:
    ---
    My favorite animal is <<<animal>>>.

    <<<this is a tag>>>

    This text will be kept as-is.
    ---

    Calling replace_text("animal", "octocat") will cause the string
    "<<<animal>>>" to be replaced with the string "octocat"
    """
    def __init__(self, text, replacements=None):
        """
        Creates a File object from a string representing the contents of a file,
        and, optionally, a list of replacements to be done on the file.

        Replacements are in the form that is taken be File.replace()
        """
        self.init_text = text
        self.text = self.init_text
        if replacements is not None:
            self.replace(replacements)

    def replace(self, replacements):
        """
        Take a list of multiple replacements, and perform all of them. If you
        just want to do one replacement, do not use this function!

        The list of replacements is in the format of:

        [
            ["function_name", "key", "replacement/file"],
            ...
        ]

        Where function_name is the name of any text replacement function
        (currently "replace_text", "replace_file", "insert_text", or
        "insert_file"), "key" is the tag to be replaced (without the enclosing
        angle brackets, and "replacement/file" is the text or filename that the
        tag will be replaced with.
        """
        actions = {
            "replace_text": self.replace_text,
            "replace_file": self.replace_file,
            "insert_text":  self.insert_text,
            "insert_file": self.insert_file
        }
        for replacement in replacements:
            actions[replacement[0]](replacement[1], replacement[2])

    def replace_text(self, key, text):
        """
        Replace a tag with a string

        key is the tag to be replaced, without the enclosing angle brackets
        text is the string to replace it with
        """
        replace_text = "<<<{}>>>".format(key)
        self.text = self.text.replace(replace_text, text)

    def replace_file(self, key, file_name):
        """
        Replace a tag with the contents of a file

        key is the tag to be replaced, without the enclosing angle brackets
        file_name is name of the file that it will be replaced with
        """
        self.replace_text(key, open(file_name).read())

    def insert_text(self, key, text):
        """
        Insert text directly after a tag

        This assumes that the tag is the last thing on a line. For example:

        good:
        //<<<tag>>>

        bad:
        /*
        stuff
        <<<tag>>>*/

        key is the tag to be replaced, without the enclosing angle brackets
        text is the string that will be inserted
        """
        replace_text = "<<<{}>>>".format(key)
        insert_at = self.text.find(replace_text) + len(replace_text) + 1 # Next line
        self.text = self.text[:insert_at] + text + "\n" + self.text[insert_at:]

    def insert_file(self, key, file_name):
        """
        Insert a file directly after a tag

        This assumes that the tag is the last thing on a line. For example:

        good:
        //<<<tag>>>

        bad:
        /*
        stuff
        <<<tag>>>*/

        key is the tag to be replaced, without the enclosing angle brackets
        file_name is the name of the file that it will be replaced with
        """
        self.insert_text(key, open(file_name).read())
