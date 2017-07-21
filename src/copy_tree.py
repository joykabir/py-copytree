#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Ziaul Kabir
# Date: 20-July-2017
# Released under MIT license

"""
Implements copytree function for python
"""
# pylint: disable=too-many-branches

from __future__ import print_function

import fnmatch
import os
from os.path import isdir, join
import shutil

def copy_tree(src, dest, ignore=None, symlink=False, force=False):
    """
    An advance and alternate implementation of copytree.

    :param src: The source path to copy from
    :param dest: The destination path to copy to
    :param ignore: Ignore patterns, as a function
    """

    #  Spcial characters in path ". ~"" are resolved
    spath = os.path.abspath(os.path.expanduser(src))
    dpath = os.path.abspath(os.path.expanduser(dest))

    # Create destination if it does not exist
    if not os.path.exists(dpath):
        os.makedirs(dpath)
        try:
            shutil.copystat(spath, dpath)
        except OSError:
            # Does not work in Windows
            pass

    # Get lists of all files and dirs in source path
    sitems = os.listdir(spath)

    # Call ignore function and get the items to ignore
    if ignore is not None:
        ignored_names = ignore(spath, sitems)
    else:
        ignored_names = set()


    for item in sitems:
        # If item is found in ignored patterns
        # then don't move ahead.
        if item in ignored_names:
            continue

        sitem = os.path.join(spath, item)
        ditem = os.path.join(dpath, item)

        # Handle symlink if it is True
        if os.path.islink(sitem):
            if symlink:
                if os.path.lexists(ditem):
                    os.remove(ditem)
                os.symlink(os.readlink(sitem), ditem)

        # If source item is a directory,
        # recursivly check
        elif os.path.isdir(sitem):
            copy_tree(sitem, ditem, ignore, symlink, force)

        # Skip if the file exists in the destination.
        # Overwite, if force is True
        elif os.path.isfile(ditem):
            if force:
                print('Overwriting destination: {}'.format(repr(ditem)))
                shutil.copy2(sitem, ditem)

        # Copy rest, those do not exists in destination
        else:
            print('Copying: {}'.format(repr(sitem)))
            shutil.copy2(sitem, ditem)

def ignore_patterns(*patterns):
    """
    List of patterns to ignore

    :param args patterns: Defines a sequence of glob-style patterns
                          to specify what files to ignore.
    """
    def _ignore_patterns(path, names):  # pylint: disable=unused-argument
        "returns ignore list"

        ignored_item = []
        for pattern in patterns:
            ignored_item.extend(fnmatch.filter(names, pattern))
        return set(ignored_item)

    return _ignore_patterns

def include_patterns(*patterns):
    """
    List of patterns to include

    See: https://stackoverflow.com/a/35161407
    There is a bug though in the answer.

    :param args patterns: Defines a sequence of glob-style patterns
                          to specify what files to NOT ignore.
    """
    def _ignore_patterns(path, names):
        "returns ignore list"

        keep = set(name for pattern in patterns
                   for name in fnmatch.filter(names, pattern))
        ignore = set(name for name in names
                     if name not in keep and not isdir(join(path, name)))
        return ignore

    return _ignore_patterns
