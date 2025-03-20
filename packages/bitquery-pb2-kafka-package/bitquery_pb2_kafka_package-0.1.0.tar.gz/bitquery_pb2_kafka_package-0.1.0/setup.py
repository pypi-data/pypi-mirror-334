from setuptools import setup, find_packages

setup(
    name='bitquery-pb2-kafka-package',          # replace with your package name
    version='0.1.0',                # initial version
    packages=find_packages(),
    author='Bitquery',
    author_email='divyasshree@bitquery.io',
    description='This package contains the pb2 files necessary to interact with Bitquery Kafka Protobuf messages',
    url='https://github.com/bitquery/streaming-protobuf-python', 
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # classifier indicates license
        'Operating System :: OS Independent',
    ],
)
