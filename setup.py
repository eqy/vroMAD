import sys

from cx_Freeze import setup, Executable

build_exe_options = {"include_files": ['C:\Python33\Lib\site-packages\sc2reader\data\ ']}

setup(
    name = "vroMAD",
    version = "0.1.0",
    executables = [Executable("__main__.py", base = "WIN32GUI")])
