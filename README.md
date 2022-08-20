# Protobuf to Database Objects
This utility is for converting protobuf files into useful database objects.

# Installation
```
pip install protobuf-db
```
or clone the repo from github and then:
```
python3 setup.py install
```

# Introduction
[Google's Protobuf Documentation](https://developers.google.com/protocol-buffers)

When an system uses a collection of microservices to accomplish its goal, one of the problems you must solve is defining a common message definition and libraries around that definition for each language you utilize in your microservice architecture so they can all communicate with each other effectively. Google solved this problem with protobufs, an actively maintained, public, and well documented project making it ideal to build on.

One feature of such a system design is that you can get significant insight into the state of your system by logging the protobuf messages. The problem arises when it comes to analizing that data in an efficient and meaningful way. There are many amazing plug and play data analysis tools but they usually require your data to be in a database. While this is truthfully not a terrible process it can be made easier if there is a tool that can help you manage your database schemas based on provided protobufs. Protobuf message definitions already force the structure needed to define the database structure, that information just needs to be transformed. That is what this utility does.

# Protobuf to Schema
This part of the protobuf-db utility converts an existing collection of protobuf message definitions as python objects into an sql schema.


# Protobuf Change to Schema Migration Script
This part of the protobuf-db utility takes a collection of protobuf message definitions, compares it to another collection in order to generate a migration sql file.


