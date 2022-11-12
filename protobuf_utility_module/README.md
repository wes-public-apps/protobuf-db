# Protobuf Utility Purpose
The goal of this utility is to provide an open source infrastructure to enable event driven data stream logging, translations, schema management, and simulation for a defined protobuf management tool. This specific module is focused being lean by providing solutions that require almost no third party dependencies. Other modules in this repo expand on specific aspects this module's functionality but are isolated since they require domain specific dependencies. If you want to get more out of this module check out those modules.

# Introduction
[Google's Protobuf Documentation](https://developers.google.com/protocol-buffers)

When an system uses a collection of microservices to accomplish its goal, one of the problems you must solve is defining a common message definition and libraries around that definition for each language you utilize in your microservice architecture so they can all communicate with each other effectively. Google solved this problem with their protobuf project which is actively maintained, public, and well documented. This makes it an ideal project to utilize in production.

There are many benefits to using the system outlined above that I will not get into here because they are discussed more effectively elsewhere (I recommend "Building Microservices" by Sam Newman) but one of the biggests cons is an increase in complexity around managing such a system. One chunk of that complexity is low latency handling of the messages being streamed between microservices. There is significant value in using those messages to gain real time insight into the health of your system and for deep analysis later on. That is where this protobuf utility comes into play. It provides infrastructure for logging the streamed messages, hooks to add custom in system processing logic, transforms to automate the data ingestion pipeline, and finally some data analysis tools.

# Protobuf Logger
This part of the protobuf utility handles logging the live stream of protobuf messages.

# Translation
This part of the protobuf utility handles converting the logged protobuf data into different formats. Specifically it converts the data to csv and to a database.

# Out of Scope
- Services
- Options

# Protobuf to Schema
This part of the protobuf-db utility converts an existing collection of protobuf message definitions as python objects into an sql schema.

# Protobuf Change to Schema Migration Script
This part of the protobuf-db utility takes a collection of protobuf message definitions, compares it to another collection in order to generate a migration sql file.

# Playback simulation
This part of the protobuf-db utility takes a collection of protobuf message objects that were collected using the logger utility and replays them for testing purposes.

# Developer GUI
This part of the protobuf utility provides tools to convert protobufs to a graphql schema and query.

# Future Work
1. Implement logging functionality in a lower level language such as C
2. implement real time processing infrastructure in a lower level language such a C
