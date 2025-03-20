# setup.py
from setuptools import setup, find_packages

setup(
    name='luziip',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',  
    ],
    description='A simple IP info fetcher',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='luzi inc',
    author_email='help@luzitool.ct.ws',
    url='https://luzitool.ct.ws/luziip.php',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
