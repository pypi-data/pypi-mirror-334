from setuptools import setup, find_packages

setup(
    name='isoddeven',
    version='0.4.2',
    description='A Python package to check if a number is odd or even.',
    author='Nilay Sarma',
    packages=find_packages(),
    install_requires=[],
    license="MIT",
    url="https://github.com/nilaysarma/isoddeven",
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Repository": "https://github.com/nilaysarma/isoddeven",
        "Release Notes": "https://github.com/nilaysarma/isoddeven/releases/latest",
    },
)