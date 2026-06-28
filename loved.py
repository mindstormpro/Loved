import shutil
import os
import zipfile
import sys
import getopt

import os.path
def ignorePath(path):
    normPath = os.path.abspath(path)
    def ignoref(directory, contents):
        return [
            f for f in contents
            if os.path.abspath(os.path.join(directory, f)) == normPath]
    return ignoref


cwd: str = os.getcwd()
print(cwd)
args: list[str] = sys.argv[1:]
options = "hb:o:"
long_options: list[str] = ["Help", "Builds=", "Output="]
arguments, values = getopt.getopt(args, options, long_options)
buildTarg = None
outDir: str = "build/"

def buildLove():
    try: 
        os.mkdir(cwd + "/" + outDir)
        
    except:
        None
    
    
    shutil.rmtree(cwd + "/" + outDir + "/temp/", True)
    print(cwd + "/" + outDir)
    shutil.copytree(cwd, cwd + "/" + outDir + "/temp/", ignore=ignorePath(cwd + "/" + outDir ))
    
    os.remove(cwd + "/" + outDir + "/temp" + "/loved.py")
    shutil.make_archive("game", 'zip', cwd + "/" + outDir + "/temp/", cwd + "/" + outDir)
    os.rename(cwd + "/game.zip", cwd + "/" + outDir + "/game.love")
    shutil.rmtree(cwd + "/" + outDir + "/temp/", True)
def winBuild():
    print("hello from win build!")
    


try:
    arguments, values = getopt.getopt(args, options, long_options)
    for currentArg, currentVal in arguments:
        if currentArg in ("-h", "--Help"):
            print("loved.py help menu: \nargs: \n   --Builds=<target> or -b <target>, where target is either 'all', 'win', 'mac', 'linux', or '.love' (defaults to the current OS or .love)\n  --Output=<dir> or -o <dir>, where dir is the output directory relative to the current directory (defaults to build)")
        elif currentArg in ("-b", "--Builds"):
            if currentVal == "all" or currentVal == "win" or currentVal == "mac" or currentVal == "linux":
                buildTarg = currentVal
        elif currentArg in ("-o", "--Output"):
            outDir = currentVal
except getopt.error as err:
    print(str(err))


buildLove()


winBuild()
    