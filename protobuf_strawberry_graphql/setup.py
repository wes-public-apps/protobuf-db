from setuptools import setup, find_packages


tests_requires = []

dev_requires = [] + tests_requires

setup(
    name="protobuf-strawberry-graphql",
    version="0.1.0",
    description='''
    Infrastructure for converting protobuf objects to a graphql model using python's strawberry
    library.
    ''',
    author='Wesley Murray',
    author_email='murraywj97@gmail.com',
    license='MIT',
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="protobuf strawberry graphql",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "protobuf == 4.21.6",
        "strawberry-graphql == 0.142.1"
    ],
    tests_require=tests_requires,
    extras_require={
        'test': tests_requires,
        'dev': dev_requires,
    },
    include_package_data=True,
)
