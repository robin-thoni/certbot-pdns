#! /usr/bin/env python
from os import path
from setuptools import setup
from setuptools import find_packages

install_requires = [
    'acme',
    'certbot',
    'zope.interface',
]

here = path.abspath(path.dirname(__file__))

setup(
    name='certbot-pdns',
    version="1.2.0",

    description="Certbot DNS authenticator",
    long_description="""\
Authenticator plugin that performs dns-01 challenge by saving
necessary validation resources to appropriate records in a PowerDNS server.""",

    url='https://git.rthoni.com/robin.thoni/certbot-pdns',
    author="Robin Thoni",
    author_email='robin@rthoni.com',

    license='MIT',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: System Administrators',
        'Topic :: Internet :: Name Service (DNS)',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords="certbot authenticator plugin dns pdns powerdns api",

    packages=find_packages(),
    install_requires=install_requires,

    extras_require={
        'dev': [],
        'test': [],
    },

    package_data={
    },

    data_files=[('etc/letsencrypt', ['certbot-pdns.json'])],

    entry_points={
        'certbot.plugins': [
            'auth = certbot_pdns.authenticator:Authenticator',
        ],
    },
)
