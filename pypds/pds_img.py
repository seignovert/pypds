# -*- coding: utf-8 -*-

from ._communs import INSTRUMENT, VERBOSE, PDS_OBJ

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
    def jpg(self, pref='v'):
        return self.extras('browse') + pref + self.img_id + '.qub.jpeg'

    @property
    def thumb(self, pref='v'):
        return self.extras('thumbnail') + pref + self.img_id + '.qub.jpeg_small'

    @property
    def tiff(self, pref='v'):
        return self.extras('tiff') + pref + self.img_id + '.qub.tiff'
