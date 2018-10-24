from setuptools import setup, find_packages

setup(
    name="freeFile",
    packages=find_packages(),
    version='0.0.1',
    description="command line tool for auto tuner",
    author="Cat.1",
    author_email='zhuyuefeng0@gmail.com',
    url="http://git.gansi.me/Cat.1/freeFile.git",
    download_url='http://git.gansi.me/Cat.1/freefile/-/archive/master/freefile-master.tar.gz',
    keywords=['command', 'line', 'tool', 'oss', 'update', 'download'],
    classifiers=[],
    install_requires=[
        'oss2',
        'hashlib',
        'configparser',
        'six'
    ]
)
