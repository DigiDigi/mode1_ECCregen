#!/usr/bin/env python2.7

# Create a patch file out of original and modified split binaries.
# split.bin, modified.bin -> create_patch.py -> patchfile.txt
# The patch file is a series of lines: ByteIndex ChangedBytes

import argparse
parser = argparse.ArgumentParser(description='Create a new patched binary.')
parser.add_argument('original', nargs='?', help='Original split data. (Default: split.bin)')
parser.add_argument('modified', nargs='?', help='Modified split data. (Default: modified.bin)')
parser.add_argument('patch', nargs='?', help='Output patch file. (Default: patchfile.txt)')
args = parser.parse_args()

filename1 = 'split.bin'
filename2 = 'modified.bin'
filename3 = 'patchfile.txt'
if args.original:
    filename1 = args.original
if args.modified:
    filename2 = args.modified
if args.patch:
    filename3 = args.patch

originalfile = open(filename1, 'rb')
modifiedfile = open(filename2, 'rb')
patchfile = open(filename3, 'w')

global originalbyte
global pf_string
global pf_flag
global pf_byteindex
originalbyte = '.'
pf_string = ''
pf_flag = False
pf_byteindex = 0


while originalbyte:
    originalbyte = originalfile.read(1)
    modifiedbyte = modifiedfile.read(1)
    if originalbyte != modifiedbyte:
        pf_string = pf_string + modifiedbyte
        pf_flag = True
    else:
        if pf_flag:
            patchfile.write(str(pf_byteindex) + ' ')
            for eachbyte in pf_string:
                patchfile.write(hex(ord(eachbyte))[2:])
            patchfile.write('\n')

            pf_flag = False
            pf_string = ''
    pf_byteindex += 1
if pf_flag:
    patchfile.write(str(pf_byteindex) + ' ' + pf_string + '\n')


originalfile.close()
modifiedfile.close()
patchfile.close()
