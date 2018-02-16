# -*- coding: utf-8 -*-

ROOT_URL = 'https://pds-imaging.jpl.nasa.gov'
MISSION = 'cassini'
SPACECRAFT = 'cassini_orbiter'
INSTRUMENT = 'vims'

VERBOSE = True

import os
import wget
from lxml import html
import requests
import logging
import datetime as dt

from .folders import MD5, CSV, mkdir, isfile


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

class PDS(PDS_OBJ):
    def __init__(self, inst=INSTRUMENT, verbose=VERBOSE):
        PDS_OBJ.__init__(self, inst, verbose)
        self.releases = self.list_md5
        return

    def __repr__(self):
        return 'PDS tree for the %s instrument onboard the %s of the %s mission' % (
            self.inst.upper(), self.spacecraft.title(), self.mission.title()
        )

    def __len__(self):
        return self.nb_releases

    @property
    def list_md5(self):
        '''List the releases downloaded'''
        releases = []
        for md5 in os.listdir(MD5):
            if md5.endswith('_md5.txt') and self.inst in md5:
                releases.append(md5.replace('_md5.txt', ''))
        return releases

    @property
    def nb_releases(self):
        '''Number of releases downloaded'''
        return len(self.releases)

    @property
    def nb_imgs(self):
        '''Number of image in the folder'''
        nb_imgs = 0
        for release in self.releases:
            nb_imgs += RELEASE(release,
                               self.inst, self.verbose).nb_imgs
        return nb_imgs

    @property
    def last_release(self):
        '''Check the last release available on the PDS'''
        if self.verbose:
            print('Checking the last release (%s)' % self.inst.upper())

        logging.getLogger("requests").setLevel(logging.WARNING)
        page = requests.get(self.root_url + '/volumes/' + self.inst + '.html')
        releases = html.fromstring(page.content).xpath('//center/text()')
        last_release = int(releases[-1].replace('Volume ', ''))

        if self.verbose:
            print('> Last release available: #%i' % last_release)
        return last_release

    def download_release(self, release=None):
        '''Download one or a list of releases'''
        if release is None:
            releases = range(1, self.last_release)
            if self.verbose:
                print('All the available releases will be downloaded')
        elif isinstance(release, (int,str)):
            releases = [release]
        else:
            releases = release

        for _release in releases:
            RELEASE(_release, self.inst, self.verbose, load=False).download
        return

    @property
    def start(self):
        '''Start time in the downloaded releases'''
        return RELEASE(self.releases[0], self.inst,
                       self.verbose, load=True).start

    @property
    def end(self):
        '''End time in the downloaded releases'''
        return RELEASE(self.releases[-1], self.inst,
                       self.verbose, load=True).end

    @property
    def first(self):
        '''First image in the downloaded releases'''
        return RELEASE(self.releases[0], self.inst,
                       self.verbose, load=True).first

    @property
    def last(self):
        '''Last image in the downloaded releases'''
        return RELEASE(self.releases[0], self.inst,
                       self.verbose, load=True).last

class RELEASE(PDS_OBJ):
    def __init__(self, ref, inst=INSTRUMENT, verbose=VERBOSE, load=True, overwrite=False):
        PDS_OBJ.__init__(self, inst, verbose)

        if isinstance(ref, int):
            self.ref = ref
        elif isinstance(ref, str):
            self.inst, ref = ref.replace('co','').split('_')
            self.ref = int(ref)
            self.inst 
        else:
            raise TypeError('Release id must be a INT or a STR (ex: `covims_0001`)')

        self.overwrite = overwrite
        self.folders = []
        if load:
            self.load
        return
    
    def __str__(self):
        return 'co%s_%.4i' % (self.inst.lower(), self.ref)

    def __repr__(self):
        return 'PDS release: %s' % str(self)

    def __len__(self):
        return self.nb_imgs

    @property
    def nb_folders(self):
        '''Number of folder in the release'''
        return len(self.folders)

    @property
    def nb_imgs(self):
        '''Number of image in the folder'''
        nb_imgs = 0
        for i in range(self.nb_folders):
            nb_imgs += self.folders[i].nb_imgs
        return nb_imgs

    @property
    def url(self):
        return '/'.join([
            self.root_url,
            'data',
            self.mission,
            self.spacecraft,
            str(self)
        ]) + '/'

    @property
    def md5(self):
        return str(self) + '_md5.txt'

    @property
    def url_md5(self):
        return '/'.join([
            self.root_url,
            'data',
            self.mission,
            self.spacecraft,
            self.md5
        ])

    @property
    def download(self):
        '''Download the missing md5 releases'''
        mkdir(MD5)

        if not isfile(MD5, self.md5, self.overwrite):
            if self.verbose:
                print('-> Download md5 for the release %s' % str(self))
            wget.download(self.url_md5, out=MD5)
            print('')  # Line return after wget ended

        elif self.verbose:
            print('-> The %s already exists' % self.md5)

        return
    
    @property
    def read(self):
        if not isfile(MD5, self.md5, self.overwrite):
            self.download

        with open(os.path.join(MD5, self.md5), 'r') as f:
            lines = f.readlines()
        return lines

    @property
    def load(self):
        '''Extract list of folders and images from md5 file'''
        if self.verbose:
            print('Extracting data from md5 file of release %s' %
                str(self)
            )

        prev = None
        for line in self.read:
            _line = line.split('/')

            if _line[1] == 'data':
                if _line[-1].endswith('.lbl\n'):
                    _folder = _line[-2]
                    _img = _line[-1][1:-5]

                    if prev is None or prev != _folder:
                        self.folders.append(
                            FOLDER(_folder, str(self), self.inst)
                        )
                        prev = _folder

                    self.folders[-1].imgs.append(
                        IMG(_img, _folder, str(self), self.inst)
                    )
        return

    @property
    def start(self):
        '''Release start time'''
        if len(self.folders) == 0:
            self.load
        return self.folders[0].start

    @property
    def end(self):
        '''Release end time'''
        if len(self.folders) == 0:
            self.load
        return self.folders[-1].end

    @property
    def first(self):
        '''Folder first image'''
        if len(self.folders) == 0:
            self.load
        return self.folders[0].first

    @property
    def last(self):
        '''Folder last image'''
        if len(self.folders) == 0:
            self.load
        return self.folders[-1].last


