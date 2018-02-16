# -*- coding: utf-8 -*-
import pytest
import datetime

from pypds import DB


@pytest.fixture
def instrument():
    return 'vims'

@pytest.fixture
def release():
    return 'covims_0064'

@pytest.fixture
def first():
    return (datetime.datetime(2013, 12, 25, 8, 36, 22), 1766654697)

@pytest.fixture
def last():
    return (datetime.datetime(2013, 12, 31, 14, 34, 18), 1767194848)

@pytest.fixture
def nb_imgs():
    return 164

def test_first(release, first):
    assert DB().first(release) == first

def test_last(release, last):
    assert DB().last(release) == last

def test_nb_imgs(release, nb_imgs):
    assert DB().nb_imgs(release) == nb_imgs

def test_nb_tot_imgs(instrument):
    nb_imgs = DB().nb_tot_imgs(instrument)
    assert type(nb_imgs) is int
    assert nb_imgs > 0
