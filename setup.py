#!/usr/bin/env python

import os
from setuptools import setup, find_packages


# --- >
VERSION = os.getenv("CI_COMMIT_TAG")
if not VERSION:
    VERSION = "0.0.1"

# --- >
setup(
    name="service-structure",
    version=VERSION,
    packages=find_packages(),
    long_description="Control device management external API",
    url="https://github.com/megamott/Service-structure.git",
    license="MIT",
    author="matvey.konoplyov",
    author_email="megamott27@gmail.com",
    python_requires=">=3.9",
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
    ],
)