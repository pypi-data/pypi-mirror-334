import setuptools

# Package metadata
NAME = "MongoRex"
VERSION = "1.0.1"
DESCRIPTION = "MongoRex simplifies MongoDB operations by providing a clean, reusable interface for CRUD, indexing, aggregation, and database management tasks."
URL = "https://github.com/TraxDinosaur/MongoRex"
AUTHOR = "TraxDinosaur"
AUTHOR_CONTACT = "https://traxdinosaur.github.io"
LICENSE = "CC-BY-SA 4.0"
KEYWORDS = ["MongoDB", "Python MongoDB", "MongoDB operations", "CRUD operations", "Database management",
            "MongoDB Python package", "MongoDB CRUD", "MongoDB indexing", "MongoDB aggregation",
            "Database interface", "MongoDB toolkit", "Python database library", "MongoRex"]

# Read long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

# Packages required by the project
REQUIRED_PACKAGES = [
    "pymongo"
]

setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_contact=AUTHOR_CONTACT,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved",
        "Operating System :: OS Independent",
    ],
    keywords=KEYWORDS,
    install_requires=REQUIRED_PACKAGES,
    python_requires=">=3.6",
)