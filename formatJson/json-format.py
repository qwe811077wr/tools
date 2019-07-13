#coding=utf8

import argparse
import collections
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def main():
    prog = 'python -m json.tool'
    description = ('A simple command line interface for json module '
                   'to validate and pretty-print JSON objects.')
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument('infile', nargs='?', type=argparse.FileType(),
                        help='a JSON file to be validated or pretty-printed')
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                        help='write the output of infile to outfile')
    parser.add_argument('--sort-keys', action='store_true', default=False,
                        help='sort the output of dictionaries alphabetically by key')
    options = parser.parse_args()

    infile = options.infile or sys.stdin
    outfile = options.outfile or sys.stdout
    sort_keys = options.sort_keys
    with infile:
        try:
            if sort_keys:
                obj = json.load(infile)
            else:
                obj = json.load(infile,
                                object_pairs_hook=collections.OrderedDict)
        except ValueError as e:
            raise SystemExit(e)
    with outfile:
        json.dump(obj, outfile, sort_keys=sort_keys, ensure_ascii=False, indent=2)
        outfile.write('\n')


    
main()