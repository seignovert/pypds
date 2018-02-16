# -*- coding: utf-8 -*-
import pytest
import os
import datetime

from pypds import RELEASE, IMG
from pypds.folders import MD5


@pytest.fixture
def instrument():
    return 'vims'

@pytest.fixture
def release_md5():
    return 'covims_0064_md5.txt'

@pytest.fixture
def release_int():
    return 64

@pytest.fixture
def release_str():
    return 'covims_0064'

@pytest.fixture
def release_url():
    return 'https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter/covims_0064/'


def test_release(release_int, release_str, instrument):
    assert str(RELEASE(release_int, instrument)) == release_str
    assert int(RELEASE(release_str, instrument)) == release_int

def test_md5(release_int, instrument, release_md5):
    assert RELEASE(release_int, instrument).md5 == release_md5

def test_url(release_int, instrument, release_url):
    assert RELEASE(release_int, instrument).url == release_url

def test_nb_folders(release_int, instrument):
    nb_folders = RELEASE(release_int, instrument).nb_folders
    assert type(nb_folders) is int
    assert nb_folders > 0

def test_nb_imgs(release_int, instrument):
    nb_imgs = RELEASE(release_int, instrument).nb_imgs
    assert type(nb_imgs) is int
    assert nb_imgs > 0

def test_start(release_int, instrument):
    assert type(RELEASE(release_int, instrument).start) is datetime.datetime

def test_end(release_int, instrument):
    assert type(RELEASE(release_int, instrument).end) is datetime.datetime

def test_first(release_int, instrument):
    assert type(RELEASE(release_int, instrument).first) is IMG

def test_last(release_int, instrument):
    assert type(RELEASE(release_int, instrument).last) is IMG
