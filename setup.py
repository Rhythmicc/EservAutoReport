from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
VERSION = "0.0.6"

setup(
    name="EservAutoReport",
    version=VERSION,
    description="< your pypi lib description >",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="< your pypi lib keywords >",
    author="< your name >",
    url="< which url to find your lib >",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=["Qpro", "selenium"],
    entry_points={
        "console_scripts": [
            "cup-ear = EservAutoReport.main:main",
        ]
    },
)
