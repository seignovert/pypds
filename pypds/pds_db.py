# -*- coding: utf-8 -*-

import os
import sqlite3

from ._communs import DB_NAME, MD5, INSTRUMENT, date_split, list_md5
from .pds_release import RELEASE, IMG

class DB(object):
    def __init__(self):
        self.connexion = sqlite3.connect(DB_NAME)
        self.cursor = self.connexion.cursor()
        return

    def __del__(self):
        self.connexion.close()

    def __repr__(self):
        return 'PDS database'

    @property
    def delete(self):
        '''Delete the database'''
        user = raw_input('Delete PDS database? [y/N]: ')
        if user == 'y' or user == 'Y':
            self.connexion.close()
            os.remove(DB_NAME)

    @property
    def commit(self):
        '''Run COMMIT'''
        self.connexion.commit()

    def execute(self, sql, data):
        '''Execute SQL statement'''
        self.cursor.execute(sql, data)
        self.commit

    def executemany(self, sql, data):
        '''Execute many SQL statement'''
        self.cursor.executemany(sql, data)
        self.commit

    @property
    def vacuum(self):
        '''Clean the database'''
        self.cursor.execute('VACUUM')

    def fetchOne(self, sql):
        '''Fetch first row'''
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def fetchAll(self, sql):
        '''Fetch all rows'''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def drop_table(self, tname):
        '''Drop exisiting table'''
        self.commit
        self.cursor.execute('DROP TABLE IF EXISTS '+tname)

    def create_table(self, tname, fields, overwrite=True):
        '''
        Create new table

        overwrite: Drop table and data is already exists [True]
        '''
        sql = 'CREATE TABLE %s (\n\t' % tname
        cols = []
        for field in fields:
            col = '\t'.join([field['id'], field['type']])
            cols.append(col)
        sql += ',\n\t'.join(cols) + '\n);'
        
        if overwrite:
            self.drop_table(tname)

        self.cursor.execute(sql)

    @property
    def releases_fields(self):
        '''ALL_RELEASES table fields'''
        return [
            {'id': 'release', 'type': 'TEXT PRIMARY KEY'},
            {'id': 'start', 'type': 'TEXT NOT NULL'},
            {'id': 'end', 'type': 'TEXT NOT NULL'},
            {'id': 'first', 'type': 'INTEGER UNIQUE'},
            {'id': 'last', 'type': 'INTEGER UNIQUE'},
            {'id': 'nb_imgs', 'type': 'INTEGER'},
        ]

    @property
    def md5_fields(self):
        '''MD5 table fields'''
        return [
            {'id': 'img_id', 'type': 'TEXT PRIMARY KEY'},
            {'id': 'folder', 'type': 'TEXT NOT NULL'}
        ]

    def insert_release(self, release):
        '''Insert release infos'''
        sql = 'INSERT INTO all_%s VALUES (?,?,?,?,?,?)' % release.inst
        start, first = self.first(release)
        end, last = self.last(release)
        nb_imgs = self.nb_imgs(release)
        data = (str(release), start, end, first, last, nb_imgs)
        self.execute(sql, data)

    def insert_folder(self, folder):
        '''Insert images from release'''
        sql = 'INSERT INTO %s VALUES (?,?)' % folder.release
        data = []
        for img in folder.imgs:
            data.append((str(img), str(folder)))
        self.executemany(sql, data)

    def build(self, inst=INSTRUMENT):
        '''
        Build the database based on MD5 files available
        for a specific instrument
        '''
        inst = inst.lower()
        self.create_table('all_'+inst, self.releases_fields)
        
        for md5 in list_md5(inst):
            release = RELEASE(md5)
            self.create_table(md5, self.md5_fields)
            
            for folder in release.folders:
                self.insert_folder(folder)
            
            self.insert_release(release)
        self.vacuum

    def first(self, release, fmt='%Y%jT%H%M%S'):
        '''Search for the first image in a release'''
        sql = 'SELECT img_id, folder FROM %s ORDER BY img_id LIMIT 1' % release
        img, folder = self.fetchOne(sql)
        first, _ = date_split(folder, fmt)
        return first, int(img.split('_')[0])

    def last(self, release, fmt='%Y%jT%H%M%S'):
        '''Search for the last image in a release'''
        sql = 'SELECT img_id, folder FROM %s ORDER BY img_id DESC LIMIT 1' % release
        img, folder = self.fetchOne(sql)
        _, last = date_split(folder, fmt)
        return last, int(img.split('_')[0])

    def nb_imgs(self, release):
        '''Count the number of images in a release'''
        sql = 'SELECT COUNT(img_id) FROM %s' % release
        return int(self.fetchOne(sql)[0])

    def nb_tot_imgs(self, inst):
        '''
        Count the total number of images in the database
        for a specific instrument'''
        sql = 'SELECT SUM(nb_imgs) FROM all_%s' % inst.lower()
        return int(self.fetchOne(sql)[0])

    def img(self, img_id, inst=INSTRUMENT):
        '''Search IMG with img_id'''
        img_key = int(img_id.split('_')[0])
        sql = 'SELECT release FROM all_%s ' % inst.lower()
        sql += 'WHERE first >= %i ORDER BY release LIMIT 1' % img_key
        release = self.fetchOne(sql)
        if not release is None:
            img = self.img_release(img_id, release[0])
        if img is None:
            img = self.img_all(img_id, inst)
        return img

    def img_release(self, img_id, release):
        '''Search IMG with img_id in a specific release'''
        sql = 'SELECT * FROM %s ' % release
        sql += 'WHERE img_id = "%s" LIMIT 1' % img_id
        img = self.fetchOne(sql)
        if not img is None:
            return IMG(img[0], img[1], release)
        return None

    def releases(self, inst=INSTRUMENT):
        '''Search all the releases for an instrument'''
        sql = 'SELECT release FROM all_%s' % inst.lower()
        list = self.fetchAll(sql)
        if not list is None:
            releases = []
            for release in list:
                releases.append(release[0])
            return releases
        return None

    def img_all(self, img_id, inst=INSTRUMENT):
        '''Search IMG all the available releases in the database'''
        imgs = []
        for release in self.releases(inst):   
            sql = 'SELECT * FROM %s ' % release
            sql += 'WHERE img_id LIKE "%%%s%%"' % img_id
            _imgs = self.fetchAll(sql)
            if len(_imgs) == 1:
                imgs.append(
                    IMG(_imgs[0][0], _imgs[0][1], release)
                )
            elif len(_imgs) > 1:
                for img in _imgs:
                    imgs.append(IMG(img[0], img[1], release))

        if len(imgs) == 0:
            raise ValueError('Image %s not found' % img_id)
        elif len(imgs) == 1:
            return imgs[0]
        return imgs
