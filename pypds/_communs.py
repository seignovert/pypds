# -*- coding: utf-8 -*-

import os

ROOT_URL = 'https://pds-imaging.jpl.nasa.gov'
MISSION = 'cassini'
SPACECRAFT = 'cassini_orbiter'
INSTRUMENT = 'vims'

VERBOSE = True

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


class PDS_OBJ(object):
    def __init__(self, inst=INSTRUMENT, verbose=VERBOSE):
        self.root_url = ROOT_URL
        self.mission = MISSION
        self.spacecraft = SPACECRAFT
        self.inst = inst.lower()
        self.verbose = verbose
        return

    def __repr__(self):
        return 'PDS object for the %s instrument onboard the %s of the %s mission' % (
            self.inst.upper(), self.spacecraft.title(), self.mission.title()
        )

    @property
    def url(self):
        return '/'.join([
            self.root_url,
            'data',
            self.mission,
            self.spacecraft
        ]) + '/'
