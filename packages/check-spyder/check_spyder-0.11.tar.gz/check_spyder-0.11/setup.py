from setuptools import setup, find_packages

# python setup.py sdist
# twine upload dist/*

#packages=find_packages(),
#install_requires=['os'],
#long_description=open('check_spyder/Readme.md', encoding='utf-8').read(),
setup(
    name='check_spyder',
    version='0.11',
    packages=['check_spyder'],
    description='Library to detect if you are using Spyder IDE or not.',
    long_description_content_type='text/markdown',
    long_description=open('Readme_check_spyder.md', encoding='utf-8').read(),
    author='Javier S. Zurdo',
    url='https://github.com/javierzurdo/Check_Spyder',
    classifiers=[
                 'Programming Language :: Python :: 3',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                ],
    python_requires='>=3.6',
)