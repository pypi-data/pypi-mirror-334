import setuptools

about = {}
with open("mindsdb_sql_parser/__about__.py") as fp:
    exec(fp.read(), about)

setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],
    url=about['__github__'],
    download_url=about['__pypi__'],
    license=about['__license__'],
    author=about['__author__'],
    author_email=about['__email__'],
    description=about['__description__'],
    packages=setuptools.find_packages(exclude=('tests*',)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)
