from setuptools import setup, find_packages

setup(
    name='pentachoron',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'numpy',

    ],
    description='pentachoron is a new light-weight library for Quantum computing. It has custom algorithms and gates!',
    author='Idrees Ahmad',
    author_email='thethinker22xd@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
