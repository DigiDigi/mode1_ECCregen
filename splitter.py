#!/usr/bin/env python2.7

# Script for splitting out data from mode 1 2352 data tracks.
# Input files: (source.iso)
# Output files: (split.bin, headers.txt)
#
# -Outline-
# Reads each byte from the source file into a list.
# When it has taken 16 bytes, checks if the first 12 bytes is a sync pattern.
# If so:
#     Write byte index the pattern begins on to headers.txt. Write space and header bytes. Write newline.
#     Read next 2048 characters from source, write to split.bin.
#     Read and skip the next 288 bytes.
#
# -Note-
# Extremely slow.

import argparse
parser = argparse.ArgumentParser(description='Splits data out of iso mode-1 2352 data tracks.')
parser.add_argument('source', nargs='?', help='Input binary data. (Default: source.iso)')
parser.add_argument('split', nargs='?', help='Output binary data. (Default: split.bin)')
parser.add_argument('headers', nargs='?', help='Sync location, Header (Default: headers.txt)')
args = parser.parse_args()

filename1 = 'source.iso'
filename2 = 'split.bin'
filename3 = 'headers.txt'
if args.source:
    filename1 = args.source
if args.split:
    filename2 = args.split
if args.headers:
    filename3 = args.headers

sourcefile = open(filename1, 'rb')
splitfile = open(filename2, 'wb')
headerfile = open(filename3, 'w')

byteindex = [0]
lastbyte = [None]
bytelist = []
syncpattern = [0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00]


def readbyte(num=1):
    for n in xrange(num):
        newbyte = sourcefile.read(1)
        bytelist.append(newbyte)
        lastbyte[0] = newbyte
        byteindex[0] += 1


def clearlist(lst, num, ind=0):
    for n in xrange(num):
        lst.pop(ind)


readbyte()

counter = 0
while lastbyte[0]:  # Read bytes until no byte is read.
    counter += 1
    if len(bytelist) == 16:
        ordlist = []
        for byte in bytelist:
            ordlist.append(ord(byte))
        if ordlist[:12] == syncpattern:
            headerfile.write(str(byteindex[0]-16) + ' ')

            header = str((256**3 * ordlist[-4]) + (256 ** 2 * ordlist[-3]) + (256 * ordlist[-2]) + ordlist[-1])

            print byteindex[0]-16, ' ', header

            headerfile.write(header + '\n')

            clearlist(bytelist, 16)
            readbyte(2048)
            for b in bytelist:
                splitfile.write(b)
            readbyte(288)
            clearlist(bytelist, 2336)

        else:
            # Remove the bytes from the list.
            clearlist(bytelist, 16)
    readbyte()
    if counter % 10000000 == 0:
        print 'Reading..'

print 'Done.'
sourcefile.close()
splitfile.close()
headerfile.close()
