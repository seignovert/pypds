# -*- coding: utf-8 -*-
import pytest
import os
import datetime

from pypds import IMG


@pytest.fixture
def instrument():
    return 'vims'

@pytest.fixture
def release():
    return 'covims_0064'

@pytest.fixture
def folder():
    return '2013361T044356_2013361T051908'

@pytest.fixture
def img():
    return '1766814041_1'

@pytest.fixture
def url():
    return 'https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter' + \
        '/covims_0064/data/2013361T044356_2013361T051908/'

@pytest.fixture
def lbl():
    return 'https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter' + \
        '/covims_0064/data/2013361T044356_2013361T051908/v1766814041_1.lbl'

@pytest.fixture
def qub():
    return 'https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter' + \
        '/covims_0064/data/2013361T044356_2013361T051908/v1766814041_1.qub'

@pytest.fixture
def jpg():
    return 'https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter' + \
        '/covims_0064/extras/browse/' + \
        '2013361T044356_2013361T051908/v1766814041_1.qub.jpeg'

@pytest.fixture
def thumb():
    return 'https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter' + \
        '/covims_0064/extras/thumbnail/' + \
        '2013361T044356_2013361T051908/v1766814041_1.qub.jpeg_small'

@pytest.fixture
def tiff():
    return 'https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter' + \
        '/covims_0064/extras/tiff/' + \
        '2013361T044356_2013361T051908/v1766814041_1.qub.tiff'

def test_url(img, folder, release, instrument, url):
    assert IMG(img, folder, release, instrument).url == url

def test_lbl(img, folder, release, instrument, lbl):
    assert IMG(img, folder, release, instrument).lbl == lbl

def test_qub(img, folder, release, instrument, qub):
    assert IMG(img, folder, release, instrument).qub == qub

def test_jpg(img, folder, release, instrument, jpg):
    assert IMG(img, folder, release, instrument).jpg == jpg

def test_thumb(img, folder, release, instrument, thumb):
    assert IMG(img, folder, release, instrument).thumb == thumb

def test_tiff(img, folder, release, instrument, tiff):
    assert IMG(img, folder, release, instrument).tiff == tiff
