from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

#python setup.py sdist bdist_wheel to import
#twine upload dist/* to upload
setup(
    name='seleniumeasy',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'pandas>=2.2.3',
        'requests>=2.32.3',
        'bs4>=0.0.2',
        'selenium>=4.29.0',
        'lxml>=5.3.1'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
