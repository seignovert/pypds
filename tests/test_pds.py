# -*- coding: utf-8 -*-
import pytest
import os
import datetime

from pypds import PDS, IMG
from pypds.folders import MD5


@pytest.fixture
def instrument():
    return 'vims'

@pytest.fixture
def release_md5():
    return os.path.join(MD5, 'covims_0064_md5.txt')

@pytest.fixture
def release_int():
    return 64

@pytest.fixture
def release_str():
    return 'covims_0064'

@pytest.fixture
def pds_url():
    return 'https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/'

def test_url(instrument, pds_url):
    assert PDS(instrument).url == pds_url

def test_last_release(instrument):
    assert type(PDS(instrument).last_release) is int

def test_remove_release_int(instrument, release_md5, release_int):
    PDS(instrument).remove_release(release_int)
    assert not os.path.isfile(release_md5)

def test_download_release_int(instrument, release_md5, release_int):
    PDS(instrument).download_release(release_int)
    assert os.path.isfile(release_md5)

def test_remove_release_str(instrument, release_md5, release_str):
    PDS(instrument).remove_release(release_str)
    assert not os.path.isfile(release_md5)

def test_download_release_str(instrument, release_md5, release_str):
    PDS(instrument).download_release(release_str)
    assert os.path.isfile(release_md5)

def test_releases(instrument):
    releases = PDS(instrument).releases
    assert type(releases) is list
    assert len(releases) > 0
    assert type(releases[0]) is str
    assert releases[0][:2] == 'co'
    assert '_' in releases[0]

def test_nb_releases(instrument):
    nb_releases = PDS(instrument).nb_releases
    assert type(nb_releases) is int
    assert nb_releases > 0

def test_nb_imgs(instrument):
    nb_imgs = PDS(instrument).nb_imgs
    assert type(nb_imgs) is int
    assert nb_imgs > 0

def test_start(instrument):
    assert type(PDS(instrument).start) is datetime.datetime

def test_end(instrument):
    assert type(PDS(instrument).end) is datetime.datetime

def test_first(instrument):
    assert type(PDS(instrument).first) is IMG

def test_last(instrument):
    assert type(PDS(instrument).last) is IMG
