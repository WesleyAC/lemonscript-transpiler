#lemonscript-transpiler [![Build Status](https://travis-ci.org/WesleyAC/lemonscript-transpiler.svg)](https://travis-ci.org/WesleyAC/lemonscript-transpiler) [![Coverage Status](https://coveralls.io/repos/github/WesleyAC/lemonscript-transpiler/badge.svg?branch=master)](https://coveralls.io/github/WesleyAC/lemonscript-transpiler?branch=master) ![License](https://img.shields.io/badge/license-MIT-blue.svg)

This is a script that converts .func files into a .h and .cpp file to be used with lemonscript.

##`.func` file format

`transpile.py` takes in a directory containing all the `.func` files that you want to compile, and outputs a `auto_functions.cpp` and `auto_functions.h` file to be used in the robot code. Here's an example of a valid `.func` file:

```
Wait(Time time)

include {
  "muan/utils/timing_utils.h"
}

global {
  Time start_time
}

init {
  Time start_time = muan::now();
  return false;
}

periodic {
  return (muan::now() - start_time < lemon_get("start_time"));
}
```

A few things to keep in mind:

* The first line of the file must have the name of the auto function, and all of it's arguments on it.
* You cannot have indentation before `include`, `init`, or `periodic`.
* All files to include must be on a different line in the `include` block. Commas are optional, but suggested.
* If you try to break the transpiler, you will be able to. It should handle any reasonable file, but don't try to break it.

##Supported units

Lemonscript treats all arguments as void pointers, and internally converts them to the correct units. Because of this, only the following types are supported as arguments to auto functions:

* `int`
* `bool`
* `float`
* `std::string`
* `Time`
* `Distance`
* `Length`
* `Angle`
* `Velocity`
* `Acceleration`
* `AngularVelocity`
* `Voltage`

##Arguments

`transpile.py` has two flags:

* `--input-dir` - A directory with all the `.func` files in it. Defaults to `auto_functions`.
* `--output-dir` - A directory to put the transpiled .cpp and .h files in. Defaults to the directory that the script was run from.
