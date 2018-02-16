PyPDS
===
Python package to manipulate the Cassini VIMS data from the PDS.

Install
---
```bash
python setup.py install|develop
```

Init
---
```python
import pypds as pds

# Check the last release for `VIMS` available on the PDS
pds.PDS('VIMS').last_release

# List the releases downloaded
pds.PDS('VIMS').releases

# Download all the new releases
pds.PDS('VIMS').update

# Download a single release
pds.PDS('VIMS').download_release(1)
# or
pds.PDS('VIMS').download_release('covims_0001')

# Download a serie releases
pds.PDS('VIMS').download_release([1,2,3])

# Count the number of images included in the downloaded releases
pds.PDS('VIMS').nb_imgs
# or
len(pds.PDS('VIMS'))

# Get start time in the downloaded releases
pds.PDS('VIMS').start
# Get release end time in the downloaded releases
pds.PDS('VIMS').end

# Get first image in the downloaded releases
pds.PDS('VIMS').first
# Get last image in the downloaded releases
pds.PDS('VIMS').last

```

Usage
---
```python
import pypds as pds

## RELEASES

# Load a release
pds.RELEASE('covims_0001')
# or
pds.RELEASE(1, inst='VIMS')
# or [default: `VIMS`]
pds.RELEASE(1)

# (If the MD5 file does not exist it will be downloaded into `./md5/` folder)

# Update release
pds.RELEASE('covims_0001', overwrite=True, load=False).download

# Get release folders
pds.RELEASE('covims_0001').folders

# Count the number of images included in the release
pds.RELEASE('covims_0001').nb_imgs
# or
len(pds.RELEASE('covims_0001'))

# Get release start time
pds.RELEASE('covims_0001').start
# Get release end time
pds.RELEASE('covims_0001').end

# Get release first image
pds.RELEASE('covims_0001').first
# Get release last image
pds.RELEASE('covims_0001').last


## FOLDERS

# Get a specific folder
pds.FOLDER('2000262T123038_2000262T132642', 'covims_0001')

# Count the number of images included in the folder
pds.FOLDER('2000262T123038_2000262T132642', 'covims_0001').nb_imgs
# or
len(pds.FOLDER('2000262T123038_2000262T132642', 'covims_0001'))

# Get folder start time
pds.FOLDER('2000262T123038_2000262T132642', 'covims_0001').start
# Get folder end time
pds.FOLDER('2000262T123038_2000262T132642', 'covims_0001').end

# Get folder first image
pds.FOLDER('2000262T123038_2000262T132642', 'covims_0001').first
# Get folder last image
pds.FOLDER('2000262T123038_2000262T132642', 'covims_0001').last


## IMAGES

# Get a specific image
img = pds.IMG('1347971911_3','2000262T123038_2000262T132642', 'covims_0001')

# Get its `.LBL` location
img.lbl
# Get its `.QUB` location
img.qub
# Get its `.JPG` location
img.jpg
# Get its `.JPG thumbnail` location
img.thumb
# Get its `.TIFF` location
img.tiff
```

Database
---
```python
from pypds import DB

# Create the database based on MD5 files
# available for a specific instrument
DB().build('vims')

# Search for the first image in a release
DB().first('covims_0001')

# Search for the last image in a release
DB().last('covims_0001')

# Count the number of images in a release
DB().nb_imgs('covims_0001')

# Count the total number of images in the database
DB().nb_tot_imgs
# or
len(DB())

# Delete the database
DB().delete

```


Dependencies:
---
- `wget`
- `lxml`
- `requests`
- `logging`
- `datetime`
