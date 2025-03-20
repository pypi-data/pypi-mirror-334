#! /usr/bin/env python

import os
import re
import json
import platform
import argparse
from datetime import date


def stamp_version(line, pattern, version):
    new_line = re.sub(pattern, lambda m: m.group(0).replace(m.group(1), version, 1), line)
    return new_line


def view_file(current_version, filename, pattern):
    is_good = True
    pattern = pattern.replace('{version}', '(.*?)')
    with open(filename, 'r') as f:
        lines = f.readlines()

    print(f'\n=== {filename}')
    line_num = 0
    for line in lines:
        line_num += 1
        result = re.search(pattern, line)
        if result:
            file_version = result.group(1)
            print(f'line {line_num}:', line.rstrip())
            if not current_version == file_version:
                print(f'** Not set to current version: >{file_version}< should be >{current_version}<')
                is_good = False
    return is_good


def change_file(new_version, filename, pattern, dry_run=False):
    pattern = pattern.replace('{version}', '(.*?)')
    with open(filename, 'r') as f:
        lines = f.readlines()

    modded = ''

    print(f'\n=== {filename}')
    line_num = 0
    for line in lines:
        line_num += 1
        new_line = stamp_version(line, pattern, new_version)
        modded += new_line
        if not line == new_line:
            print(f'line {line_num} from:', line.rstrip())
            print(f'      {" " * len(str(line_num))}to:  ', new_line.rstrip())

    if not dry_run:
        with open(filename, 'w') as f:
            f.write(modded)
    else:
        print(' - unchanged')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--set', help='Provide the new version to set.')
    parser.add_argument('-v', '--view-files', help='View the current state of all files to stamp. (ignores --set)', action='store_true')
    parser.add_argument('-d', '--dry-run', help='See which files will change, and from what version.', action='store_true')
    parser.add_argument('-t', '--tag', help='Create git tag with current version (ignored if used with --set).', action='store_true')

    args = parser.parse_args()
    
    if not os.path.isfile('version_stamp.json'):
        print('version_stamp.json is missing')
        quit(1)


    with open('version_stamp.json', 'r') as f:
        stamps = json.load(f)


    current_version = stamps['version']
    print(f'Current version is {current_version}')

    new_version = args.set

    if args.view_files:
        print('Viewing files')
        all_good = True
        for file in stamps['files']:
            is_file_good = view_file(current_version, file['path'], file['pattern'])
            all_good = all_good and is_file_good
        if not all_good:
            print(f'\n*** One or more files do not match the current version of {current_version}')

    elif new_version:
        if args.dry_run:
            print('----- DRY RUN -----\n')
        print(f'Changing to {new_version}')
        for file in stamps['files']:
            change_file(new_version, file['path'], file['pattern'], args.dry_run)
            
        if not args.dry_run:
            stamps['version'] = new_version
            with open('version_stamp.json', 'w') as f:
                f.write(json.dumps(stamps, indent=4))

    elif args.tag:  # cannot tag when file is freshly changed - must add/commit first
        print(f'creating git tag {current_version}')
        today = date.today()
        silent = ' > /dev/null 2> /dev/null'
        if platform.system() == 'Windows':
            silent = ' > nul 2> nul'

        comment = f'Released {today}'
        os.system(f'git tag -d {current_version} {silent}')
        os.system(f'git tag -a {current_version} -m "{comment}"')


if __name__ == '__main__':
    main()
