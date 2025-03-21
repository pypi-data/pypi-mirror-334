#!/usr/bin/env python
from distutils.command.build import build as _build
import re
from setuptools import setup, find_packages
import subprocess
import platform


class build(_build):
    def run(self):
        if platform.system() == "Darwin":
            try:
                # Build our C library
                subprocess.check_call(['./Turbo/build_lib.sh'])
                _build.run(self)
            except:
                print("! Could not build turbo")


_versionRE = re.compile(r'__version__\s*=\s*\"([^\"]+)\"')
with open('Lib/fontgoggles/__init__.py', "r") as fg_init:
    match = _versionRE.search(fg_init.read())
    assert match is not None, "fontgoggles.__version__ not found"
    fg_version = match.group(1)

fg_version = "1.8.4.7"

setup(
    name="coldtype-fontgoggles",
    #use_scm_version={"write_to": "Lib/fontgoggles/_version.py"},
    version=fg_version,
    description="coldtype-fontgoggles is a PyPI-enabled version of the main library for the FontGoggles application.",
    author="Just van Rossum",
    author_email="justvanrossum@gmail.com",
    url="https://github.com/coldtype/fontgoggles",
    package_dir={"": "Lib"},
    packages=find_packages("Lib"),
    package_data={'fontgoggles.mac': ['*.dylib']},
    install_requires=[
        "blackrenderer>=0.6.0",
        "fonttools>=4.53.1",
        "uharfbuzz>=0.42.0",
        "python-bidi==0.4.2", # pinned for non-forward-compatibility
        "unicodedata2>=15.1.0",
    ],
    extras_require={
        "more-fonts": [
            "fonttools[woff,lxml,unicode,ufo,type1]>=4.53.1",
            "ufo2ft",
            "numpy"
        ]
    },
    setup_requires=["setuptools_scm<8.0.0"],
    python_requires=">=3.10",
    classifiers=[
    ],
    cmdclass={'build': build},
)
