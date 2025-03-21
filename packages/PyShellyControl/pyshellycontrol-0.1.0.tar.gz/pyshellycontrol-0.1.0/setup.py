from setuptools import setup, find_packages

setup(
    name='PyShellyControl',
    version='0.1.0',
    author='Michael Christian Dörflinger',
    author_email='michaeldoerflinger93@gmail.com',
    description='A python library for controlling shelly devices',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Michdo93/PyShellyControl',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'paho-mqtt',
    ],
)