class FOLDER(PDS_OBJ):
    def __init__(self, name, release, inst=INSTRUMENT, fmt='%Y%jT%H%M%S'):
        PDS_OBJ.__init__(self, inst)
        self.name, self.start, self.end = self.split(name, fmt)
        self.release = release
        self.imgs = []
        return

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'PDS release folder: %s' % str(self)

    def __len__(self):
        return self.nb_imgs

    @property
    def nb_imgs(self):
        '''Number of images in the folder'''
        return len(self.imgs)

    @property
    def url(self):
        return '/'.join([
            self.root_url,
            'data',
            self.mission,
            self.spacecraft,
            self.release,
            'data',
            self.name
        ]) + '/'

    def split(self, folder, fmt='%Y%jT%H%M%S'):
        '''Split Date1_Date2 folder into datetime'''
        start, end = folder.split('_')

        # BugFix wrong date in PDS (covims_0003)
        if start[:4] == '1866':
            # Use the end year for substitution
            print('[Warning] Wrong year %s -> %s (%s)' % (
                start[:4], end[:4], folder
            ))
            start = end[:4]+start[4:]

        if end[:4] == '1866':
            # Use the start year for substitution
            print('[Warning] Wrong year %s -> %s (%s)' % (
                end[:4], start[:4], folder
            ))
            end = start[:4]+end[4:]

        return folder,\
            dt.datetime.strptime(start, fmt),\
            dt.datetime.strptime(end, fmt)

    @property
    def first(self):
        '''Folder first image'''
        if len(self.imgs) == 0:
            return None
        return self.imgs[0]

    @property
    def last(self):
        '''Folder last image'''
        if len(self.imgs) == 0:
            return None
        return self.imgs[-1]

class IMG(PDS_OBJ):
    def __init__(self, img_id, folder, release, inst=INSTRUMENT):
        PDS_OBJ.__init__(self, inst)
        self.img_id = img_id
        self.folder = folder
        self.release = release
        return

    def __str__(self):
        return self.img_id

    def __repr__(self):
        return 'PDS image: %s' % str(self)

    @property
    def url(self):
        return '/'.join([
            self.root_url,
            'data',
            self.mission,
            self.spacecraft,
            self.release,
            'data',
            self.folder
        ])+'/'

    def extras(self, extra='browse'):
        return '/'.join([
            self.root_url,
            'data',
            self.mission,
            self.spacecraft,
            self.release,
            'extras',
            extra,
            self.folder
        ])+'/'

    @property
    def lbl(self, pref='v'):
        return self.url + pref + self.img_id + '.lbl'

    @property
    def qub(self, pref='v'):
        return self.url + pref + self.img_id + '.qub'

    @property
    def img(self, pref='N'):
        return self.url + pref + self.img_id + '.img'

    @property
    def jpg(self, pref='v'):
        return self.extras('browse') + pref + self.img_id + '.qub.jpeg'

    @property
    def thumb(self, pref='v'):
        return self.extras('thumbnail') + pref + self.img_id + '.qub.jpeg_small'

    @property
    def tiff(self, pref='v'):
        return self.extras('tiff') + pref + self.img_id + '.qub.tiff'
