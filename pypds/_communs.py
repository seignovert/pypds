# -*- coding: utf-8 -*-

import os
import datetime as dt

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


def date_split(name, fmt='%Y%jT%H%M%S'):
    '''Split Date1_Date2 folder into datetime'''
    start, end = name.split('_')

    # BugFix wrong date in PDS (covims_0003)
    if start[:4] == '1866':
        # Use the end year for substitution
        print('[Warning] Wrong year %s -> %s (%s)' % (
            start[:4], end[:4], name
        ))
        start = end[:4]+start[4:]

    if end[:4] == '1866':
        # Use the start year for substitution
        print('[Warning] Wrong year %s -> %s (%s)' % (
            end[:4], start[:4], name
        ))
        end = start[:4]+end[4:]

    return dt.datetime.strptime(start, fmt),\
        dt.datetime.strptime(end, fmt)


def list_md5(inst):
    '''List the releases downloaded for specific instrument'''
    releases = []
    for md5 in os.listdir(MD5):
        if md5.endswith('_md5.txt') and inst in md5:
            releases.append(md5.replace('_md5.txt', ''))
    return releases


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
