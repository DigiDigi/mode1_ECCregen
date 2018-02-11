#!/usr/bin/env python2.7

# Rejoin modified split.bin

import argparse
parser = argparse.ArgumentParser(description='Create a new patched binary.')
parser.add_argument('source', nargs='?', help='Original source. (Default: source.iso)')
parser.add_argument('split', nargs='?', help='Modified binary data. (Default: split.bin)')
parser.add_argument('sync', nargs='?', help='Sync locations. (Default: sync.txt)')
parser.add_argument('patched', nargs='?', help='Output patched file. (Default: patched.iso)')
args = parser.parse_args()
