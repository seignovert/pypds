# -*- coding: utf-8 -*-
import pytest
import os
import datetime

from pypds import FOLDER, IMG


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
def folder_fmt():
    return '%Y%jT%H%M%S'

@pytest.fixture
def dt_start():
    return datetime.datetime(2013, 12, 27, 4, 43, 56)

@pytest.fixture
def dt_end():
    return datetime.datetime(2013, 12, 27, 5, 19, 8)

@pytest.fixture
def first_img():
    return '1766814041_1'

@pytest.fixture
def last_img():
    return '1766816153_1'

@pytest.fixture
def folder_url():
    return 'https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter' + \
        '/covims_0064/data/2013361T044356_2013361T051908/'

def test_url(folder, release, instrument, folder_url):
    assert FOLDER(folder, release, instrument).url == folder_url

def test_nb_imgs(folder, release, instrument):
    nb_imgs = FOLDER(folder, release, instrument).nb_imgs
    assert type(nb_imgs) is int
    assert nb_imgs >= 0

def test_split(folder, release, instrument, folder_fmt, dt_start, dt_end):
    start, end = FOLDER(folder, release, instrument).split(fmt=folder_fmt)
    assert start == dt_start
    assert end == dt_end

def test_first(folder, release, instrument, first_img):
    assert FOLDER(folder, release, instrument).first is None
    # [WARNING] imgs are not loaded from folder yet
    # assert FOLDER(folder, release, instrument).first == \
    #     IMG(first_img, folder, release, instrument)

def test_last(folder, release, instrument, last_img):
    assert FOLDER(folder, release, instrument).last is None
    # [WARNING] imgs are not loaded from folder yet
    # assert FOLDER(folder, release, instrument).last == \
    #     IMG(last_img, folder, release, instrument)
