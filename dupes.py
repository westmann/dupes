#!/usr/local/bin/python

import os
import sys
import hashlib

ignorelist = [".DS_Store"]

def getdirs():
    if len(sys.argv) < 2:
        return [ os.getcwd() ]
    else:
        dirs = sys.argv[1:]
        for dir in dirs:
            if not os.path.isdir(dir):
                print dir, "is not a directory"
                exit(1)
        return dirs

def sha(fileName):
    fd = open(fileName, "rb")
    content = fd.readlines()
    fd.close()
    m = hashlib.sha1()
    for eachLine in content:
        m.update(eachLine)
    return m.hexdigest()

def hashfiles(dir, filemap):
    print "hash files for", dir
    if not isinstance(filemap, dict):
        filemap = {}
    i = 0
    for root, dirs, files in os.walk(dir):
        for file in files:
            if not file in ignorelist:
               path = os.path.join(root, file)
               hash = sha(path)
               if not hash in filemap:
                   filemap[hash] = [ path ]
               else:
                   filemap[hash].append(path)
               i += 1
               if i % 80 == 0:
                   print
               else:
                   print ".",
    print
    return filemap

def printfilemap(filemap):
    for chksum, paths in filemap.items():
        if len(paths) > 1:
            printentry(chksum, paths)
            
def printentry(chksum, paths):
    prev = None
    for path in sorted(paths):
        if chksum != prev:
            indent = chksum
            prev = chksum
        else:
            indent = " " * len(chksum)
        print indent, path

filemap = None
for dir in getdirs():
    filemap = hashfiles(dir, filemap)

printfilemap(filemap)
