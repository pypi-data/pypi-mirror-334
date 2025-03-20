from os import path
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='ul-db-utils',
    version='5.0.0a5',
    description='Python ul db utils',
    author='Unic-lab',
    author_email='',
    url='https://gitlab.neroelectronics.by/unic-lab/libraries/common-python-utils/db-utils.git',
    packages=find_packages(include=['ul_db_utils*']),
    platforms='any',
    package_data={
        '': ['*.sql'],
        'ul_db_utils': ['py.typed'],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            'uldbutls=ul_db_utils.main:main',
        ],
    },
    include_package_data=True,
    install_requires=[
        "flask==3.1.0",  # FOR COMPATIBILITY
        "py-dateutil==2.2",

        "psycopg2-binary==2.9.9",
        "psycogreen==1.0.2",
        "flask-sqlalchemy==3.1.1",
        "flask-migrate==4.1.0",
        "sqlalchemy[mypy]==2.0.29",
        "sqlalchemy-utils==0.41.2",
        "sqlalchemy-serializer==1.4.21",
        "alembic==1.14.1",
        "flask-mongoengine-3==1.1.0",

        "redis==5.2.1",

        "types-psycopg2==2.9.21.20250121",
        "types-sqlalchemy-utils==1.1.0",

        "ul-py-tool>=1.15.42",
    ],
)
