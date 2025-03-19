from setuptools import setup, find_packages

setup(
    name='vickycalulator',                   # Package name (must be unique on PyPI)
    version='0.2.0',                # Initial release version
    description='A simple calculation package',
    long_description=open('README.md').read(),
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