from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sap_rfc_data_collector',
    packages=[
        'sap_rfc_data_collector',
    ],
    version='0.4',
    license='MIT',
    description='Collect data from SAP tables',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Victor Outtes',
    author_email='victor.outtes@gmail.com',
    url='https://github.com/victorouttes/sap-rfc-data-collector',
    download_url='https://github.com/victorouttes/sap-rfc-data-collector/archive/refs/tags/0.4.tar.gz',
    keywords=['sap', 'data', 'rfc', 'read_table', 'ec3', 'hana'],
    install_requires=[
        'Cython~=0.29.23',
        'pandas~=1.2.4',
        'pyrfc~=2.4.1',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)