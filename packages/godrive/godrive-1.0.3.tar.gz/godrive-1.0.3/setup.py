from setuptools import setup, find_packages

PACKAGE_NAME = "godrive"
VERSION = "1.0.3"
AUTHOR = "Your Name"
AUTHOR_EMAIL = "your-email@example.com"
DESCRIPTION = "Godrive CLI - Upload files to Google Drive easily"
URL = "https://github.com/yourusername/godrive"
LICENSE = "MIT"

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url=URL,
    license=LICENSE,
    packages=find_packages(),
    install_requires=[
        "pydrive2",
        "tqdm"
    ],
    entry_points={
        "console_scripts": [
            "godrive=godrive.godrive:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
