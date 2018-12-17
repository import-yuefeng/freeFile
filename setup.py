from setuptools import setup, find_packages


setup(
    name="freeFile",
    version='0.2.0',
    description="command line tool for auto update/download program.",
    author="Cat.1",
    author_email='git@gansi.me',
    url="https://github.com/import-yuefeng/freeFile.git",
    download_url='https://github.com/import-yuefeng/freeFile/archive/master.zip',
    keywords=['command', 'line', 'tool', 'oss', 'update', 'download'],
    scripts=['./ff'],
    packages=['client', 'client/API'],
    include_package_data=True,
    install_requires=[
        'requests',
        'argparse',
        'configparser',
        'six',
        'sh'
    ]
)
