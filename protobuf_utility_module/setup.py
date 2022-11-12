from setuptools import setup, find_packages


tests_requires = []

dev_requires = [] + tests_requires

setup(
    name="protobuf-db",
    version="1.0.0",
    description="A python utility for managing protobuf database objects.",
    author='Wesley Murray',
    author_email='murraywj97@gmail.com',
    url='https://github.com/wes-public-apps/protobuf-db',
    download_url="https://github.com/wes-public-apps/protobuf-db/releases",
    license='MIT',
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="protobuf schema sql migration",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "protobuf == 4.21.6"
    ],
    tests_require=tests_requires,
    extras_require={
        'test': tests_requires,
        'dev': dev_requires,
    },
    include_package_data=True,
)
