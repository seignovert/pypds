# -*- coding: utf-8 -*-

import os
from lxml import html
import requests
import logging

from ._communs import ROOT_URL, MISSION, SPACECRAFT,\
                      INSTRUMENT, VERBOSE, PDS_OBJ, list_md5
from .pds_release import RELEASE

class PDS(PDS_OBJ):
    def __init__(self, inst=INSTRUMENT, verbose=VERBOSE):
        PDS_OBJ.__init__(self, inst, verbose)
        self.releases = sorted(list_md5(self.inst))
        return

    def __repr__(self):
        return 'PDS tree for the %s instrument onboard the %s of the %s mission' % (
            self.inst.upper(), self.spacecraft.title(), self.mission.title()
        )

    def __len__(self):
        return self.nb_releases

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
        if isinstance(release, (int,str)):
            releases = [release]
        else:
            releases = release

        for _release in releases:
            RELEASE(_release, self.inst, self.verbose, load=False).download
        return

    def remove_release(self, release=None):
        '''Remove one or a list of releases'''
        if isinstance(release, (int,str)):
            releases = [release]
        else:
            releases = release

        for _release in releases:
            RELEASE(_release, self.inst, self.verbose, load=False).remove
        return

    @property
    def update(self):
        '''Download new releases'''
        old = int(self.releases[-1].split('_')[1])
        new = range(old+1, self.last_release+1)
        if len(new) == 0 and self.verbose:
            print('No new releases available')
        else:
            print('All the new available releases will be downloaded')
            for release in new:
                self.download_release(release)
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
        return RELEASE(self.releases[-1], self.inst,
                       self.verbose, load=True).last

