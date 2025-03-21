from setuptools import setup, find_packages

setup(
    name="gps-tools-pkg",
    version="0.1.2",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    description="Tools for handling GPS data and calculations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/gps_tools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: GIS",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.6",
    keywords="gps, navigation, geolocation",
) 