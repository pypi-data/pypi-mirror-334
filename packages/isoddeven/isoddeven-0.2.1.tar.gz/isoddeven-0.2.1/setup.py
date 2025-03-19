from setuptools import setup, find_packages

setup(
    name='isoddeven',
    version='0.2.1',
    description='A fun Python package to find out if a number is odd or even vouched at mewtru.com/is-odd',
    author='Nilay Sarma',
    packages=find_packages(),
    install_requires=["requests"],
    license="MIT"
)