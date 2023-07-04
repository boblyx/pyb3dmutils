###########################
## b3dm2GLTF             ##
## by Bob Lee YX         ##
###########################

import os
import mmap
import shutil
import pathlib
import argparse
import json
from pygltflib import GLTF2

def convertFile(filePath, outPath=None):
    """Converts a b3dm file by removing the b3dm header and truncating it into a new glb file. This glb file is then converted into glTF.
    Parameters
    ----------
    filePath: <string> a string of the file to be converted.
    outputPath: <string> a string of the output path where the converted gltf will be output
    """
    input = pathlib.Path(filePath)
    folder = input.parent
    if (not input.suffix == ".b3dm"):
        return 0
    filename = pathlib.Path(filePath).name
    if(outPath == None):
        outPath = folder
    input_copy = os.path.join(outPath, filename + ".glb")
    header_file = os.path.join(outPath, filename + ".json")
    shutil.copyfile(input, input_copy)
    header_glTF = b"glTF"
    # Truncate the b3dm header up until the start of the glTF header
    with open(input_copy, "r+") as f:
        with mmap.mmap(f.fileno(), 0, access = mmap.ACCESS_WRITE) as m:
            m.seek(0)
            # find the first bracket
            bLocStart = m.find(b"{")
            gLoc = m.find(header_glTF)
            bLocEnd = gLoc
            orig_file = m.read()
            header_txt = orig_file[bLocStart:bLocEnd]
            new_file = orig_file[int(gLoc):]
            m.resize(len(new_file))
            m[:] = new_file
            m.flush()
            pass
        pass
    # Save b3dm header data into a .json file
    with open(header_file, "wb") as f:
        f.write(b'{"data":[')
        f.write(header_txt.replace(b'}',b'},',1))
        f.write(b"]}")
        pass
    # Write b3dm header into the _extra attribute in the mesh primitive
    extra_data = {}
    with open(header_file, "r") as f:
        extra_data = json.load(f)
        pass
    glb = GLTF2().load(input_copy)
    #glb.meshes[0].extras = "test"
    outputFilePath = os.path.join(outPath,filename + ".gltf")
    glb.save(outputFilePath)
    print("Successfully saved to %s" % outputFilePath)

def convertFolder(folderPath, outPath=None):
    """Converts all b3dm files in a given folder by calling convertFile()
    Parameters
    ----------
    folderPath: <string> a string of the folder path within which all files are to be converted non recursively.
    outputPath: <string> a string of the output path where converted gltfs will be output
    """
    folder = pathlib.Path(folderPath)
    folderParent = folder.parent
    folderName = folder.name
    newFolder = ""
    if(outPath == None):
        newFolder = os.path.join(folderParent, folderName+"_GLTF")
    else:
        newFolder = outPath
    if(not os.path.exists(newFolder)):
        os.mkdir(newFolder)
        pass
    files = os.listdir(folderPath)
    for file in files:
        fullPath = os.path.join(folderPath, file)
        print("Converting %s ..." % fullPath)
        convertFile(fullPath, newFolder)
        pass
    pass

parser = argparse.ArgumentParser()
parser.add_argument('-i','--input', help="Input file or folder name")
parser.add_argument('-o', '--output', help="Output file or folder name")
args = parser.parse_args()
argDict = vars(args)

# Check if input path is a file or folder
if(not os.path.exists(argDict["input"])):
    print("Invalid input path supplied. Please try again.")
    exit()
if(os.path.isfile(argDict["input"])):
    print("Converting %s...!" % argDict["input"])
    convertFile(argDict["input"])
    pass
else:
    print("Converting all .b3dm files in %s" % argDict["input"])
    convertFolder(argDict["input"])


