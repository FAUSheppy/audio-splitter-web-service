#!/usr/bin/python3

import sys
import os

if not sys.argv[1]:
    print("Ussage: ./converter DIRNAME")
    sys.exit(1)

dirname = sys.argv[1]
if not os.path.isdir(dirname):
    print("Not a directory")
    sys.exit(1)

for fname in os.listdir(dirname):
    if not fname.endswith(".ogg"):
        continue
    path = os.path.join(dirname, fname)
    pathTmp = path + ".tmp"
    os.rename(path, pathTmp)
    os.system("ffmpeg -i '{}' '{}'".format(pathTmp, path))
    os.remove(pathTmp)
