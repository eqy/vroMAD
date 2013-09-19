from cx_Freeze import setup, Executable
import os

#There's no documentation on how to do this zip-include stuff, just posts by SO Gods
CONST_SC2READER_PATH = 'C:\Python33\Lib\site-packages\sc2reader\data\\'
CONST_ROOT = 'C:\Python33\Lib\site-packages\\'

includefiles = list()
for dirpath, dirnames, filenames in os.walk(CONST_SC2READER_PATH):
    for filename in filenames:
        includefiles.append([dirpath+'\\'+filename, os.path.relpath(dirpath+'\\'+filename,CONST_ROOT)])
        print(includefiles[-1])


setup(
     name = "vroMAD",
     version = "0.1.0",
     options = {'build_exe': {'zip_includes':includefiles}},
     executables = [Executable("__main__.py", base = "WIN32GUI")])
