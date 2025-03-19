import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='vickycalulator',                   # Package name (must be unique on PyPI)
    version='0.3.0',                # Initial release version
    description='A Python package offering basic math calculations',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Vicky',
    author_email='vickyvijay069@gmail.com',
    # url='https://github.com/yourusername/vicky',  # Optional, your repo URL
    packages=find_packages(),       # Automatically find package directories
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',        # Specify minimum Python version if needed
)