from setuptools import setup, find_packages
import sys
import os

PACKAGE_NAME = "godrive"

# Platform-specific executables
if sys.platform == "win32":
    executables = ["bin/godrive.exe", "bin/godrive_upload.exe"]
else:
    executables = ["bin/godrive", "bin/godrive_upload"]

executables = [exe for exe in executables if os.path.exists(exe)]

setup(
    name=PACKAGE_NAME,
    version="1.0.2",
    author="Rohan Yadav",
    author_email="rohanbhatotiya@gmail.com",
    description="A CLI tool to upload files to Google Drive",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rohanbhatotiya/godrive",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "godrive=godrive.cli:main",
            "godrive_upload=godrive.cli:main",
        ],
    },
    data_files=[("bin", executables)],  # Install binaries
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
