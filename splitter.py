#!/usr/bin/env python2.7

# Script for splitting out data from mode 1 2352 data tracks.
# Input files: (source.iso)
# Output files: (split.bin, sync.txt)
#
# -Outline-
# Reads chunks of 16 bytes and checks if the first 12 bytes are a sync pattern.
# If so:
#     Write byte index the sync pattern begins on to sync.txt. Write newline.
#     Read next 2048 characters from source, write to split.bin.
#     Read and skip the next 288 bytes.
#

import argparse
parser = argparse.ArgumentParser(description='Splits data out of iso mode-1 2352 data tracks.')
parser.add_argument('source', nargs='?', help='Input binary data. (Default: source.iso)')
parser.add_argument('split', nargs='?', help='Output binary data. (Default: split.bin)')
parser.add_argument('sync', nargs='?', help='Sync locations. (Default: sync.txt)')
args = parser.parse_args()

filename1 = 'source.iso'
filename2 = 'split.bin'
filename3 = 'sync.txt'
if args.source:
    filename1 = args.source
if args.split:
    filename2 = args.split
if args.sync:
    filename3 = args.sync

sourcefile = open(filename1, 'rb')
splitfile = open(filename2, 'wb')
syncfile = open(filename3, 'w')

byteindex = [0]
lastbytes = ['Bytes']
syncpattern_list = [0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00]
syncpattern = ''
for i in xrange(len(syncpattern_list)):
    syncpattern = syncpattern + chr(syncpattern_list[i])


def readbytes(num=1):
    newbyte = sourcefile.read(num)
    lastbytes[0] = newbyte
    byteindex[0] += num
    return newbyte


def skipbytes(num=1):
    sourcefile.read(num)
    byteindex[0] += num


counter = 0  # For checking if still alive.
while lastbytes[0]:  # Read bytes until no byte is read.
    counter += 1

    bytestr = readbytes(16)
    if bytestr[:12] == syncpattern:
        syncfile.write(str(byteindex[0]-16) + '\n')
        print byteindex[0]-16
        bytestr = readbytes(2048)
        for b in bytestr:
            splitfile.write(b)
        skipbytes(288)

    if counter % 10000000 == 0:
        print 'Reading..'

print 'Done.'
sourcefile.close()
splitfile.close()
syncfile.close()
