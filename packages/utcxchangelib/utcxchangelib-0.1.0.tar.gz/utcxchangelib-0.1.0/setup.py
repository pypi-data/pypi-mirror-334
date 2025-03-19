from setuptools import setup, find_packages

setup(
    name='utcxchangelib',
    version='0.1.0',
    author='Ian Magnell',
    author_email='ianmm3203@gmail.com',
    description='Client for xchangeV3',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

