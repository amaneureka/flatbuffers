#!/usr/bin/env python3
#
# Copyright 2022 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import filecmp
import glob
import platform
import shutil
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument(
    "--flatc",
    help="path of the Flat C compiler relative to the root directory")
    
args = parser.parse_args()

# Get the path where this script is located so we can invoke the script from
# any directory and have the paths work correctly.
script_path = Path(__file__).parent.resolve()

# Get the root path as an absolute path, so all derived paths are absolute.
root_path = script_path.parent.parent.absolute()

# Get the location of the flatc executable, reading from the first command line
# argument or defaulting to default names.
flatc_exe = Path(
    ("flatc" if not platform.system() == "Windows" else "flatc.exe")
    if not args.flatc
    else args.flatc
)

# Find and assert flatc compiler is present.
if root_path in flatc_exe.parents:
    flatc_exe = flatc_exe.relative_to(root_path)
flatc_path = Path(root_path, flatc_exe)
assert flatc_path.exists(), "Cannot find the flatc compiler " + str(flatc_path)

# Execute the flatc compiler with the specified parameters
def flatc(options, cwd=script_path):
    cmd = [str(flatc_path)] + options 
    result = subprocess.run(cmd, cwd=str(cwd), check=True)

def make_absolute(filename, path=script_path):
   return Path(path, filename).absolute()

def assert_file_exists(filename, path=script_path):
    file = Path(path, filename)
    assert file.exists(), "could not find file: " + filename
    return file

def assert_file_contains(file, needle):
    assert needle in open(file).read(), "coudn't find '"+needle+"' in file: "+str(file)
    return file

def assert_file_and_contents(file, needle, path=script_path):
    assert_file_contains(assert_file_exists(file, path), needle).unlink()

def run_all(module):
  methods = [func for func in dir(module) if callable(getattr(module, func)) and not func.startswith("__")]
  for method in methods:
      try:
          print(method)
          getattr(module, method)(module)
          print(" [PASSED]")
      except Exception as e:
          print(" [FAILED]: " +str(e))
