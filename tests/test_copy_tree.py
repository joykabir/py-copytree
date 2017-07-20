# -*- coding: utf-8 -*-

# Author: Ziaul Kabir
# Date: 20-July-2017
# Released under MIT license

"""
Tests copy_tree function
"""
from contextlib import contextmanager

import os
import shutil
import tempfile

import pytest

from src.copy_tree import copy_tree, ignore_patterns, include_patterns

@pytest.mark.parametrize('result, slink', (('success', True),
                                           ('success', False),
                                           ('error', True),
                                           ('error', False)))
def test_copy_tree(result, slink):
    """
    Tests copy_tree function
    """
    src = tempfile.mkdtemp()
    dest = tempfile.mkdtemp()

    try:
        if result == 'success':
            add_data(src)

        copy_tree(src, dest, symlink=slink)

        for root, dirs, files in os.walk(dest):
            if root == src and result == 'success':
                assert 'foobar' in dirs

            if root == src and result == 'error':
                assert 'foobar' not in dirs

            if str(root).endswith('foobar'):
                assert 'myfile.jpg' in files

    finally:
        shutil.rmtree(src)
        shutil.rmtree(dest)
@pytest.mark.parametrize('kind', ['ignore', 'include'])
def test_copy_tree_ignore(kind):
    """
    Test copy_tree with ignore enabled
    """

    src = tempfile.mkdtemp()
    dest = tempfile.mkdtemp()
    add_data(src)

    try:
        if kind == 'ignore':
            copy_tree(src, dest, ignore=ignore_patterns('*.jpg'), force=False)

            for root, dirs, files in os.walk(dest):
                if root == dest:
                    assert 'foobar' in dirs
                if str(root).endswith('foobar'):
                    assert 'myfile.jpg' not in files
        if kind == 'include':
            copy_tree(src, dest, ignore=include_patterns('*.jpg'), force=True)

            for root, dirs, files in os.walk(dest):
                if root == dest:
                    assert 'foobar' in dirs
                if str(root).endswith('foobar'):
                    assert 'myfile.jpg' in files
    finally:
        shutil.rmtree(src)
        shutil.rmtree(dest)

def add_data(path):
    """
    Add fake data
    """
    os.makedirs(os.path.join(path, 'foobar'))
    f_path = os.path.join(path, 'foobar', 'myfile.jpg')

    with open_file(f_path, 'w') as filereader:
        filereader.write('{"Name": "Fake"}')

@contextmanager
def open_file(path, mode):
    """
    Open file in path
    """
    target_file = open(path, mode)
    yield target_file
    target_file.close()
