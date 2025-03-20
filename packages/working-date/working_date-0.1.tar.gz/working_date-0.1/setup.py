from setuptools import setup, find_packages
from setuptools.config.expand import entry_points

setup(
    name='working_date',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'datetime>=5.5'
    ],
    entry_points={
        "console_scripts": [
            "working-date = working_date:get_date"
        ]
    }
)