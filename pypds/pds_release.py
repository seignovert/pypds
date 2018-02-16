# -*- coding: utf-8 -*-

import os
import wget

from ._communs import INSTRUMENT, VERBOSE, MD5, mkdir, isfile, PDS_OBJ
from .pds_folder import FOLDER
from .pds_img import IMG


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
    
    def __int__(self):
        return self.ref

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
        '''Download the md5 file release'''
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
    def remove(self):
        '''Remove the missing md5 file release'''
        mkdir(MD5)

        if isfile(MD5, self.md5, self.overwrite):
            os.remove(os.path.join(MD5, self.md5))
            if self.verbose:
                print('-> Removed md5 for the release %s' % str(self))
        elif self.verbose:
            print('-> The %s does not already exist' % self.md5)

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
