import shutil
import os
import zipfile
import sys
import getopt
import requests
import os.path



def ignorePath(path):
    normPath = os.path.abspath(path)
    def ignoref(directory, contents):
        return [
            f for f in contents
            if os.path.abspath(os.path.join(directory, f)) == normPath]
    return ignoref


cwd: str = os.getcwd()
args: list[str] = sys.argv[1:]
options = "hb:o:"
long_options: list[str] = ["Help", "Builds=", "Output="]
arguments, values = getopt.getopt(args, options, long_options)
buildTarg = "all"
outDir: str = "build/"
version = 11.5
filePrefix = f"love-{version}-win64/"

def buildLove():
    try: 
        os.mkdir(cwd + "/" + outDir)
        
    except:
        None
    
    
    shutil.rmtree(cwd + "/" + outDir + "/temp/", True)
    print("copying the game directory")
    shutil.copytree(cwd, cwd + "/" + outDir + "/temp/", ignore=ignorePath(cwd + "/" + outDir ))
    os.remove(cwd + "/" + outDir + "/temp" + "/loved.py")

    print("zipping...")
    shutil.make_archive("game", 'zip', cwd + "/" + outDir + "/temp/", cwd + "/" + outDir)
    os.rename(cwd + "/game.zip", cwd + "/" + outDir + "/game.love")
    print("removing temp directory")
    shutil.rmtree(cwd + "/" + outDir + "/temp/", True)
    print("built game.love!")


def winBuild():
    print("downloading windows love version for bundling...")
    loveWinUrl = f"https://github.com/love2d/love/releases/download/{version}/love-{version}-win64.zip"
    response = requests.get(loveWinUrl)
    with open(cwd + "/" + outDir + "/lovewin.zip", mode="wb") as file:
        file.write(response.content)
    print("extracting windows love files...")
    winLoveZip = zipfile.ZipFile(cwd + "/" + outDir + "/lovewin.zip")
    filePrefix = f"love-{version}-win64/"
    zipfile.ZipFile.extractall(winLoveZip, cwd + "/" + outDir + "/", [f"{filePrefix}love.dll", f"{filePrefix}love.exe", f"{filePrefix}lovec.exe", f"{filePrefix}lua51.dll", f"{filePrefix}mpg123.dll", f"{filePrefix}msvcp120.dll", f"{filePrefix}msvcr120.dll", f"{filePrefix}OpenAL32.dll", f"{filePrefix}SDL2.dll"])
    os.rename(cwd + "/" + outDir + f"/love-{version}-win64/", cwd + "/" + outDir + "/winBuild/")
    with open(f"{cwd}/{outDir}/winBuild/game.exe", 'wb') as winGame:
        with open(f"{cwd}/{outDir}/winBuild/love.exe", "rb") as file:
            shutil.copyfileobj(file, winGame)
        with open(f"{cwd}/{outDir}/game.love", "rb") as file:
            shutil.copyfileobj(file, winGame)
    os.remove(f"{cwd}/{outDir}/winBuild/love.exe")


try:
    arguments, values = getopt.getopt(args, options, long_options)
    for currentArg, currentVal in arguments:
        if currentArg in ("-h", "--Help"):
            print("loved.py help menu: \nargs: \n   --Builds=<target> or -b <target>, where target is either 'all', 'win', 'mac', 'linux', or '.love' (defaults to the current OS or .love)\n  --Output=<dir> or -o <dir>, where dir is the output directory relative to the current directory (defaults to build)")
        elif currentArg in ("-b", "--Builds"):
            if currentVal == "all" or currentVal == "win" or currentVal == "mac" or currentVal == "linux" or currentVal == ".love":
                buildTarg = currentVal
        elif currentArg in ("-o", "--Output"):
            outDir = currentVal
except getopt.error as err:
    print(str(err))

shutil.rmtree(cwd + "/" + outDir + "/", True)

buildLove()



if buildTarg != ".love":
    print("fetching latest love version...")
    response = requests.get("https://github.com/love2d/love/releases/latest", allow_redirects=True)
    version = response.url[response.url.rfind('/') + 1:]
    print("latest love version is: " + version + "!")

if buildTarg == "win" or buildTarg == "all":
    winBuild()
    