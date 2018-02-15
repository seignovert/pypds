# -*- coding: utf-8 -*-

import os

_ROOT = os.path.abspath(os.path.dirname(__file__))
MD5 = os.path.join(_ROOT, 'md5')
CSV = os.path.join(_ROOT, 'csv')

def mkdir(folder):
    '''Create directory if not exists'''
    if not os.path.isdir(folder):
        os.mkdir(folder)
    return

def isfile(root, fname, overwrite=False):
    '''Check if file exists and should be overwrite'''
    f = os.path.join(root, fname)
    if overwrite:
        print('[Warning] %s will be overwritten' % f)
    return (os.path.isfile(f) and not overwrite)
