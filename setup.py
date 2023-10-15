
from setuptools import setup

setup(
        name='beadroll',
        description='a pythonic mini script for ics file creation',
        version='0.0.1',
	long_description='a pythonic mini script for ics file creation made on the fly',
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

