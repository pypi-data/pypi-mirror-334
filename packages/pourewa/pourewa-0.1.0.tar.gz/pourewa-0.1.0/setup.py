from setuptools import setup, find_packages

setup(
    name="pourewa",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "httplib2",
        "pydicom"
    ],
    author="Fraser Callaghan",
    author_email="callaghan.fm@gmail.com",
    description="A commandline tool for managing Orthanc DICOM servers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/fraser29/pourewa",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "pourewa=pourewa.pourewa:main",
        ],
    },
)