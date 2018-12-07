from setuptools import setup, find_packages


setup(
    name="freeFile",
    packages=find_packages(),
    version='0.1.2',
    description="command line tool for auto update/download program.",
    author="Cat.1",
    author_email='git@gansi.me',
    url="https://github.com/import-yuefeng/freeFile.git",
    download_url='https://github.com/import-yuefeng/freeFile/archive/master.zip',
    keywords=['command', 'line', 'tool', 'oss', 'update', 'download'],
    scripts=['./ff'],
    # entry_points={'console_scripts': [
    # './ff']},
    install_requires=[
        'requests',
        'argparse',
        'configparser',
        'six',
        'sh'
    ]
)
