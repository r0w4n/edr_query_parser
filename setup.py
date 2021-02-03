import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="edr query parser",
    version="1.3",
    author="r0w4n",
    author_email="r0w4n@nuisance.com",
    description="Environmental data retrieval API query parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/r0w4n/edr_query_parser",
    packages=setuptools.find_packages(),
    install_requires=[
        'python-dateutil',
        'geomet'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
