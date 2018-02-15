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

# Check the last release for `VIMS`
pds.PDS('VIMS').last_release

# Download all the available releases
pds.PDS('VIMS').download_all
```

Usage
---
```python
import pypds as pds

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

# Get release start time
pds.RELEASE('covims_0001').start

# Get release end time
pds.RELEASE('covims_0001').end

# Get release first image
pds.RELEASE('covims_0001').first

# Get release last image
pds.RELEASE('covims_0001').last

# Get first image of the first folder
pds.RELEASE('covims_0001').folders[0].imgs[0]

# Get its `.LBL` location
pds.RELEASE('covims_0001').folders[0].imgs[0].lbl

# Get its `.QUB` location
pds.RELEASE('covims_0001').folders[0].imgs[0].qub

# Get its `.JPG` location
pds.RELEASE('covims_0001').folders[0].imgs[0].jpg

# Get its `.JPG thumbnail` location
pds.RELEASE('covims_0001').folders[0].imgs[0].thumb

# Get its `.TIFF` location
pds.RELEASE('covims_0001').folders[0].imgs[0].tiff
```


Dependencies:
---
- `wget`
- `lxml`
- `requests`
- `logging`
- `datetime`
