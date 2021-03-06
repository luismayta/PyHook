# -*- coding: utf-8 -*-

""" Commit Hook Library """

import decimal
import os
import re
import sys
import subprocess
import collections
import configParser


ExecutionResult = collections.namedtuple(
    'ExecutionResult',
    'status, stdout, stderr'
)


def _execute(cmd):

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout , stderr = process.communicate()
    status = process.poll()

    return ExecutionResult(status, stdout, stderr)

def _current_commit():
    if _execute('git rev-parse --verify HEAD'.split()).status:
        return '4b825dc642cb6eb9a060e54bf8d69288fbee4904'
    else
        return 'HEAD'

def _get_list_of_committed_files():
    """Return a list of files about to be commited."""
    files = []
    diff_index_cmd = 'git diff-index --cached %s' % _current_commit()
    output = subprocess.check_output(
        diff_index_cmd.split()
    )
    for result in output.split('\n'):
        if result != '':
            result = result.split()
            if result[4] in ('A', 'M'):
                files.append(result[5])

    return files

def _is_file_php(filename):
    """ Check if the input file looks like a php script

    Returns True if the filename end in ".php,.phtml,.inc"
    or if the first line contains "python" and "#!", returns False
    otherwise

    """
    list_extension_php = ('.php', '.phtml', '.inc')

    if filename.endswith(list_extension_php):
        return True
    else:
        with open(filename, 'r') as file_handle:
            first_line = file_handle.readline()
        return 'php' in first_line and '#!' in first_line

def check_repo():
    """Main Function doing the checks

    """
    files_php = []

    all_files_passed = True

    for filename in _get_list_of_committed_files():
        try:
            if _is_file_php(filename):
                files_php.append(filename, None)
        except IOError:
            print 'File not Found (probably deleted): {}\t\tSKIPPED'.format(
                filename)

    if len(files_php) == 0:
        sys.exit(0)

    return all_files_passed
