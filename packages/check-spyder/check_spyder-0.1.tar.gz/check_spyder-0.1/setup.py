from setuptools import setup, find_packages

# python setup.py sdist
# twine upload dist/*

#packages=find_packages(),
setup( 
    name='check_spyder',
    version='0.1',
    packages=['check_spyder'],
    description='Library to detect if you are using Spyder IDE or not.',
    long_description=open('check_spyder/README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Javier S. Zurdo',
    url='https://github.com/javierzurdo/Check_Spyder',
    install_requires=['os'],
)