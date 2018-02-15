# This will try to import setuptools. If not here, it fails with a message
try:
    from setuptools import setup
except ImportError:
    raise ImportError("PyPDS could not be installed, probably because"
        " setuptools is not installed on this computer."
        "\nInstall ez_setup ([sudo] pip install ez_setup) and try again.")

setup(name='pypds',
      version='0.1',
      description='Python package to manipulate the Cassini VIMS data.',
      url='http://github.com/seignovert/pypds',
      author='Benoit Seignovert',
      author_email='python@seignovert.fr',
      license='MIT',
      packages=['pypds'],
      install_requires=[
          'wget',
          'lxml',
          'requests',
          'logging',   
          'datetime',
      ],
      zip_safe=False)
