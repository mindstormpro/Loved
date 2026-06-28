import shutil
import os
import zipfile
import sys
import getopt

def winBuild():
    print("hello from win build!")
    try:
        shutil.rmtree(cwd + "/" + outDir)
    except:
        None
    shutil.copytree(cwd, cwd + "/" + outDir)
    os.remove(cwd + "/" + outDir + "/loved.py")

cwd: str = os.getcwd()
print(cwd)
args: list[str] = sys.argv[1:]
options = "hb:o:"
long_options: list[str] = ["Help", "Builds=", "Output="]
arguments, values = getopt.getopt(args, options, long_options)
buildTarg = None
outDir: str = "build/"

try:
    arguments, values = getopt.getopt(args, options, long_options)
    for currentArg, currentVal in arguments:
        if currentArg in ("-h", "--Help"):
            print("loved.py help menu: \nargs: \n   --Builds=<target> or -b <target>, where target is either 'all', 'win', 'mac', 'linux', or '.love' (defaults to the current OS or .love)\n  --Output=<dir> or -o <dir>, where dir is the output directory relative to the current directory (defaults to build)")
        elif currentArg in ("-b", "--Builds"):
            if currentVal == "all" or currentVal == "win" or currentVal == "mac" or currentVal == "linux":
                buildTarg = currentVal
        elif currentArg in ("-o", "--Output"):
            outdir = currentVal
except getopt.error as err:
    print(str(err))





winBuild()
    