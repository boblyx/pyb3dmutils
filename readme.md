# pyb3dmutils
A bunch (currently only one) of handy script utilities relating to b3dm.

## Features
- Individual & batch conversion of .b3dm into glTF 2.0 format.
- Output associated .glb, .bin and .json files (.json files contain the b3dm header under the "data" property)

## Installation
```bash
git clone https://github.com/boblyx/pyb3dmutils.git
cd pyb3dmutils
pip install -r requirements.txt
```
## Usage
### Convert a .b3dm file into a .glTF file to a specific folder
```bash
python b3dm2glTF.py -i file.b3dm -o myFolder
```

b3dm2glTF resolves output to the folder where the input file is if output path is not supplied.
### Convert a folder containing .b3dm files into another folder of .glTF files
```bash
python b3dm2glTF.py -i myFolder -o anotherFolder
```

b3dm2glTF automatically creates a new folder if an output path is not supplied.


