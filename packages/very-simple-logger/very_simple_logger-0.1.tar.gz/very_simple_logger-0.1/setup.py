from setuptools import setup, find_packages

# python setup.py sdist
# twine upload dist/*

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
# open('Readme_check_spyder.md', encoding='utf-8').read(),
#packages=find_packages(),
#long_description=open('check_spyder/Readme.md', encoding='utf-8').read(),
setup(
    name='very_simple_logger',
    version='0.01',
    packages=['very_simple_logger'],
    description='Library to create a simple logger with a standard format.',
    long_description_content_type='text/markdown',
    long_description=long_description,
    author='Javier S. Zurdo',
    install_requires=['logging'],
    url='https://github.com/javierzurdo/Very_Simple_Logger',
    classifiers=[
                 'Programming Language :: Python :: 3',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                ],
    python_requires='>=3.6',
)