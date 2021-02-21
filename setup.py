#!/usr/bin/python3
#-*- coding: utf-8 -*-

from setuptools import setup, find_packages

# *************** Dependencies *********
INSTALL_REQUIRES = [
	'pyfields>=1.6'
	'valid8>=5.0',
	'makefun',
    'funcsigs;python_version<"3.3"',
	'enum34;python_version<"3.4"'
]  # 'sentinel',
DEPENDENCY_LINKS = []
EXTRAS_REQUIRE = {}

# ************** ID card *****************
DISTNAME         = 'DipTrace'
DESCRIPTION      = 'The DipTrace Library Generator'
MAINTAINER       = 'Oleksandr Kolodkin'
MAINTAINER_EMAIL = 'alexandr.kolodkin@gmail.com'
URL              = 'https://github.com/kolod/DipTrace-LibraryGenerator'
LICENSE          = 'BSD 3-Clause'
LICENSE_LONG     = 'License :: OSI Approved :: BSD License'
KEYWORDS         = 'diptrace pcb library generator'

setup(
	name=DISTNAME,
	description=DESCRIPTION,

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    # version=VERSION, NOW HANDLED BY GIT

	maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,

    license=LICENSE,
    url=URL,

	# See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
		#   1 - Planning
		#   2 - Pre-Alpha
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
		'Development Status :: 2 - Pre-Alpha',

		# Indicate who your project is intended for
		'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

		# Pick your license as you wish (should match "license" above)
        LICENSE_LONG,

		# Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.6',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
	],

	# What does your project relate to?
    keywords=KEYWORDS,

	# You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
	packages=find_packages(exclude=['test_*', 'lib_*']),

	# List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=INSTALL_REQUIRES,
    dependency_links=DEPENDENCY_LINKS,

	version='0.1.1',

	zip_safe=False
)