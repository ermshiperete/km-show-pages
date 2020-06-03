#!/usr/bin/python3

import gi
import logging
import os.path
import re
import argparse


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Merge entries in file')
  parser.add_argument('file', help='file with entries to merge')
  parser.add_argument('-v', '--verbose', action='store_true',
                      help='verbose logging')
  parser.add_argument('-vv', '--veryverbose',
                      action='store_true', help='very verbose logging')

  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')
  elif args.veryverbose:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s:%(message)s')
  else:
    logging.basicConfig(format='%(levelname)s:%(message)s')

  stream = open(args.file, 'r')
  lines = stream.readlines()
  stream.close()

  pattern = re.compile("^\t- \[ \] (?P<kbName>[^ ]+) \((?P<file>[^ )]+)( \[(?P<encoding>[^]]+)\])?\)")
  keyboards = {}
  for line in lines:
    match = pattern.match(line)
    if match:
      kbName = match.group("kbName")
      file = match.group("file")
      encoding = match.group("encoding")
      keyboard = keyboards.get(kbName, {})
      keyboard[file] = encoding
      keyboards[kbName] = keyboard

  for kbName, files in dict(sorted(keyboards.items())).items():
    fileStr = ''
    for file, encoding in dict(sorted(files.items())).items():
      if encoding == None:
        fileStr += f'{file}, '
      else:
        fileStr += f'{file} [{encoding}], '
    print(f"  - [ ] {kbName} ({fileStr[0:-2]})")
