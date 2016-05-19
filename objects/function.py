class Function(object):
    """
    Represents a .func file

    text - text passed into the constructor
    get_name() - the name of the function, as it will be used in the .auto file
    get_constructors() - a list containing 2 strings that are inserted into C++
                         source code as constructors for tne periodic and init
                         functions.
    get_args() - A list of all args. Example:
                 [["Distance", "dist"], ["Angle", "angle"]]
    get_section_code() - the literal C++ code that should be in a section
    get_section() - The text in a section
    get_includes() - A list of everything that needs to be included. Strings in
                     this list will most likely be enclosed in quotes or angle
                     brackets
    """
    def __init__(self, text):
        """
        Parses a string from a .func file into a easy to use format

        This sets self.text, then runs any functions needed to set up member
        variables by parsing self.text.
        """
        self.text = text

    def get_section(self, section_name):
        """
        Gets a "section" in self.text. Example of a section:

        name {
          ...
          stuff
          ...
        }

        That would be a section with the name "name".

        Sections that are used are "include", "init", and "periodic".
        """
        found_section = False
        text_in_section = []
        for line in self.text.split("\n"):
            if not found_section and \
               line.strip()[:len(section_name)] == section_name and \
               line.strip()[-1] == "{":
                found_section = True
            elif found_section and not line[0] == "}":
                text_in_section.append(line)
            elif found_section:
                return '\n'.join(text_in_section)
        return '' #TODO(Wesley) Better way of indicating failure

    def get_section_code(self, section):
        """
        Gets the transpiled C++ code inside a section, including auto-generated
        variable casting code.
        """
        raw_code = self.get_section(section)
        var_init_lines = []

        cast_functions = {
            "int":                 "ConvertArgs::ls_convert_int({})",
            "bool":                "ConvertArgs::ls_convert_bool({})",
            "float":               "ConvertArgs::ls_convert_float({})",
            "string":              "{}",
            "std::string":         "{}",
            "Time":                "ConvertArgs::ls_convert_time({})",
            "Distance":            "ConvertArgs::ls_convert_distance({})",
            "Length":              "ConvertArgs::ls_convert_distance({})",
            "Angle":               "ConvertArgs::ls_convert_angle({})",
            "Velocity":            "ConvertArgs::ls_convert_velocity({})",
            "Acceleration":        "ConvertArgs::ls_convert_acceleration({})",
            "AngularVelocity":     "ConvertArgs::ls_convert_angularvelocity({})",
            "Voltage":             "ConvertArgs::ls_convert_voltage({})"
        }

        argnum = 0

        if len(self.get_args()) > 0:
            for arg in self.get_args():
                var_cast_func = cast_functions[arg[0]].format("ls_arg_list[{}]".format(argnum))
                var_init_line = "  {arg[0]} {arg[1]} = {cast};".format(arg=arg, cast=var_cast_func)
                var_init_lines.append(var_init_line)
                argnum += 1

        return ("  // BEGIN AUTO GENERATED CODE\n" +
                "\n".join(var_init_lines) +
                "\n  // END AUTO GENERATED CODE\n\n" +
                raw_code)

    def get_includes(self):
        """
        Returns a list of all of the lines in the "include" section of self.text,
        stripping trailing commas if needed.
        """
        includes = []
        for line in self.get_section("include").split("\n"):
            if line:
                include_text = line.strip()
                if include_text[-1] == ",":
                    include_text = include_text[:-1]
                includes += [include_text]
        return includes

    def get_args(self):
        """
        Returns a list of arguments. For an example of the format, see the
        class docstring.
        """
        try:
            arg_string = self.get_raw_constructor().split("(")[1].split(")")[0]
        except IndexError:
            arg_string = ""
        args = []
        if arg_string.strip() != "":
            for arg in arg_string.split(","):
                arg = arg.strip()
                arg_pair = [arg.strip().split(" ")[0], arg.strip().split(" ")[-1]]
                args.append(arg_pair)
        return args

    def get_raw_constructor(self):
        """
        Returns the first line of self.text, which we assume to be the
        lemonscript-style constructor. This is not valid C++ code.
        """
        return self.text.split("\n")[0]

    def get_constructors(self):
        """
        Returns the valid C++ constructors for the init and periodic functions.
        """
        prefix = "bool AutoFunction::"
        arg_list = "(CitrusRobot* robot, std::vector<void *> ls_arg_list)"
        init_constructor = (prefix + self.get_name() + "Init" + arg_list)
        periodic_constructor = (prefix + self.get_name() + "Periodic" + arg_list)
        return [init_constructor, periodic_constructor]

    def get_name(self):
        """
        Returns the name of the function, as it will be used in lemonscript.
        """
        return self.get_raw_constructor().split("(")[0].strip()
