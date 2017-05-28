#! /usr/bin/env python

from setuptools import setup
from setuptools import find_packages

install_requires = [
    'acme',
    'certbot',
    'zope.interface',
]

setup(
    name='certbot-pdns',
    description="Certbot DNS authenticator",
    url='https://git.rthoni.com/robin.thoni/certbot-pdns',
    author="Robin Thoni",
    author_email='robin@rthoni.com',
    license='MIT',
    install_requires=install_requires,
    packages=find_packages(),
    entry_points={
        'certbot.plugins': [
            'auth = certbot_pdns.authenticator:Authenticator',
        ],
    },
)
