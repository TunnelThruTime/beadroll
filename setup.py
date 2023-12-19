
from setuptools import setup
import site
import os

# Get the path to the site-packages directory
site_packages_dir = site.getsitepackages()[0]

# Create and write to the '.pth' file
with open(os.path.join(site_packages_dir, 'myproject.pth'), 'w') as f:
   f.write('docs/man/')

setup(
        name='beadroll',
        description='a pythonic mini script for ics file creation',
        version='0.0.1',
	long_description='a pythonic mini script for ics file creation made on the fly',
        data_files=[('/usr/local/share/man/man1', ['docs/man/beadroll.1'])],
        py_modules=['main'],
        author='Laurence Allan Lawlor',
        author_email='laurencelawlor@gmail.com',
        install_requires=[
            'Click',
	    'ics',
        'pretty_errors',
	    'rich',
            'ipython'],
        entry_points={
            'console_scripts': [
                'beadroll = main:cli' ],
            },  
        )   

