from setuptools import setup, find_packages

setup(
    name='datavalidatorchidimmaijoma',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    author='Chidimma Ijoma',
    author_email='nevusijoma@gmail.com',
    description='A simple data validation package',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Data-Epic/data-validator-chidimma-ijoma",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license="MIT",
)
