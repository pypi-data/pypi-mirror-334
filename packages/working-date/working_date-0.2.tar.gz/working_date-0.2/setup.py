from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='working_date',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'datetime>=5.5'
    ],
    entry_points={
        "console_scripts": [
            "working-date = working_date:get_date"
        ]
    },
    long_description=description,
    long_description_content_type="text/markdown",
)